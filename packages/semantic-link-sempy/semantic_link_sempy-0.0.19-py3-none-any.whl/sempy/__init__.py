from . import _version
from .fabric._environment import _get_environment, get_notebook_workspace_id, _on_fabric
from ._utils._log import _initialize_log


__version__ = _version.get_versions()['version']

_initialize_log(
    _on_fabric(),
    _get_environment(),
    get_notebook_workspace_id()
)
