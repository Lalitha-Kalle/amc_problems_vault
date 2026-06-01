(async function () {
    const $ = id => document.getElementById(id);

    const applyBtn          = $('applyBtn');
    const resetBtn          = $('resetBtn');
    const countEl           = $('resultsCount');
    const tbody             = $('problemsBody');
    const filterNote        = $('filterNote');
    const searchInput       = $('subtopicSearch');
    const searchClear       = $('searchClear');
    const subtopicList      = $('subtopicList');
    const dropdownWrap      = $('subtopicDropdown');
    const difficultySelect  = $('difficultySelect');

    let allSubtopics        = [];
    let selectedSubtopic    = '';
    let selectedDifficulty  = '';

    // ── Load filters and difficulty levels ────────────────────────────
    async function loadFilters() {
        const filterData = await fetch('/api/filters').then(r => r.json());
        const subtopicsData = await fetch('/api/level3').then(r => r.json());
        allSubtopics = subtopicsData.filter(Boolean).sort();

        // Populate difficulty levels
        if (filterData.difficulty_levels) {
            filterData.difficulty_levels.forEach(diff => {
                const option = document.createElement('option');
                option.value = diff.level;
                option.textContent = diff.label;
                difficultySelect.appendChild(option);
            });
        }
    }

    // ── Dropdown rendering ─────────────────────────────────────────────
    function renderList(items) {
        subtopicList.innerHTML = '';
        if (!items.length) {
            const li = document.createElement('li');
            li.className = 'no-results';
            li.textContent = 'No sub-topics found';
            subtopicList.appendChild(li);
            return;
        }
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            if (item === selectedSubtopic) li.classList.add('selected');
            li.addEventListener('mousedown', e => {
                e.preventDefault();
                setSelected(item);
                loadProblems();
            });
            subtopicList.appendChild(li);
        });
    }

    function showDropdown() {
        const q = searchInput.value.trim().toLowerCase();
        const filtered = q
            ? allSubtopics.filter(s => s.toLowerCase().includes(q))
            : allSubtopics;
        renderList(filtered);
        subtopicList.hidden = false;
    }

    function hideDropdown() {
        subtopicList.hidden = true;
    }

    function setSelected(value) {
        selectedSubtopic  = value;
        searchInput.value = value;
        searchClear.hidden = false;
        hideDropdown();
    }

    searchInput.addEventListener('focus', showDropdown);

    searchInput.addEventListener('input', () => {
        if (selectedSubtopic && searchInput.value !== selectedSubtopic) {
            selectedSubtopic = '';
        }
        searchClear.hidden = !searchInput.value;
        showDropdown();
    });

    searchInput.addEventListener('blur', () => {
        setTimeout(hideDropdown, 150);
    });

    searchInput.addEventListener('keydown', e => {
        if (e.key === 'Escape') { hideDropdown(); searchInput.blur(); }
        if (e.key === 'Enter')  { hideDropdown(); loadProblems(); }
    });

    searchClear.addEventListener('click', () => {
        selectedSubtopic   = '';
        searchInput.value  = '';
        searchClear.hidden = true;
        searchInput.focus();
    });

    document.addEventListener('click', e => {
        if (!dropdownWrap.contains(e.target)) hideDropdown();
    });

    // ── Load problems ──────────────────────────────────────────────────
    async function loadProblems() {
        showLoading();
        const params = new URLSearchParams();
        if (selectedSubtopic) params.set('level_3', selectedSubtopic);
        if (selectedDifficulty) params.set('difficulty_level', selectedDifficulty);
        const problems = await fetch(`/api/problems?${params}`).then(r => r.json());
        renderProblems(problems);
    }

    function renderProblems(problems) {
        countEl.textContent = `${problems.length} problem${problems.length !== 1 ? 's' : ''} found`;

        if (problems.length === 0) {
            tbody.innerHTML = `
                <tr><td colspan="8" class="state-cell">
                    <div class="empty-wrap">
                        <div class="empty-icon">&#x1F50D;</div>
                        <p class="empty-text">No problems match your filters.</p>
                    </div>
                </td></tr>`;
            return;
        }

        tbody.innerHTML = '';
        problems.forEach(p => {
            const tr = document.createElement('tr');
            tr.addEventListener('click', () =>
                window.open(`/problem/${p.year}/${p.version}/${p.question_num}`, '_blank'));

            const tagsHtml = (raw, cls) => raw
                ? raw.split(',').map(t => `<span class="tag ${cls}" title="${esc(t)}">${esc(trunc(t, 30))}</span>`).join('')
                : `<span class="tag tag-none">—</span>`;

            const contentHtml = p.has_content
                ? `<span class="content-pill yes">&#x2713; Full text</span>`
                : `<span class="content-pill no">Topics only</span>`;

            tr.innerHTML = `
                <td class="year-cell">${p.year}</td>
                <td><span class="ver-pill">${p.version}</span></td>
                <td><span class="qnum-circle">${p.question_num}</span></td>
                <td><div class="tags">${tagsHtml(p.level_1s, 'tag-l1')}</div></td>
                <td><div class="tags">${tagsHtml(p.level_2s, 'tag-l2')}</div></td>
                <td><div class="tags">${tagsHtml(p.level_3s, 'tag-l3')}</div></td>
                <td>${contentHtml}</td>
                <td>
                    <button class="view-btn"
                        onclick="event.stopPropagation();window.open('/problem/${p.year}/${p.version}/${p.question_num}','_blank')">
                        View &#x2192;
                    </button>
                </td>`;
            tbody.appendChild(tr);
        });
    }

    function showLoading() {
        countEl.textContent = 'Loading…';
        tbody.innerHTML = `
            <tr><td colspan="8" class="state-cell">
                <div class="state-inner"><div class="spinner"></div>Loading problems…</div>
            </td></tr>`;
    }

    // ── Difficulty level handler ───────────────────────────────────────
    difficultySelect.addEventListener('change', () => {
        selectedDifficulty = difficultySelect.value;
        loadProblems();
    });

    // ── Reset ──────────────────────────────────────────────────────────
    function reset() {
        selectedSubtopic    = '';
        selectedDifficulty  = '';
        searchInput.value   = '';
        searchClear.hidden  = true;
        difficultySelect.value = '';
        filterNote.textContent = '';
        loadProblems();
    }

    applyBtn.addEventListener('click', loadProblems);
    resetBtn.addEventListener('click', reset);

    // ── Helpers ───────────────────────────────────────────────────────
    function esc(s) {
        return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }
    function trunc(s, n) { return s.length > n ? s.slice(0, n) + '…' : s; }

    // ── Init ──────────────────────────────────────────────────────────
    await loadFilters();
    await loadProblems();
})();
