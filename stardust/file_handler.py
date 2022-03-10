import os
from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction, isbuiltin
from typing import Callable


def find_local_function(module, file_path) -> Callable:
    method = None
    # getmembers returns a list of tuples
    for member in getmembers(module):
        name, item = member
        if (
            isfunction(item)
            and not isbuiltin(item)
            # we want to catch only local functions, not imported ones
            and os.path.samefile(item.__code__.co_filename, file_path)
        ):
            method = item

    return method


def handle(file_path: str):
    try:
        with open(file_path) as f:
            module = SourceFileLoader("stardust.app", file_path).load_module()

    except FileNotFoundError:
        print("No such file or directory.")
        exit(1)

    return find_local_function(module, file_path)
