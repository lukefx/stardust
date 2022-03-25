import os
import sys
from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction, isbuiltin
from typing import Callable


def find_local_function(module, path) -> Callable:
    method = None
    file = os.path.basename(path)
    file_name, file_ext = os.path.splitext(file)

    # getmembers returns a list of tuples
    for name, item in getmembers(module):
        if (
            file_name != "__init__"
            # we want to catch only local functions, not imported ones
            and isfunction(item)
            and not isbuiltin(item)
            and os.path.samefile(item.__code__.co_filename, path)
        ) or (file_name == "__init__" and isfunction(item)):
            method = item

    return method


def handle(path: str):
    module_path = path

    if os.path.isdir(path):
        module_path = os.path.join(path, "__init__.py")

    if os.path.exists(module_path):
        module = SourceFileLoader("stardust.app", module_path).load_module()
    else:
        sys.stderr.write("No such file or directory.")
        exit(1)

    return find_local_function(module, module_path)
