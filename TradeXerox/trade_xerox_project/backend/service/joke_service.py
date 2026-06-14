"""
joke_service.py — thin HTTP wrapper around the joke REST API.

Keeping network logic here (away from the pywebview Api class) makes it
straightforward to swap providers, add caching, or mock in tests.
"""

import json
import urllib.error
import urllib.request
from typing import TypedDict

from ..config import JOKE_API_URL, REQUEST_TIMEOUT


class JokeResult(TypedDict):
    setup: str
    punchline: str


class JokeServiceError(Exception):
    """Raised for any failure while fetching a joke."""


def fetch_joke() -> JokeResult:
    """
    Fetch one random joke from the upstream API.

    Returns:
        JokeResult with 'setup' and 'punchline' strings.

    Raises:
        JokeServiceError on network errors or unexpected response shapes.
    """
    try:
        req = urllib.request.Request(
            JOKE_API_URL,
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise JokeServiceError(f"Network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise JokeServiceError("Request timed out.") from exc

    try:
        data: dict = json.loads(raw)
        return JokeResult(setup=data["setup"], punchline=data["punchline"])
    except (json.JSONDecodeError, KeyError) as exc:
        raise JokeServiceError(f"Unexpected API response: {exc}") from exc
