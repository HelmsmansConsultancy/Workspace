import webview
import urllib.request
import json


class Api:
    def get_joke(self):
        try:
            url = "https://official-joke-api.appspot.com/random_joke"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
            return {"setup": data["setup"], "punchline": data["punchline"]}
        except Exception as e:
            return {"error": str(e)}


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Random Joke</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      padding-top: 80px;
      background: #f0f4f8;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #2d3748;
    }

    #btn {
      padding: 14px 36px;
      font-size: 1rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      background: #4f46e5;
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
      box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
    }

    #btn:hover  { background: #4338ca; }
    #btn:active { transform: scale(0.97); }
    #btn:disabled { background: #a5b4fc; cursor: not-allowed; }

    #joke-box {
      margin-top: 40px;
      width: min(520px, 90vw);
      text-align: center;
    }

    #setup {
      font-size: 1.15rem;
      font-weight: 500;
      line-height: 1.6;
      min-height: 1.6em;
    }

    #punchline {
      margin-top: 18px;
      font-size: 1.05rem;
      font-style: italic;
      color: #4f46e5;
      min-height: 1.6em;
      opacity: 0;
      transition: opacity 0.5s ease 0.3s;
    }

    #punchline.visible { opacity: 1; }

    #error {
      margin-top: 20px;
      color: #e53e3e;
      font-size: 0.9rem;
    }

    .spinner {
      display: inline-block;
      width: 18px; height: 18px;
      border: 3px solid #fff;
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      vertical-align: middle;
      margin-right: 8px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <button id="btn" onclick="fetchJoke()">🎲 Tell me a joke</button>

  <div id="joke-box">
    <p id="setup"></p>
    <p id="punchline"></p>
    <p id="error"></p>
  </div>

  <script>
    async function fetchJoke() {
      const btn       = document.getElementById('btn');
      const setupEl   = document.getElementById('setup');
      const punchEl   = document.getElementById('punchline');
      const errorEl   = document.getElementById('error');

      // Reset
      setupEl.textContent   = '';
      punchEl.textContent   = '';
      punchEl.classList.remove('visible');
      errorEl.textContent   = '';
      btn.disabled          = true;
      btn.innerHTML         = '<span class="spinner"></span>Loading…';

      try {
        const result = await window.pywebview.api.get_joke();

        if (result.error) {
          errorEl.textContent = '⚠ ' + result.error;
        } else {
          setupEl.textContent = result.setup;
          // Delay punchline reveal for comedic effect
          setTimeout(() => {
            punchEl.textContent = result.punchline;
            punchEl.classList.add('visible');
          }, 800);
        }
      } catch (e) {
        errorEl.textContent = '⚠ Could not reach the backend.';
      } finally {
        btn.disabled     = false;
        btn.innerHTML    = '🎲 Tell me a joke';
      }
    }
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    api = Api()
    window = webview.create_window(
        title="Random Joke",
        html=HTML,
        js_api=api,
        width=620,
        height=460,
        resizable=True,
    )
    webview.start()