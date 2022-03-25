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


### Response types

For a more complex response, where you would like to specify an HTTP status code or a custom media type, just use the
`send` method insted or returning a dict.

```python
from stardust.responses import send

async def serve(req):
    return send(
        content={"Hello": "World"}, 
        status_code=201, 
        media_type="application/vnd.stardust.api.v1+json"
    )
```

### Others return types

```python
from stardust.responses import send, json, text, stream, html, redirect, file

async def serve():
    # General method, automatically identifies the payload type
    return send({"Hello": "World"})

    # JSON
    return json({"Hello": "World"})

    # Plain text
    return text("Hello World")

    # Streaming content (requires a generator function)
    return stream(generator_fun)

    # Html content
    return html("<html><body>Hello World</body></html>")

    # Redirect to another location
    return redirect("https://www.google.com")

    # Returns a file
    return file(file_path)

```

### Apps with multiple files

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

#### Apps with different responses

```py
from stardust.responses import json

async def serve():
    return json(content={"hello":"world"}, status_code=200)
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