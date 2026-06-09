"""
api.py — pywebview JS API.

Every public method is callable from the frontend via
  window.pywebview.api.<method_name>(...)
All methods return JSON-serialisable dicts.
"""

from .xml_service import parse_xml, XmlServiceError


class XmlApi:
    """Exposes XML parsing to the web front-end."""

    def parse_xml(self, xml_text: str) -> dict:
        """
        Parse raw XML text sent from the frontend.

        Returns on success:
            {"ok": true, "entries": [{"key": "...", "value": "..."}, ...]}

        Returns on failure:
            {"ok": false, "error": "<human-readable message>"}
        """
        try:
            entries = parse_xml(xml_text)
            return {"ok": True, "entries": entries}
        except XmlServiceError as exc:
            return {"ok": False, "error": str(exc)}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": f"Unexpected error: {exc}"}
