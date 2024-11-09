# Stardust 🌟

[![PyPI version](https://badge.fury.io/py/stardust.svg)](https://badge.fury.io/py/stardust)
[![Python Versions](https://img.shields.io/pypi/pyversions/stardust.svg)](https://pypi.org/project/stardust/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A micro web framework inspired by serverless and lambda deployments, designed for simplicity and efficiency.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install Stardust using pip:

```bash
pip install stardust
```

Requires Python 3.10 or higher.

## Quick Start

Create a simple API in seconds with `app.py`:

```python
async def serve(req):
    return {"hello": "world"}
```

Run your application:

```bash
stardust app.py
```

Your API will be available at `http://localhost:8000`

## Features

- 🚀 **Minimal Setup**: Create APIs with just a single function
- 🛠 **Modern Python**: Built for Python 3.10+ with full async support
- 🔌 **CORS Enabled**: Built-in CORS middleware for web applications
- ⚡ **Fast**: Powered by Starlette and Uvicorn
- 🧩 **Flexible Responses**: Support for JSON, Plain Text, and custom Response objects
- 🔍 **Developer Friendly**: Debug mode and customizable logging

## Usage Examples

### JSON Response

```python
async def serve(req):
    return {"message": "Hello, World!"}
```

### Plain Text Response

```python
from starlette.responses import PlainTextResponse

async def serve(req):
    return PlainTextResponse("Hello, World!")
```

### Query Parameters

```python
async def serve(req):
    name = req.query_params.get("name", "world")
    return {"hello": name}
```

### POST Request Handler

```python
async def serve(req):
    body = await req.json()
    return body  # Echo back the request body
```

### Custom Status Codes

```python
from starlette.responses import Response

async def serve(req):
    return Response(status_code=204)
```

## Command Line Options

```bash
stardust [options] [file]

Options:
  --port PORT        Port number (default: 8000)
  --host HOST        Host address (default: 0.0.0.0)
  --log-level LEVEL  Logging level (default: error)
  --debug           Enable debug mode
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/lukefx/stardust
cd stardust

# Install development dependencies
uv sync --all-extras --dev

# Run tests
uv run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Built with:
- [Starlette](https://www.starlette.io/)
- [Uvicorn](https://www.uvicorn.org/)

---

Created by [Luca Simone](mailto:info@lucasimone.info)
