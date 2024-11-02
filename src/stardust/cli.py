import argparse

import uvicorn

from .file_handler import handle
from .stardust import Stardust


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="?",
        default="app.py",
        help="Python file or directory with at least one async function that returns a string, object or Response.",
    )

    parser.add_argument(
        "--file",
        dest="file",
        help="Python file or directory with at least one async function that returns a string, object or Response.",
    )

    parser.add_argument(
        "--port",
        metavar="P",
        type=int,
        default=8000,
        help="Port number where the framework will listen for incoming requests.",
    )

    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address to bind the server to.",
    )
    parser.add_argument(
        "--log-level",
        choices=["critical", "error", "warning", "info", "debug"],
        default="error",
        help="Logging level for the server.",
    )

    parser.add_argument(
        "--debug",
        metavar="D",
        type=bool,
        default=False,
        help="Enable debug option.",
    )

    args = parser.parse_args()
    fun = handle(args.file)
    app = Stardust(fun=fun, port=args.port, debug=args.debug).build()
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        access_log=args.debug,
        log_level=args.log_level,
    )
