/**
 * api.js — thin wrapper around window.pywebview.api
 *
 * Centralises all backend calls so ui.js never touches pywebview directly.
 * This makes it easy to mock the backend during browser-based development.
 */

const backendJokeApi = (() => {
  /**
   * Wait for pywebview to inject its JS bridge, then resolve.
   * @returns {Promise<object>} the pywebview api object
   */
  function _ready() {
    return new Promise((resolve) => {
        if (window.pywebview?.jokeApi) {
        resolve(window.pywebview.jokeApi);
        return;
      }
        window.addEventListener('pywebviewready', () => resolve(window.pywebview.jokeApi), { once: true });
    });
  }

  /**
   * Fetch one random joke from the Python backend.
   * @returns {Promise<{ok: boolean, setup?: string, punchline?: string, error?: string}>}
   */
  async function getJoke() {
      const jokeApi = await _ready();
      return jokeApi.get_joke();
  }

  return { getJoke };
})();
