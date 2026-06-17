# Joke Machine — pywebview demo

A minimal but properly structured desktop application built with Python and
[pywebview](https://pywebview.flowrl.com/). Fetches random jokes from the
[Official Joke API](https://official-joke-api.appspot.com/) and displays them
in a native desktop window.

---

## Project structure

```
joke_app/
│
├── main.py                        # Entry point — creates the webview window
│
├── requirements.txt
│
├── backend/                       # Pure Python; no DOM knowledge here
│   ├── __init__.py
│   ├── config.py                  # App-wide constants (URLs, window size …)
│   ├── joke_service.py            # HTTP logic; fetches & parses the API
│   └── api.py                     # pywebview JS API class (JokeApi)
│
└── frontend/                      # Everything rendered inside the webview
    ├── templates/
    │   └── index.html             # Single HTML page
    └── static/
        ├── css/
        │   └── main.css           # All styles
        └── js/
            ├── api.js             # Thin JS wrapper around window.pywebview.api
            └── ui.js              # DOM manipulation & user interaction
```

### Layer responsibilities

| Layer | File(s) | Knows about |
|---|---|---|
| Entry point | `main.py` | Config + Api class + webview |
| Config | `backend/config.py` | Constants only |
| Service | `backend/joke_service.py` | HTTP + JSON parsing |
| JS API | `backend/api.py` | Service layer; returns plain dicts |
| HTML | `frontend/templates/index.html` | Structure only |
| Styles | `frontend/static/css/main.css` | Presentation only |
| JS bridge | `frontend/static/js/api.js` | pywebview bridge |
| JS UI | `frontend/static/js/ui.js` | DOM + calls api.js |

---

## Getting started

```bash
# 0. Create the virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 1. Install dependency
pip install -r requirements.txt

# 2. Run
python main.py

# 3. To find out more versions to install
pip index versions library


```

> **Platform note:** pywebview uses the OS's built-in web renderer
> (WebKit on macOS/Linux, WebView2 on Windows). On Linux you may also need
> `python3-gi`, `gir1.2-webkit2-4.0`, and `libgtk-3-dev`.
