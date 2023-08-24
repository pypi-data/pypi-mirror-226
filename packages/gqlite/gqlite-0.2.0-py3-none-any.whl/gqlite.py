"""Lightweight GraphQL client."""

import os

import dotenv
import requests

dotenv.load_dotenv()


class Client:
    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.headers = {"Authorization": f"Bearer {token}"}

    def query(self, text: str) -> dict:
        response = requests.post(
            self.url,
            json={"query": text},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()


url = os.getenv("GQLITE_URL", "")
token = os.getenv("GQLITE_TOKEN", "")

client = Client(url=url, token=token)
query = client.query
