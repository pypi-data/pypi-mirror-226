# gqlite

Lightweight client for GraphQL in Python.

```bash
pip install gqlite
```

Set the two environment variables:

1. `GQLPY_URL` for the URL.
2. `GQLPY_TOKEN` for the authorization token.

You can also set these in `.env`.

Then:

```python
import gqlite

query: str = ... # your GraphQL query

json_response = gqlite.post(query)
```
