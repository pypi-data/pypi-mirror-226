# gqlite

Simple client for querying GraphQL from Python using
[`requests`](https://requests.readthedocs.io/en/latest/).

## Installation

```bash
pip install gqlite
```

## Usage

First set the two environment variables `GQLITE_URL` and `GQLITE_TOKEN`.
You can also use a `.env` file for these. Then:

```python
import gqlite

text = """
  hero {
    name
  }
}
"""
gqlite.query(text)  # returns a dict

```
