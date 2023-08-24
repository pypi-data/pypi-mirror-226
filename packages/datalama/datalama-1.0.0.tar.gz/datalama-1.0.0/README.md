# Datalama client, for Python 3

[![Package](https://github.com/Lamadava/datalama-python/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/Lamadava/datalama-python/actions/workflows/python-package.yml)
![PyPI](https://img.shields.io/pypi/v/datalama)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datalama)

[![Downloads](https://pepy.tech/badge/datalama)](https://pepy.tech/project/datalama)
[![Downloads](https://pepy.tech/badge/datalama/month)](https://pepy.tech/project/datalama)
[![Downloads](https://pepy.tech/badge/datalama/week)](https://pepy.tech/project/datalama)


## Installation

```
pip install datalama
```

## Usage

Create a token https://datalama.io/tokens and copy "Access key"

```python
from datalama import Client

cl = Client(token="<ACCESS_KEY>")
```

```python
from datalama import AsyncClient

cl = AsyncClient(token="<ACCESS_KEY>")
```

## Run tests

```
DATALAMA_TOKEN=<token> pytest -v tests.py
```
