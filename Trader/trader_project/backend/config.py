"""
Application-wide configuration.
"""

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

HTML_PATH   = TEMPLATE_DIR / "index.html"
CSS_PATH    = STATIC_DIR   / "css"  / "main.css"
JS_API_PATH = STATIC_DIR   / "js"   / "api.js"
JS_UI_PATH  = STATIC_DIR   / "js"   / "ui.js"

# ── Joke API ──────────────────────────────────────────────────────────────────
JOKE_API_URL    = "https://official-joke-api.appspot.com/random_joke"
REQUEST_TIMEOUT = 10  # seconds
