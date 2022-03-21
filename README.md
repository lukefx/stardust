# Stardust

Micro framework inspired by the simple lambda or serveless deployment.

### Usage:

```sh
$ pip install stardust
```

Create a file with a coroutine function that returns a dict, for example `app.py`:
```python
async def serve(req):
    return {
      'hello': 'world'
    }
```

Now just start the framework, nothing more to do...
```sh
$ stardust app.py
```

You're up and running! 🎉

### More complex cases

For more complex cases or apps that are not just one function, Stardust is also able to use a module as starting point.

Create a Python module:

```sh
$ tree example_module
example_module
├── __init__.py
└── app.py
```

Let's assume app is a complex app with many functions, you can find an example into the `examples` folder.
The module should export only the main function that Stardust will use as entrypoint:

```python
from .app import serve
```

And specify the module folder instead of a file:

```sh
$ stardust ./example_module
```

### Contributing

Clone the project, install all the dependencies with:

```bash
$ pipenv install
```

Linting:

```bash
$ pipenv run lint
```