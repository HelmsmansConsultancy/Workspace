"""
api.py — the pywebview JS API.

Every public method on JokeApi is callable from the frontend via
  window.pywebview.api.<method_name>(...)
Methods must return JSON-serialisable values (dict, list, str, int, None).
"""
import os
import xml.etree.ElementTree as ET
from .joke_api import JokeApi
from .xml_api import XmlApi
import webview
from rich.console import Console

console = Console()

jokeApi = JokeApi()  # noqa: N816
xmlApi = XmlApi()    # noqa: N816   

class Api:
    """Exposes backend functionality to the web front-end."""
    def __init__(self):
        self.window = None


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
    


    def element_to_dict(self, element):
        """Recursively convert an XML Element into a JSON-serializable dict."""
        node = {
            "tag": element.tag,
            "attributes": dict(element.attrib),
            "text": (element.text or "").strip(),
            "children": [self.element_to_dict(child) for child in element]
        }
        return node
    

    def select_and_parse_xml(self):
        """Open a file dialog restricted to XML files, parse the chosen file
        and return its structure as a nested dict, or an error dict."""
        file_types = ('XML Files (*.xml)',)

        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            directory=os.getcwd(),
            allow_multiple=False,
            file_types=file_types
        )

        if not result:
            return {"success": False, "error": "No file selected"}

        file_path = result[0]

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = self.element_to_dict(root)
            result = {
                "success": True,
                "filename": os.path.basename(file_path),
                "tree": data
            }
            ##console.print(result)
            return result
        except ET.ParseError as e:
            return {"success": False, "error": f"Failed to parse XML: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to read file: {e}"}
