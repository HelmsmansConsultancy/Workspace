"""
joke_app — entry point
Run:  python main.py
"""

import webview
from backend.api import JokeApi
from backend.config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, HTML_PATH


def main() -> None:
    api = JokeApi()

    window = webview.create_window(
        title=APP_TITLE,
        url=HTML_PATH,
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        min_size=(400, 360),
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
