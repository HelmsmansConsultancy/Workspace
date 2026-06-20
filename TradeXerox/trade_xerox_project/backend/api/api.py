"""
api.py — the pywebview JS API.

Every public method on JokeApi is callable from the frontend via
  window.pywebview.api.<method_name>(...)
Methods must return JSON-serialisable values (dict, list, str, int, None).
"""
import os
import xml.etree.ElementTree as ET

from backend.service.mt5_service import Mt5Service
from .xml_api import XmlApi
from webview import FileDialog
from backend.service.singleton_service import SingletonService
from rich.console import Console

console = Console()

xmlApi = XmlApi()    # noqa: N816   
mt5Service = Mt5Service()  # noqa: N816

class Api:
    """Exposes backend functionality to the web front-end."""
    def __init__(self):
        console.print("__init__")
        self.window = None


    def connectToMt5(self, path_to_executable):
        console.print("connect" + path_to_executable)
        return mt5Service.connect(path_to_executable)
    


    def parse_xml(self, xml_text: str) -> dict:
        console.print("parse_xml")
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
        console.print("select_and_parse_xml")
        """Open a file dialog restricted to XML files, parse the chosen file
        and return its structure as a nested dict, or an error dict."""
        file_types = ('XML Files (*.xml)',)

        currentDirectory = os.getcwd()
        console.print(currentDirectory)
        console.print('SingletonService().get("window")')

        # Note: pywebview's file dialog API changed in version 3.0.0, so the old
        # webview.open_file_dialog(...) is now:
        # webview.OPEN_DIALOG → webview.FileDialog.OPEN
        # webview.FOLDER_DIALOG → webview.FileDialog.FOLDER
        # webview.SAVE_DIALOG → webview.FileDialog.SAVE
        result = SingletonService().get("window").create_file_dialog(
            FileDialog.OPEN,
            directory=currentDirectory,
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
