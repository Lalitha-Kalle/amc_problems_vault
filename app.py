from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

import sqlite3
import os


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'amc-vault-secret-key-2024')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', False)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'amc_problems.db')

# ── Login Manager Setup ────────────────────────────────────────────
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ── User Class ─────────────────────────────────────────────────────
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

# Default credentials
DEFAULT_USERNAME = os.getenv("USER_NAME")
DEFAULT_PASSWORD_HASH = generate_password_hash(os.getenv("PASSWORD"))

@login_manager.user_loader
def load_user(username):
    if username == DEFAULT_USERNAME:
        return User(username)
    return None


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_difficulty_level(question_num):
    if 1 <= question_num <= 10:
        return 1
    elif 11 <= question_num <= 15:
        return 2
    elif 16 <= question_num <= 20:
        return 3
    elif 21 <= question_num <= 25:
        return 4
    return None


# ── Auth Routes ────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Check credentials
        if username == DEFAULT_USERNAME and check_password_hash(DEFAULT_PASSWORD_HASH, password):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ── App Routes ─────────────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/problem/<int:year>/<version>/<int:question_num>')
@login_required
def problem_view(year, version, question_num):
    return render_template('problem.html', year=year, version=version, question_num=question_num)


@app.route('/api/filters')
@login_required
def get_filters():
    conn = get_db()
    try:
        years = [r[0] for r in conn.execute(
            'SELECT DISTINCT year FROM problems ORDER BY year DESC').fetchall()]
        level1s = [r[0] for r in conn.execute(
            'SELECT DISTINCT level_1 FROM problems ORDER BY level_1').fetchall()]
    finally:
        conn.close()
    return jsonify({
        'years': years,
        'level1s': level1s,
        'difficulty_levels': [
            {'level': 1, 'label': 'Level 1 (Q1-10)'},
            {'level': 2, 'label': 'Level 2 (Q11-15)'},
            {'level': 3, 'label': 'Level 3 (Q16-20)'},
            {'level': 4, 'label': 'Level 4 (Q21-25)'}
        ]
    })


@app.route('/api/level2')
@login_required
def get_level2():
    level_1 = request.args.get('level_1', '')
    conn = get_db()
    try:
        if level_1:
            rows = conn.execute(
                'SELECT DISTINCT level_2 FROM problems WHERE level_1 = ? ORDER BY level_2',
                (level_1,)).fetchall()
        else:
            rows = conn.execute(
                'SELECT DISTINCT level_2 FROM problems ORDER BY level_2').fetchall()
    finally:
        conn.close()
    return jsonify([r[0] for r in rows])


@app.route('/api/level3')
@login_required
def get_level3():
    level_1 = request.args.get('level_1', '')
    level_2 = request.args.get('level_2', '')
    conn = get_db()
    try:
        conditions, params = [], []
        if level_1:
            conditions.append('level_1 = ?')
            params.append(level_1)
        if level_2:
            conditions.append('level_2 = ?')
            params.append(level_2)
        where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''
        rows = conn.execute(
            f'SELECT DISTINCT level_3 FROM problems {where} ORDER BY level_3',
            params).fetchall()
    finally:
        conn.close()
    return jsonify([r[0] for r in rows])


@app.route('/api/problems')
@login_required
def get_problems():
    year             = request.args.get('year', type=int)
    version          = request.args.get('version', '')
    level_1          = request.args.get('level_1', '')
    level_2          = request.args.get('level_2', '')
    level_3          = request.args.get('level_3', '')
    question_num     = request.args.get('question_num', type=int)
    difficulty_level = request.args.get('difficulty_level', type=int)

    conditions, params = [], []
    if year:
        conditions.append('p.year = ?');         params.append(year)
    if version:
        conditions.append('p.version = ?');      params.append(version)
    if level_1:
        conditions.append('p.level_1 = ?');      params.append(level_1)
    if level_2:
        conditions.append('p.level_2 = ?');      params.append(level_2)
    if level_3:
        conditions.append('p.level_3 = ?');      params.append(level_3)
    if question_num:
        conditions.append('p.question_num = ?'); params.append(question_num)
    if difficulty_level:
        if difficulty_level == 1:
            conditions.append('p.question_num BETWEEN 1 AND 10')
        elif difficulty_level == 2:
            conditions.append('p.question_num BETWEEN 11 AND 15')
        elif difficulty_level == 3:
            conditions.append('p.question_num BETWEEN 16 AND 20')
        elif difficulty_level == 4:
            conditions.append('p.question_num BETWEEN 21 AND 25')

    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    conn = get_db()
    try:
        rows = conn.execute(f'''
            SELECT p.year, p.version, p.question_num,
                   GROUP_CONCAT(DISTINCT p.level_1) AS level_1s,
                   GROUP_CONCAT(DISTINCT p.level_2) AS level_2s,
                   GROUP_CONCAT(DISTINCT p.level_3) AS level_3s,
                   CASE WHEN p2.question_num IS NOT NULL THEN 1 ELSE 0 END AS has_content
            FROM problems p
            LEFT JOIN problem_content p2
                   ON p.year = p2.year AND p.version = p2.version AND p.question_num = p2.question_num
            {where}
            GROUP BY p.year, p.version, p.question_num
            ORDER BY p.year DESC, p.version, p.question_num
        ''', params).fetchall()
    finally:
        conn.close()

    return jsonify([dict(r) for r in rows])


@app.route('/api/problem/<int:year>/<version>/<int:question_num>')
@login_required
def get_problem(year, version, question_num):
    conn = get_db()
    try:
        topics = conn.execute('''
            SELECT level_1, level_2, level_3 FROM problems
            WHERE year = ? AND version = ? AND question_num = ?
            ORDER BY level_1, level_2, level_3
        ''', (year, version, question_num)).fetchall()

        content = conn.execute('''
            SELECT problem, solution FROM problem_content
            WHERE year = ? AND version = ? AND question_num = ?
        ''', (year, version, question_num)).fetchone()
    finally:
        conn.close()

    return jsonify({
        'year': year,
        'version': version,
        'question_num': question_num,
        'topics': [dict(t) for t in topics],
        'problem': content['problem'] if content else None,
        'solution': content['solution'] if content else None,
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
