from setuptools import find_packages, setup

require = ["starlette==0.14.1", "uvicorn==0.12.2"]

setup(
    name="stardust",
    version="0.0.2",
    description="Stardust is micro web framework inspired by serveless and lambda deployments.",
    url="https://github.com/lukefx/stardust.git",
    author="Luca Simone",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    py_modules=["stardust"],
    scripts=["bin/stardust"],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "local"]
    ),
    include_package_data=True,
    install_requires=require,
)
