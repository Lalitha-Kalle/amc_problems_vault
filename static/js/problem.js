(function () {
    const body     = document.body;
    const YEAR     = body.dataset.year;
    const VERSION  = body.dataset.version;
    const QNUM     = body.dataset.qnum;

    // ── Load problem data ─────────────────────────────────────────────
    async function loadProblem() {
        const data = await fetch(`/api/problem/${YEAR}/${VERSION}/${QNUM}`).then(r => r.json());

        // Title
        document.getElementById('problemTitle').textContent =
            `AMC 10${VERSION} ${YEAR} — Problem ${QNUM}`;
        document.title = `AMC 10${VERSION} ${YEAR} Q${QNUM}`;

        // Topic chips (unique level_1 values)
        const chipsEl = document.getElementById('topicChips');
        const seen = new Set();
        data.topics.forEach(({ level_1, level_2, level_3 }) => {
            if (!seen.has(level_1)) {
                seen.add(level_1);
                chipsEl.appendChild(chip(level_1, 'chip-l1'));
            }
        });

        // Question content
        const qEl = document.getElementById('questionContent');
        if (data.problem) {
            qEl.innerHTML = data.problem;
            // Fix protocol-relative URLs → https
            qEl.querySelectorAll('img').forEach(img => {
                if (img.src.startsWith('//')) img.src = 'https:' + img.getAttribute('src');
            });
        } else {
            qEl.innerHTML = noContentHTML(data);
        }

        // Solution / reveal button
        const revealState  = document.getElementById('revealState');
        const revealBtn    = document.getElementById('revealBtn');
        const answerContent = document.getElementById('answerContent');

        if (data.solution) {
            revealBtn.addEventListener('click', () => {
                revealState.style.display = 'none';
                answerContent.style.display = 'flex';
                answerContent.style.flexDirection = 'column';
                answerContent.innerHTML = data.solution;
                // Fix protocol-relative URLs
                answerContent.querySelectorAll('img').forEach(img => {
                    if (img.src.startsWith('//')) img.src = 'https:' + img.getAttribute('src');
                });
            });
        } else {
            revealState.innerHTML = `<p style="color:var(--muted);font-size:.9rem">Solution not available for this year.</p>`;
        }
    }

    function chip(text, cls) {
        const s = document.createElement('span');
        s.className = `chip ${cls}`;
        s.textContent = text;
        return s;
    }

    function noContentHTML(data) {
        if (data.topics.length === 0) {
            return `<div class="no-content-box"><p>Problem content not available.</p></div>`;
        }
        const rows = data.topics.map(t =>
            `<div class="topic-row"><strong>${esc(t.level_1)}</strong> › ${esc(t.level_2)} › ${esc(t.level_3)}</div>`
        ).join('');
        return `<div class="no-content-box">
            <h3>AMC 10${VERSION} ${YEAR} — Problem ${QNUM}</h3>
            <p>Full problem text is only available for the 2025 contest.<br>
               Topic classification data for this problem is shown below.</p>
            <div class="topics-grid">${rows}</div>
        </div>`;
    }

    function esc(s) {
        return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }

    // ── Canvas setup ─────────────────────────────────────────────────
    function setupCanvas() {
        const wrap   = document.getElementById('canvasWrap');
        const canvas = document.getElementById('drawCanvas');
        const ctx    = canvas.getContext('2d');

        let drawing  = false;
        let color    = '#1a1a1a';
        let size     = 3;
        let erasing  = false;
        let lastX    = 0;
        let lastY    = 0;

        function initCanvas() {
            const r = wrap.getBoundingClientRect();
            canvas.width  = r.width;
            canvas.height = r.height;
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        initCanvas();

        // Keep canvas size in sync with container
        const ro = new ResizeObserver(() => {
            const r = wrap.getBoundingClientRect();
            if (r.width < 1 || r.height < 1) return;

            // Preserve current drawing across resize
            const tmp = document.createElement('canvas');
            tmp.width = canvas.width; tmp.height = canvas.height;
            tmp.getContext('2d').drawImage(canvas, 0, 0);

            canvas.width  = r.width;
            canvas.height = r.height;
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(tmp, 0, 0);
        });
        ro.observe(wrap);

        // ── Pointer helpers ──
        function getPos(e) {
            const r = canvas.getBoundingClientRect();
            const src = e.touches ? e.touches[0] : e;
            return { x: src.clientX - r.left, y: src.clientY - r.top };
        }

        function startStroke(e) {
            e.preventDefault();
            drawing = true;
            const { x, y } = getPos(e);
            lastX = x; lastY = y;

            // Paint a dot so single clicks leave a mark
            ctx.beginPath();
            const r = effectiveSize() / 2;
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fillStyle = erasing ? '#ffffff' : color;
            ctx.fill();
        }

        function stroke(e) {
            if (!drawing) return;
            e.preventDefault();
            const { x, y } = getPos(e);

            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = erasing ? '#ffffff' : color;
            ctx.lineWidth   = effectiveSize();
            ctx.lineCap     = 'round';
            ctx.lineJoin    = 'round';
            ctx.stroke();

            lastX = x; lastY = y;
        }

        function endStroke() { drawing = false; }

        function effectiveSize() { return erasing ? size * 4 : size; }

        canvas.addEventListener('mousedown',  startStroke);
        canvas.addEventListener('mousemove',  stroke);
        canvas.addEventListener('mouseup',    endStroke);
        canvas.addEventListener('mouseleave', endStroke);
        canvas.addEventListener('touchstart', startStroke, { passive: false });
        canvas.addEventListener('touchmove',  stroke,      { passive: false });
        canvas.addEventListener('touchend',   endStroke);

        // ── Color swatches ──
        document.querySelectorAll('.swatch').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.swatch').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                color = btn.dataset.color;
                activatePen();
            });
        });

        const customColor = document.getElementById('customColor');
        customColor.addEventListener('input', () => {
            color = customColor.value;
            document.querySelectorAll('.swatch').forEach(b => b.classList.remove('active'));
            activatePen();
        });

        // ── Size slider ──
        const penSizeInput = document.getElementById('penSize');
        const penSizeLabel = document.getElementById('penSizeLabel');
        penSizeInput.addEventListener('input', () => {
            size = parseInt(penSizeInput.value, 10);
            penSizeLabel.textContent = `${size} px`;
        });

        // ── Tool buttons ──
        const penBtn    = document.getElementById('penBtn');
        const eraserBtn = document.getElementById('eraserBtn');

        function activatePen() {
            erasing = false;
            penBtn.classList.add('active');
            eraserBtn.classList.remove('active');
            canvas.style.cursor = 'crosshair';
        }

        function activateEraser() {
            erasing = true;
            eraserBtn.classList.add('active');
            penBtn.classList.remove('active');
            canvas.style.cursor = 'cell';
        }

        penBtn.addEventListener('click',    activatePen);
        eraserBtn.addEventListener('click', activateEraser);

        // ── Clear ──
        document.getElementById('clearBtn').addEventListener('click', () => {
            if (confirm('Clear the canvas? This cannot be undone.')) {
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }
        });

        // ── Save as PDF ──
        document.getElementById('savePdfBtn').addEventListener('click', () => {
            const { jsPDF } = window.jspdf;
            const isLandscape = canvas.width > canvas.height;
            const pdf = new jsPDF({
                orientation: isLandscape ? 'landscape' : 'portrait',
                unit: 'px',
                format: [canvas.width, canvas.height],
                hotfixes: ['px_scaling']
            });
            pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, canvas.width, canvas.height);
            pdf.save(`AMC10${VERSION}_${YEAR}_Q${QNUM}_notes.pdf`);
        });
    }

    // ── Panel resizer (drag to resize left/right split) ────────────────
    function setupResizer() {
        const resizer   = document.getElementById('panelResizer');
        const leftPanel = document.getElementById('leftPanel');
        const layout    = document.querySelector('.split-layout');
        let active = false;

        resizer.addEventListener('mousedown', e => {
            active = true;
            resizer.classList.add('active');
            document.body.style.cursor     = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        });

        document.addEventListener('mousemove', e => {
            if (!active) return;
            const rect     = layout.getBoundingClientRect();
            const newWidth = e.clientX - rect.left;
            const min = 250, max = rect.width - 300 - 5;
            if (newWidth >= min && newWidth <= max) {
                leftPanel.style.width = newWidth + 'px';
            }
        });

        document.addEventListener('mouseup', () => {
            if (!active) return;
            active = false;
            resizer.classList.remove('active');
            document.body.style.cursor     = '';
            document.body.style.userSelect = '';
        });
    }

    // ── Tab switching ─────────────────────────────────────────────────
    function setupTabs() {
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(tab.dataset.panel).classList.add('active');
            });
        });
    }

    // ── Font size controls ────────────────────────────────────────────
    function setupFontSize() {
        let size = 15;
        const MIN = 11, MAX = 22;

        function apply() {
            document.documentElement.style.setProperty('--content-font-size', size + 'px');
        }

        document.getElementById('fontSmaller').addEventListener('click', () => {
            if (size > MIN) { size--; apply(); }
        });
        document.getElementById('fontLarger').addEventListener('click', () => {
            if (size < MAX) { size++; apply(); }
        });
        document.getElementById('fontReset').addEventListener('click', () => {
            size = 15; apply();
        });
    }

    // ── Init ─────────────────────────────────────────────────────────
    loadProblem();
    setupCanvas();
    setupResizer();
    setupTabs();
    setupFontSize();
})();
