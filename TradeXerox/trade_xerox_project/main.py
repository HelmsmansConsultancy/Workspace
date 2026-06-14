"""
joke_app — entry point
Run:  python main.py

Asset loading strategy
──────────────────────
pywebview's html= mode has no base URL, so browsers block external
file:// loads for <link> and <script src>.  We therefore read each
asset from disk at startup and inline it directly into the HTML string.
The file structure (separate CSS / JS files) is preserved for development;
main.py is the only place that knows about the assembly.
"""

import webview
from backend.api.api import Api
from backend.config import (
    APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    HTML_PATH, CSS_PATH, JS_API_PATH, JS_UI_PATH,
)


def build_html() -> str:
    """Inline CSS and JS into the HTML template and return the full string."""
    css    = CSS_PATH.read_text(encoding="utf-8")
    js_api = JS_API_PATH.read_text(encoding="utf-8")
    js_ui  = JS_UI_PATH.read_text(encoding="utf-8")
    html   = HTML_PATH.read_text(encoding="utf-8")

    html = html.replace("__INLINE_CSS__",    f"<style>\n{css}\n</style>")
    html = html.replace("__INLINE_JS_API__", f"<script>\n{js_api}\n</script>")
    html = html.replace("__INLINE_JS_UI__",  f"<script>\n{js_ui}\n</script>")
    return html


def main() -> None:
    api = Api()

    webview.create_window(
        title=APP_TITLE,
        html=build_html(),
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        min_size=(400, 360),
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
