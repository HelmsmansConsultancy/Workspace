"""
Application-wide configuration.
"""

from pathlib import Path

# ── Window ───────────────────────────────────────────────────────────────────
APP_TITLE     = "Random Joke"
WINDOW_WIDTH  = 1000
WINDOW_HEIGHT = 1000

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

# ── XML parsing ───────────────────────────────────────────────────────────────
MAX_FILE_SIZE_MB = 10
MAX_DEPTH        = 8   # how deep to recurse into nested elements
