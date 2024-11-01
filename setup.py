import os
from pathlib import Path

from setuptools import find_packages, setup

require = ["starlette==0.41.2", "uvicorn==0.32.0"]

THIS_DIR = Path(__file__).parent.resolve()
with open(os.path.join(THIS_DIR, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="stardust",
    version="0.0.5",
    description="Stardust is micro web framework inspired by serverless and lambda deployments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukefx/stardust.git",
    author="Luca Simone",
    author_email="info@lucasimone.info",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    py_modules=["stardust"],
    scripts=["bin/stardust"],
    packages=find_packages(
        exclude=["examples", "*.tests", "*.tests.*", "tests.*", "tests", "local"]
    ),
    include_package_data=True,
    install_requires=require,
)
