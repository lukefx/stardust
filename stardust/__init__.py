import argparse
import sys

import uvicorn

from stardust.file_handler import handle
from stardust.stardust import Stardust


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        metavar="F",
        type=str,
        default="app.py",
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
        app, host="0.0.0.0", port=args.port, access_log=False, log_level="error"
    )


sys.exit(main())
