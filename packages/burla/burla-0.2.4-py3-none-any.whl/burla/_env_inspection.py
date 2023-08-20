import subprocess
import warnings
import json
import builtins
from unittest.mock import MagicMock

import dill

from burla._helpers import nopath_warning

warnings.formatwarning = nopath_warning


class EnvironmentInspectionError(Exception):
    def __init__(self, stdout):
        super().__init__(
            (
                "The following error occurred attempting to get list if packages to install in "
                f"remove execution environment's: {stdout}"
            )
        )


def get_pip_packages():
    result = subprocess.run(
        ["pip", "list", "--format=json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.returncode != 0:
        raise EnvironmentInspectionError(result.stderr)

    for pkg in json.loads(result.stdout):
        if "+" in pkg["version"]:
            pkg["version"] = pkg["version"].split("+")[0]
        if not pkg.get("editable_project_location"):
            yield pkg


def get_imported_modules(pickled_function):
    """Returns modules that will be imported when pickled_function is unpickled"""
    imported_modules = []

    def mock_import(name, *a, **kw):
        imported_modules.append(name)
        return MagicMock()

    original_import = builtins.__import__
    builtins.__import__ = mock_import

    dill.loads(pickled_function)

    builtins.__import__ = original_import

    imported_modules = [module for module in imported_modules if not module.startswith("dill")]
    return imported_modules
