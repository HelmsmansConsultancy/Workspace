/**
 * api.js — thin wrapper around window.pywebview.api
 *
 * Centralises all backend calls so ui.js never touches pywebview directly.
 * This makes it easy to mock the backend during browser-based development.
 */

const backendApi = (() => {
    /**
     * Wait for pywebview to inject its JS bridge, then resolve.
     * @returns {Promise<object>} the pywebview api object
     */
    function _ready() {
        return new Promise((resolve) => {
            if (window.pywebview?.api) {
                resolve(window.pywebview.api);
                return;
            }
            window.addEventListener('pywebviewready', () => resolve(window.pywebview.api), { once: true });
        });
    }

    async function connectToMt5(pathToExecutable) {
        const api = await _ready();
        return api.connect(pathToExecutable);
    }

    /**
     * Send raw XML text to the Python backend for parsing.
     * @param {string} xmlText
     * @returns {Promise<{ok: boolean, entries?: Array<{key:string,value:string}>, error?: string}>}
     */
    async function parseXml(xmlText) {
        const api = await _ready();
        return api.parse_xml(xmlText);
    }

    async function select_and_parse_xml() {
        const api = await _ready();
        return api.select_and_parse_xml();
    }

    return { parseXml, select_and_parse_xml, connectToMt5 };
})();
