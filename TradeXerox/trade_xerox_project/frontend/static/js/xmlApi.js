/**
 * api.js — thin wrapper around window.pywebview.api
 *
 * Centralises all backend calls so ui.js never touches pywebview directly.
 * This makes it easy to mock the backend during browser-based development.
 */

const backendXmlApi = (() => {
  /**
   * Wait for pywebview to inject its JS bridge, then resolve.
   * @returns {Promise<object>} the pywebview api object
   */
  function _ready() {
    return new Promise((resolve) => {
      if (window.pywebview?.xmlApi) {
          resolve(window.pywebview.xmlApi);
        return;
      }
        window.addEventListener('pywebviewready', () => resolve(window.pywebview.xmlApi), { once: true });
    });
  }

    /**
     * Send raw XML text to the Python backend for parsing.
     * @param {string} xmlText
     * @returns {Promise<{ok: boolean, entries?: Array<{key:string,value:string}>, error?: string}>}
     */
    async function parseXml(xmlText) {
        const xmlApi = await _ready();
        return xmlApi.parse_xml(xmlText);
    }

    return { parseXml };
})();
