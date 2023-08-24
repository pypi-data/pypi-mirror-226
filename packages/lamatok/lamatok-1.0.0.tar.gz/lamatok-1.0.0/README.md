# Lamatok client, for Python 3

[![Package](https://github.com/Lamadava/lamatok-python/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/Lamadava/lamatok-python/actions/workflows/python-package.yml)
![PyPI](https://img.shields.io/pypi/v/lamatok)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lamatok)

[![Downloads](https://pepy.tech/badge/lamatok)](https://pepy.tech/project/lamatok)
[![Downloads](https://pepy.tech/badge/lamatok/month)](https://pepy.tech/project/lamatok)
[![Downloads](https://pepy.tech/badge/lamatok/week)](https://pepy.tech/project/lamatok)


## Installation

```
pip install lamatok
```

## Usage

Create a token https://lamatok.com/tokens and copy "Access key"

```python
from lamatok import Client

cl = Client(token="<ACCESS_KEY>")
```

```python
from lamatok import AsyncClient

cl = AsyncClient(token="<ACCESS_KEY>")
```

## Run tests

```
LAMATOK_TOKEN=<token> pytest -v tests.py
```
