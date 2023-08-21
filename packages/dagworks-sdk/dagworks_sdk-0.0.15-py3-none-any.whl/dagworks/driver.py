# Copyright (C) 2023-Present DAGWorks Inc.
#
# For full terms email support@dagworks.io.
#
# This software and associated documentation files (the "Software") may only be
# used in production, if you (and any entity that you represent) have agreed to,
# and are in compliance with, the DAGWorks Enterprise Terms of Service, available
# via email (support@dagworks.io) (the "Enterprise Terms"), or other
# agreement governing the use of the Software, as agreed by you and DAGWorks,
# and otherwise have a valid DAGWorks Enterprise license for the
# correct number of seats and usage volume.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import hashlib
import inspect
import json
import logging
import os
import uuid
from types import ModuleType
from typing import Any, Callable, Dict, List, Set, Tuple, Union

from hamilton import base, driver, node, graph
from hamilton.driver import Variable
from hamilton.io import materialization

try:
    import git
except ImportError:
    git = None

from dagworks.api import clients, constants
from dagworks.api.projecttypes import GitInfo
from dagworks.parsing.parse import parse_dag
from dagworks.telemetry.telemetry import get_adapter_representation, global_tracker
from dagworks.tracking.runs import Status, TrackingState, monkey_patch_adapter

logger = logging.getLogger(__name__)


def _hash_module(
    module: ModuleType, hash_object: hashlib.sha256, seen_modules: Set[ModuleType]
) -> hashlib.sha256:
    """Generate a hash of the specified module and its imports.

    It will recursively hash the contents of the modules and their imports, and only does so
    if the import is from the same package. This is to avoid hashing the entire python
    environment...

    :param module: the python module to hash and then crawl.
    :param hash_object: the object to update.
    :param seen_modules: the python modules we've already hashed.
    :return: the updated hash object
    """
    # Check if we've already hashed this module
    if module in seen_modules:
        return hash_object
    else:
        seen_modules.add(module)
    # Update the hash with the module's source code
    if hasattr(module, "__file__") and module.__file__ is not None:
        with open(module.__file__, "rb") as f:
            hash_object.update(f.read())
    else:
        logger.debug(
            "Skipping hash for module %s because it has no __file__ attribute or it is None.",
            module,
        )

    # Loop through the module's attributes
    for name, value in inspect.getmembers(module):
        # Check if the attribute is a module
        if inspect.ismodule(value):
            if value.__package__ is None:
                logger.info(
                    f"Skipping hash for module {value.__name__} because it has no __package__ "
                    f"attribute or it is None. This happens with lazy loaders."
                )
                continue
            # Check if the module is in the same top level package
            if value.__package__ != module.__package__ and not value.__package__.startswith(
                module.__package__
            ):
                logger.debug(
                    f"Skipping hash for module {value.__name__} because it is in a different "
                    f"package {value.__package__} than {module.__package__}"
                )
                continue
            # Recursively hash the sub-module
            hash_object = _hash_module(value, hash_object, seen_modules)

    # Return the hash object
    return hash_object


def _get_modules_hash(modules: Tuple[ModuleType]) -> str:
    """Generate a hash of the contents of the specified modules.

    It recursively hashes the contents of the modules and their imports, and only does so
    if the import is from the same package. This is to avoid hashing the entire python
    environment...

    :param modules: python modules to hash
    :return: the hex digest of the hash
    """
    # Create a hash object
    h = hashlib.sha256()
    seen_modules = set()

    # Loop through each module name
    for module in modules:
        # Update the hash with the module's source code
        h = _hash_module(module, h, seen_modules)

    # Return the hex digest of the hash
    return h.hexdigest()


