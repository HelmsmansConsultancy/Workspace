/**
 * ui.js — DOM manipulation and user interaction logic.
 *
 * Depends on api.js being loaded first (backendApi must be in scope).
 * All direct getElementById / classList calls live here; api.js stays
 * free of any DOM knowledge.
 */

const ui = (() => {
    // ── Element refs ────────────────────────────────────────────────────────
    const configButton = document.getElementById('config');
    const filenameSpan = document.getElementById('filename');
    const messageDiv = document.getElementById('message');
    const treeContainer = document.getElementById('tree-container');

    configButton.addEventListener('click', async () => {
        showMessage('', '');
        const response = await window.pywebview.api.select_and_parse_xml();

        if (!response.success) {
            showMessage(response.error, 'error');
            return;
        }

        filenameSpan.textContent = response.filename;
        showMessage('File loaded successfully.', 'info');
        renderTree(response.tree);
    });

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.className = 'message' + (type ? ' ' + type : '');
    }

    function renderTree(rootNode) {
        treeContainer.innerHTML = '';
        const rootElement = buildNode(rootNode);
        treeContainer.appendChild(rootElement);
    }

    function buildNode(node) {
        const wrapper = document.createElement('div');
        wrapper.className = 'tree-node';

        const hasChildren = node.children && node.children.length > 0;

        const content = document.createElement('div');
        content.className = 'tree-node-content' + (hasChildren ? ' has-children' : '');

        const toggle = document.createElement('span');
        toggle.className = 'toggle' + (hasChildren ? '' : ' leaf');
        toggle.textContent = hasChildren ? '▶' : '';
        content.appendChild(toggle);

        const tagSpan = document.createElement('span');
        tagSpan.className = 'tag-name';
        tagSpan.textContent = '<' + node.tag + '>';
        content.appendChild(tagSpan);

        if (node.attributes && Object.keys(node.attributes).length > 0) {
            const attrSpan = document.createElement('span');
            attrSpan.className = 'attributes';
            attrSpan.appendChild(document.createTextNode('['));
            Object.entries(node.attributes).forEach(([key, value], index) => {
                if (index > 0) {
                    attrSpan.appendChild(document.createTextNode(', '));
                }
                const attrName = document.createElement('span');
                attrName.className = 'attr-name';
                attrName.textContent = key;
                attrSpan.appendChild(attrName);

                attrSpan.appendChild(document.createTextNode('='));

                const attrValue = document.createElement('span');
                attrValue.className = 'attr-value';
                attrValue.textContent = '"' + value + '"';
                attrSpan.appendChild(attrValue);
            });
            attrSpan.appendChild(document.createTextNode(']'));
            content.appendChild(attrSpan);
        }

        if (node.text) {
            const textSpan = document.createElement('span');
            textSpan.className = 'text-content';
            textSpan.textContent = '"' + node.text + '"';
            content.appendChild(textSpan);
        }

        if (hasChildren) {
            const countSpan = document.createElement('span');
            countSpan.className = 'child-count';
            countSpan.textContent = '(' + node.children.length + ')';
            content.appendChild(countSpan);
        }

        wrapper.appendChild(content);

        if (hasChildren) {
            const childrenContainer = document.createElement('div');
            childrenContainer.className = 'children-container collapsed';

            node.children.forEach(child => {
                childrenContainer.appendChild(buildNode(child));
            });

            wrapper.appendChild(childrenContainer);

            content.addEventListener('click', (event) => {
                event.stopPropagation();
                const collapsed = childrenContainer.classList.toggle('collapsed');
                toggle.textContent = collapsed ? '▶' : '▼';
            });
        }

        return wrapper;
    }

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


    // ── Element refs ────────────────────────────────────────────────────────
    const fileInput = document.getElementById('file-input');
    const uploadZone = document.getElementById('upload-zone');
    const uploadLabel = document.getElementById('upload-label');
    const statusBar = document.getElementById('status-bar');
    const resultsEl = document.getElementById('results');
    const kvBody = document.getElementById('kv-body');
    const countEl = document.getElementById('results-count');
    // ── Private helpers ──────────────────────────────────────────────────────

    function _setStatus(msg, isError = false) {
        statusBar.textContent = msg;
        statusBar.className = 'status-bar' + (isError ? ' error' : '');
    }

    function _setLoading(filename) {
        uploadZone.classList.add('has-file');
        uploadLabel.innerHTML = `<span class="spinner"></span>Parsing <em>${filename}</em>…`;
        _setStatus('');
        resultsEl.hidden = true;
        kvBody.innerHTML = '';
    }

    function _resetUpload() {
        uploadZone.classList.remove('has-file');
        uploadLabel.textContent = 'Click to choose an XML file';
    }

    function _renderTable(entries) {
        kvBody.innerHTML = '';
        const fragment = document.createDocumentFragment();

        entries.forEach(({ key, value }) => {
            const tr = document.createElement('tr');
            if (key.includes('@')) tr.classList.add('is-attr');

            const tdKey = document.createElement('td');
            tdKey.textContent = key;

            const tdVal = document.createElement('td');
            tdVal.textContent = value;

            tr.appendChild(tdKey);
            tr.appendChild(tdVal);
            fragment.appendChild(tr);
        });

        kvBody.appendChild(fragment);
        countEl.textContent = `${entries.length} entr${entries.length === 1 ? 'y' : 'ies'}`;
        resultsEl.hidden = false;
    }

    // ── File change handler ──────────────────────────────────────────────────

    async function _onFileChange(event) {
        const file = event.target.files[0];
        if (!file) return;

        _setLoading(file.name);

        let xmlText;
        try {
            xmlText = await file.text();
        } catch {
            _resetUpload();
            _setStatus('Could not read the file.', true);
            return;
        }

        try {
            const result = await backendApi.parseXml(xmlText);

            _resetUpload();
            uploadLabel.textContent = `📄 ${file.name}`;
            uploadZone.classList.add('has-file');

            if (result.ok) {
                _renderTable(result.entries);
                _setStatus(`Parsed successfully — ${file.name}`);
            } else {
                _setStatus(result.error ?? 'Parse failed.', true);
            }
        } catch (err) {
            _resetUpload();
            _setStatus('Could not reach the backend.', true);
            console.error('[ui] parseXml error:', err);
        }

        // Reset input so the same file can be re-selected after a clear
        fileInput.value = '';
    }

    // ── Public: clear results ────────────────────────────────────────────────

    function clear() {
        _resetUpload();
        _setStatus('');
        resultsEl.hidden = true;
        kvBody.innerHTML = '';
        fileInput.value = '';
    }

    // ── Init ─────────────────────────────────────────────────────────────────
    fileInput.addEventListener('change', _onFileChange);

    return { fetchJoke, clear };
})();
