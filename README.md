# Stardust

Micro framework inspired by the simple lambda or serveless deployment.

Usage:

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

### Contributing

Clone the project, install all the dependencies with:

```bash
$ pipenv install
```

Linting:

```bash
$ pipenv run lint
```