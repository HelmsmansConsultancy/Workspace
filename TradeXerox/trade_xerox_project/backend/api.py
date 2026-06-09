"""
api.py — the pywebview JS API.

Every public method on JokeApi is callable from the frontend via
  window.pywebview.api.<method_name>(...)
Methods must return JSON-serialisable values (dict, list, str, int, None).
"""

from .joke_api import JokeApi
from .xml_api import XmlApi


jokeApi = JokeApi()  # noqa: N816
xmlApi = XmlApi()    # noqa: N816   

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

    

    def parse_xml(self, xml_text: str) -> dict:
        """
        Parse raw XML text sent from the frontend.

        Returns on success:
            {"ok": true, "entries": [{"key": "...", "value": "..."}, ...]}

        Returns on failure:
            {"ok": false, "error": "<human-readable message>"}
        """
        return xmlApi.parse_xml(xml_text)