def _derive_version_control_info(module_hash: str) -> GitInfo:
    """Derive the git info for the current project.
    Currently, this decides whether we're in a git repository.
    This is not going to work for everything, but we'll see what the customers want.
    We might end up having to pass this data in...
    """
    default = GitInfo(
        branch="unknown",
        commit_hash=module_hash,
        committed=False,
        repository="Error: No repository to link to.",
        local_repo_base_path=os.getcwd(),
    )
    if git is None:
        return default
    try:
        repo = git.Repo(".", search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        logger.warning(
            "Warning: We are not currently in a git repository. We recommend using that as a "
            "way to version the "
            "project *if* your hamilton code lives within this repository too. If it does not,"
            " then we'll try to "
            "version code based on the python modules passed to the Driver. "
            "Incase you want to get set up with git quickly you can run:\n "
            "git init && git add . && git commit -m 'Initial commit'\n"
            "Still have questions? Reach out to stefan @ dagworks.io, elijah @ dagworks.io "
            "and we'll try to help you as soon as possible."
        )
        return default
    if "COLAB_RELEASE_TAG" in os.environ:
        logger.warning(
            "We currently do not support logging version information inside a google"
            "colab notebook. This is something we are planning to do. "
            "If you have any questions, please reach out to support@dagworks.io"
            "and we'll try to help you as soon as possible."
        )
        return default

    commit = repo.head.commit
    try:
        repo_url = repo.remote().url
    except ValueError:
        # TODO: change this to point to our docs on what to do.
        repo_url = "Error: No repository to link to."
    return GitInfo(
        branch=repo.active_branch.name,
        commit_hash=commit.hexsha,
        committed=not repo.is_dirty(),
        repository=repo_url,
        local_repo_base_path=repo.working_dir,
    )


def filter_json_dict_to_serializable(
    dict_to_filter: Dict[str, Any], curr_result: Dict[str, Any] = None
):
    if curr_result is None:
        curr_result = {}
    if dict_to_filter is None:
        dict_to_filter = {}
    for key, value in dict_to_filter.items():
        try:
            json.dumps(value)
            curr_result[key] = value
        except TypeError:
            if isinstance(value, dict):
                new_result = {}
                filter_json_dict_to_serializable(value, new_result)
                curr_result[key] = new_result
            else:
                curr_result[key] = str(value)
    return curr_result


def validate_tags(tags: Any):
    """Validates that tags are a dictionary of strings to strings.

    :param tags: Tags to validate
    :raises ValueError: If tags are not a dictionary of strings to strings
    """
    if not isinstance(tags, dict):
        raise ValueError(f"Tags must be a dictionary, but got {tags}")
    for key, value in tags.items():
        if not isinstance(key, str):
            raise ValueError(f"Tag keys must be strings, but got {key}")
        if not isinstance(value, str):
            raise ValueError(f"Tag values must be strings, but got {value}")


def safe_len(x):
    return len(x) if x is not None else 0


class Driver(driver.Driver):
    def __init__(
        self,
        config: Dict[str, Any],
        *modules: ModuleType,
        project_id: int,
        api_key: str,
        username: str,
        dag_name: str,
        tags: Dict[str, str] = None,
        client_factory: Callable[
            [str, str, str], clients.DAGWorksClient
        ] = clients.BasicDAGWorksClient,
        adapter: base.HamiltonGraphAdapter = None,
        dagworks_api_url=os.environ.get("DAGWORKS_API_URL", constants.DAGWORKS_API_URL),
        dagworks_ui_url=constants.DAGWORKS_UI_URL,  # We may want to change this later for
        # on-prem deploys
    ):
        """Instantiates a DAGWorks driver. This:
        1. Requires a project to exist. Create one via https://app.dagworks.io/dashboard/projects.
        2. Sends over the shape of the DAG.
        3. Sets up execute() run-tracking.

        :param config: Configuration to use, same as standard Hamilton driver.
        :param modules: Modules to use, same as standard Hamilton driver.
        :param project_id: Identifier for the project to use to store this DAG under.
        :param api_key: API key to use for authentication. Remember not to save this in plaintext!
        :param username: email address to use for authentication.
        :param dag_name: name for this DAG. You will use this for top level curation of DAGs
        within a project.
        :param tags: Optional key value string pairs to help identify and curate this instance of
        the DAG and subsequent execution runs. E.g. {"environment": "production"}.
        Currently all .execute() runs will be tagged with these.
        :param client_factory: Optional. Advanced use. Factory to use to create the underlying
        client.
        :param adapter: Optional. Adapter to use, same as standard Hamilton driver.
        :param dagworks_api_url: Optional. URL to use for the DAGWorks API.
        :param dagworks_ui_url: Optional. URL to use for the DAGWorks UI.
        """
        super(Driver, self).__init__(config, *modules, adapter=adapter)
        if global_tracker.enabled:
            global_tracker.initialize(
                username,
                project=project_id,
                adapter=get_adapter_representation(self.adapter),
                dagworks_api_url=dagworks_api_url,
            )
        self.config = config
        self.project = project_id
        self.api_key = api_key
        self.username = username
        # TODO -- figure out how to pass any additional configuration to the client if needed
        self.client = client_factory(api_key, username, dagworks_api_url)
        self.module_hash = _get_modules_hash(modules)
        self.vcs_info = _derive_version_control_info(self.module_hash)
        self.initialized = False
        self.modules = modules
        self.project_version = None
        self.run_tags = tags if tags is not None else {}
        validate_tags(self.run_tags)
        self.dag_name = dag_name
        self.dagworks_ui_url = dagworks_ui_url
        # reassign the graph executor with all the information we have
        self.graph_executor = DAGWorksGraphExecutor(
            self.graph_executor,
            self.client,
            self.run_tags,
            self.dagworks_ui_url,
            self.project,
            self.vcs_info.local_repo_base_path,
            self.vcs_info,
            self.dag_name,
        )
        self.initialize()

    def set_name(self, new_name: str):
        """Sets a name for the driver. This allows you to force a change in the name/version of the
        DAG so the next run logs a new one.

        :param new_name:
        """
        self.dag_name = new_name
        self.graph_executor.dag_name = new_name

    @global_tracker.track_calls()
    def initialize(self):
        """Initializes the driver. This:
        1. Validates authentication
        2. Creates a project if it does not already exist
        3. Sets initialization as true

        Note this is idempotent -- it can be called by the user to test, but will get called when
        the driver runs.

        """
        logger.debug("Validating authentication against DAGWorks API...")
        self.client.validate_auth()
        logger.debug("Authentication successful!")
        logger.debug(f"Ensuring project {self.project} exists...")
        self.client.ensure_project_exists(self.project)
        self.initialized = True

    @global_tracker.track_calls(
        tracking_generators={
            "final_vars": [("num_vars", safe_len)],
            "overrides": [("num_overrides", safe_len)],
            "inputs": [("num_inputs", safe_len)],
        },
    )
    def execute(
        self,
        final_vars: List[Union[str, Callable]],
        overrides: Dict[str, Any] = None,
        display_graph: bool = False,
        inputs: Dict[str, Any] = None,
    ) -> Any:
        logger.warning(
            f"\nCapturing execution run. All runs for project can be found at "
            f"{self.dagworks_ui_url}/dashboard/project/{self.project}/runs"
        )
        return super(Driver, self).execute(final_vars, overrides, display_graph, inputs)

    @global_tracker.track_calls(
        tracking_generators={
            "final_vars": [("num_vars", safe_len)],
            "overrides": [("num_overrides", safe_len)],
            "inputs": [("num_inputs", safe_len)],
        },
    )
    def raw_execute(
        self,
        final_vars: List[str],
        overrides: Dict[str, Any] = None,
        display_graph: bool = False,
        inputs: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        return super(Driver, self).raw_execute(final_vars, overrides, display_graph, inputs)

    @global_tracker.track_calls(
        tracking_generators={
            "final_vars": [("num_vars", safe_len)],
            "overrides": [("num_overrides", safe_len)],
            "inputs": [("num_inputs", safe_len)],
            "materializers": [("num_materializers", safe_len)],
        },
    )
    def materialize(
        self,
        *materializers: materialization.MaterializerFactory,
        additional_vars: List[Union[str, Callable, Variable]] = None,
        overrides: Dict[str, Any] = None,
        inputs: Dict[str, Any] = None,
    ) -> Tuple[Any, Dict[str, Any]]:
        return super(Driver, self).materialize(
            *materializers, additional_vars=additional_vars, overrides=overrides, inputs=inputs
        )


class DAGWorksGraphExecutor(driver.GraphExecutor):
    def __init__(
        self,
        wrapping_executor: driver.GraphExecutor,
        client: clients.DAGWorksClient,
        run_tags: Dict[str, str],
        dagworks_ui_url: str,
        project_id: int,
        repo_base: str,
        vcs_info: GitInfo,
        dag_name: str,
    ):
        self.executor = wrapping_executor
        self.client = client
        self.run_tags = run_tags
        self.dagworks_ui_url = dagworks_ui_url
        self.project_id = project_id
        self.repo_base = repo_base
        self.vcs_info = vcs_info
        self.dag_name = dag_name

    def execute(
        self,
        fg: graph.FunctionGraph,
        final_vars: List[Union[str, Callable, Variable]],
        overrides: Dict[str, Any],
        inputs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Executes a graph in a blocking function.

        :param fg: Graph to execute
        :param final_vars: Variables we want
        :param overrides: Overrides --- these short-circuit computation
        :param inputs: Inputs to the Graph.
        :return: The output of the final variables, in dictionary form.
        """
        dag = parse_dag(fg, self.repo_base)
        logger.debug(f"Found a total of {len(dag.nodes)} nodes in DAG, saving...")
        project_version = self.client.register_project_version(
            self.project_id,
            self.vcs_info,
            dag=dag,
            name=self.dag_name,
            tags=self.run_tags,
        )
        run_id = str(uuid.uuid4())
        tracking_state = TrackingState(str(run_id))
        with monkey_patch_adapter(fg.adapter, tracking_state):
            tracking_state.clock_start()
            try:
                out = self.executor.execute(fg, final_vars, overrides, inputs)
                tracking_state.clock_end(status=Status.SUCCESS)
                return out
            except Exception as e:
                tracking_state.clock_end(status=Status.FAILURE)
                raise e
            finally:
                logged_run = self.client.log_dag_run(
                    tracking_state.get(),
                    project_version.id,
                    config=filter_json_dict_to_serializable(fg.config),
                    tags=self.run_tags,
                    inputs=filter_json_dict_to_serializable(inputs),
                    outputs=final_vars,
                )
                logger.warning(
                    f"\nCaptured execution run. Results can be found at "
                    f"{self.dagworks_ui_url}/dashboard/project/{self.project_id}/runs/{logged_run}\n"
                )

    def validate(self, nodes_to_execute: List[node.Node]):
        pass
