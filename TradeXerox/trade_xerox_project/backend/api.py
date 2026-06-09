"""
api.py — the pywebview JS API.

Every public method on JokeApi is callable from the frontend via
  window.pywebview.api.<method_name>(...)
Methods must return JSON-serialisable values (dict, list, str, int, None).
"""

from .joke_api import JokeApi

jokeApi = JokeApi()  # noqa: N816

class Api:
    """Exposes backend functionality to the web front-end."""

    def get_joke(self) -> dict:
        """
        Fetch a random joke and return it as a plain dict.

        Returns on success:
            {"ok": true, "setup": "...", "punchline": "..."}

        Returns on failure:
            {"ok": false, "error": "<human-readable message>"}
        """
        return jokeApi.get_joke()
