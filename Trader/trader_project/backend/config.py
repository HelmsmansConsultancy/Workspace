"""
Application-wide configuration.
All tunable values live here so the rest of the codebase stays free of
hard-coded strings and numbers.
"""

import os
from pathlib import Path

# ── Window ───────────────────────────────────────────────────────────────────
APP_TITLE     = "Random Joke"
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR   = FRONTEND_DIR / "static"
TEMPLATE_DIR = FRONTEND_DIR / "templates"
HTML_PATH    = TEMPLATE_DIR / "index.html"

# file:// URIs for static assets (needed when loading HTML from disk)
CSS_URI = STATIC_DIR.joinpath("css", "main.css").as_uri()
JS_API_URI = STATIC_DIR.joinpath("js", "api.js").as_uri()
JS_UI_URI  = STATIC_DIR.joinpath("js", "ui.js").as_uri()

# ── Joke API ──────────────────────────────────────────────────────────────────
JOKE_API_URL    = "https://official-joke-api.appspot.com/random_joke"
REQUEST_TIMEOUT = 10  # seconds
