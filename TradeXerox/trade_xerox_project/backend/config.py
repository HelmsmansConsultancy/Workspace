"""
Application-wide configuration.
"""

from pathlib import Path

# ── Window ───────────────────────────────────────────────────────────────────
APP_TITLE     = "Trade Xerox"
WINDOW_WIDTH  = 1200
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

# ── XML parsing ───────────────────────────────────────────────────────────────
MAX_FILE_SIZE_MB = 10
MAX_DEPTH        = 8   # how deep to recurse into nested elements
