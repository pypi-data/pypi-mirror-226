"""Lightweight GraphQL client."""

import os

import dotenv
import requests

dotenv.load_dotenv()


class Client:
    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.headers = {"Authorization": f"Bearer {token}"}

    def post(self, query: str) -> dict:
        response = requests.post(
            self.url,
            json={"query": query},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()


url = os.getenv("GQLPY_URL", "")
token = os.getenv("GQLPY_TOKEN", "")

_inst = Client(url=url, token=token)

post = _inst.post
