"""
joke_app — entry point
Run:  python main.py
"""

import webview
from backend.api import JokeApi
from backend.config import (
    APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    HTML_PATH, CSS_URI, JS_API_URI, JS_UI_URI,
)


def load_html() -> str:
    """
    Read index.html and replace placeholder tokens with absolute file:// URIs
    so pywebview can resolve CSS and JS regardless of working directory.
    """
    html = HTML_PATH.read_text(encoding="utf-8")
    html = html.replace("__CSS_URI__",    CSS_URI)
    html = html.replace("__JS_API_URI__", JS_API_URI)
    html = html.replace("__JS_UI_URI__",  JS_UI_URI)
    return html


def main() -> None:
    api = JokeApi()

    window = webview.create_window(
        title=APP_TITLE,
        html=load_html(),        # pass resolved HTML string, not a file URL
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        min_size=(400, 360),
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
