"""
Application-wide configuration.
All tunable values live here so the rest of the codebase stays free of
hard-coded strings and numbers.
"""

import os

# ── Window ──────────────────────────────────────────────────────────────────
APP_TITLE     = "Random Joke"
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480

# ── Paths ────────────────────────────────────────────────────────────────────
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(_BASE_DIR, "frontend")
HTML_PATH    = os.path.join(FRONTEND_DIR, "templates", "index.html")

# ── API ───────────────────────────────────────────────────────────────────────
JOKE_API_URL    = "https://official-joke-api.appspot.com/random_joke"
REQUEST_TIMEOUT = 10  # seconds
