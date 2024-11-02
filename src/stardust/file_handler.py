import importlib.util
import sys
from inspect import getmembers, isbuiltin, isfunction
from pathlib import Path
from typing import Callable


def find_local_function(module) -> Callable | None:
    # getmembers returns a list of tuples
    for name, item in getmembers(module):
        # Check if it's a function but not a builtin
        if isfunction(item) and not isbuiltin(item):
            # Check if function is defined in this module by comparing its code location
            # Also check if the function's module is the same or a submodule
            if hasattr(item, "__code__") and (
                item.__module__ == module.__name__
                or item.__module__.startswith(f"{module.__name__}.")
            ):
                return item

    # Nothing found
    return None


def load_module(module_name: str, path: str | Path):
    path = Path(path)

    # Handle directory case
    if path.is_dir():
        init_file = path / "__init__.py"
        if not init_file.is_file():
            raise FileNotFoundError(f"'{init_file}' does not exist")
        target_path = init_file
    # Handle file case
    elif path.is_file():
        target_path = path
    else:
        raise ValueError(f"Path '{path}' is neither a file nor directory")

    # Create a module spec from the location
    spec = importlib.util.spec_from_file_location(module_name, str(target_path))
    if spec is None:
        raise ImportError(f"Cannot find spec for module '{module_name}' at '{path}'")

    # Create and execute module
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def handle(path: str) -> Callable:
    module = load_module("stardust.app", path)
    return find_local_function(module)
