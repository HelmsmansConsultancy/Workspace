"""
api.py — the pywebview JS API.

Every public method on JokeApi is callable from the frontend via
  window.pywebview.api.<method_name>(...)
Methods must return JSON-serialisable values (dict, list, str, int, None).
"""

from ..service.joke_service import fetch_joke, JokeServiceError


class JokeApi:
    """Exposes backend functionality to the web front-end."""

    def get_joke(self) -> dict:
        """
        Fetch a random joke and return it as a plain dict.

        Returns on success:
            {"ok": true, "setup": "...", "punchline": "..."}

        Returns on failure:
            {"ok": false, "error": "<human-readable message>"}
        """
        try:
            joke = fetch_joke()
            return {"ok": True, "setup": joke["setup"], "punchline": joke["punchline"]}
        except JokeServiceError as exc:
            return {"ok": False, "error": str(exc)}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": f"Unexpected error: {exc}"}
