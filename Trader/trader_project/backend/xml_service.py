"""
xml_service.py — XML parsing logic.

Accepts raw XML text, walks the element tree, and returns a flat list of
key-value pairs suitable for display.  Nesting is shown via dot-notation keys
(e.g. "catalog.book.title").  Attributes are included as key@attr notation.

Keeping all parsing logic here (away from the Api class) makes it easy
to unit-test and swap out independently.
"""

import xml.etree.ElementTree as ET
from typing import TypedDict

from .config import MAX_DEPTH, MAX_FILE_SIZE_MB


class KVEntry(TypedDict):
    key: str
    value: str


class XmlServiceError(Exception):
    """Raised for any failure while parsing XML."""


def _clean_tag(tag: str) -> str:
    """Strip namespace URI from a tag, e.g. '{http://…}name' → 'name'."""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def _walk(element: ET.Element, prefix: str, depth: int, results: list[KVEntry]) -> None:
    """Recursively walk the element tree and append KVEntry items."""
    if depth > MAX_DEPTH:
        results.append(KVEntry(key=prefix + "…", value="(max depth reached)"))
        return

    tag = _clean_tag(element.tag)
    key = f"{prefix}.{tag}" if prefix else tag

    # Attributes
    for attr_name, attr_value in element.attrib.items():
        results.append(KVEntry(key=f"{key}@{_clean_tag(attr_name)}", value=attr_value))

    text = (element.text or "").strip()
    children = list(element)

    if text and not children:
        # Leaf node — the text content is the value
        results.append(KVEntry(key=key, value=text))
    elif not children and not text:
        # Empty element
        results.append(KVEntry(key=key, value="(empty)"))
    else:
        # Branch node — recurse; track sibling indices for repeated tags
        tag_counts: dict[str, int] = {}
        for child in children:
            child_tag = _clean_tag(child.tag)
            tag_counts[child_tag] = tag_counts.get(child_tag, 0) + 1

        tag_seen: dict[str, int] = {}
        for child in children:
            child_tag = _clean_tag(child.tag)
            if tag_counts[child_tag] > 1:
                idx = tag_seen.get(child_tag, 0)
                tag_seen[child_tag] = idx + 1
                child_prefix = f"{key}.{child_tag}[{idx}]" if prefix else f"{key}[{idx}]"
                # Pass key as the prefix so the child tag is not duplicated
                _walk_with_key(child, child_prefix, depth + 1, results)
            else:
                _walk(child, key, depth + 1, results)


def _walk_with_key(element: ET.Element, forced_key: str, depth: int, results: list[KVEntry]) -> None:
    """Like _walk but the full key for this element is already known."""
    if depth > MAX_DEPTH:
        results.append(KVEntry(key=forced_key + "…", value="(max depth reached)"))
        return

    for attr_name, attr_value in element.attrib.items():
        results.append(KVEntry(key=f"{forced_key}@{_clean_tag(attr_name)}", value=attr_value))

    text = (element.text or "").strip()
    children = list(element)

    if text and not children:
        results.append(KVEntry(key=forced_key, value=text))
    elif not children and not text:
        results.append(KVEntry(key=forced_key, value="(empty)"))
    else:
        tag_counts: dict[str, int] = {}
        for child in children:
            child_tag = _clean_tag(child.tag)
            tag_counts[child_tag] = tag_counts.get(child_tag, 0) + 1

        tag_seen: dict[str, int] = {}
        for child in children:
            child_tag = _clean_tag(child.tag)
            if tag_counts[child_tag] > 1:
                idx = tag_seen.get(child_tag, 0)
                tag_seen[child_tag] = idx + 1
                child_key = f"{forced_key}.{child_tag}[{idx}]"
                _walk_with_key(child, child_key, depth + 1, results)
            else:
                _walk(child, forced_key, depth + 1, results)


def parse_xml(xml_text: str) -> list[KVEntry]:
    """
    Parse XML text and return a flat list of KVEntry dicts.

    Args:
        xml_text: Raw XML string.

    Returns:
        List of {"key": "...", "value": "..."} dicts.

    Raises:
        XmlServiceError on oversized input or malformed XML.
    """
    size_mb = len(xml_text.encode("utf-8")) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise XmlServiceError(
            f"File is {size_mb:.1f} MB — limit is {MAX_FILE_SIZE_MB} MB."
        )

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise XmlServiceError(f"Invalid XML: {exc}") from exc

    results: list[KVEntry] = []
    _walk(root, "", 0, results)
    return results
