/**
 * ui.js — DOM manipulation and user interaction logic.
 *
 * Depends on api.js being loaded first (backendApi must be in scope).
 * All direct getElementById / classList calls live here; api.js stays
 * free of any DOM knowledge.
 */

const ui = (() => {
    // ── Element refs ────────────────────────────────────────────────────────
    const btn = document.getElementById('btn');
    const setupEl = document.getElementById('setup');
    const punchEl = document.getElementById('punchline');
    const errorEl = document.getElementById('error');

    // ── Private helpers ──────────────────────────────────────────────────────
    function _setLoading(isLoading) {
        btn.disabled = isLoading;
        btn.innerHTML = isLoading
            ? '<span class="spinner"></span>Fetching…'
            : 'Tell me a joke';
    }

    function _clearJoke() {
        setupEl.textContent = '';
        punchEl.textContent = '';
        punchEl.classList.remove('visible');
        errorEl.textContent = '';
    }

    function _showError(message) {
        errorEl.textContent = `⚠ ${message}`;
    }

    function _showJoke(setup, punchline) {
        setupEl.textContent = setup;
        // Slight delay so the punchline feels earned
        setTimeout(() => {
            punchEl.textContent = punchline;
            punchEl.classList.add('visible');
        }, 750);
    }

    // ── Public API ───────────────────────────────────────────────────────────
    async function fetchJoke() {
        _clearJoke();
        _setLoading(true);

        try {
            const result = await backendApi.getJoke();

            if (result.ok) {
                _showJoke(result.setup, result.punchline);
            } else {
                _showError(result.error ?? 'Something went wrong.');
            }
        } catch (err) {
            _showError('Could not reach the backend.');
            console.error('[ui] fetchJoke error:', err);
        } finally {
            _setLoading(false);
        }
    }

    return { fetchJoke };
})();
