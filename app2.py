from flask import Flask, request, jsonify, redirect
import sqlite3
import string
import random
from datetime import datetime, timedelta

app = Flask(__name__)
DB = "urls.db"

# base62 characters for generating short codes
CHARS = string.ascii_letters + string.digits


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def generate_short_code(length=6):
    # randomly pick 6 characters from base62 set
    return ''.join(random.choices(CHARS, k=length))


@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'Please provide a url field'}), 400

    original_url = data['url']

    if not original_url.startswith('http'):
        return jsonify({'error': 'URL must start with http or https'}), 400

    # default expiry is 30 days
    days = data.get('expires_in_days', 30)
    expires_at = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db()

    # keep generating until we get a unique code
    while True:
        code = generate_short_code()
        existing = conn.execute('SELECT id FROM urls WHERE short_code = ?', (code,)).fetchone()
        if not existing:
            break

    conn.execute(
        'INSERT INTO urls (original_url, short_code, created_at, expires_at) VALUES (?, ?, ?, ?)',
        (original_url, code, created_at, expires_at)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'short_code': code,
        'short_url': f'http://localhost:5000/{code}',
        'expires_at': expires_at
    }), 201


@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    conn = get_db()
    row = conn.execute(
        'SELECT original_url, expires_at FROM urls WHERE short_code = ?',
        (short_code,)
    ).fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Short URL not found'}), 404

    # check if the link has expired
    expires_at = datetime.strptime(row['expires_at'], '%Y-%m-%d %H:%M:%S')
    if datetime.now() > expires_at:
        return jsonify({'error': 'This link has expired'}), 410

    return redirect(row['original_url'])


@app.route('/info/<short_code>', methods=['GET'])
def url_info(short_code):
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM urls WHERE short_code = ?',
        (short_code,)
    ).fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Short URL not found'}), 404

    return jsonify({
        'short_code': row['short_code'],
        'original_url': row['original_url'],
        'created_at': row['created_at'],
        'expires_at': row['expires_at']
    })


@app.route('/all', methods=['GET'])
def list_all():
    conn = get_db()
    rows = conn.execute('SELECT * FROM urls ORDER BY id DESC').fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            'short_code': row['short_code'],
            'original_url': row['original_url'],
            'created_at': row['created_at'],
            'expires_at': row['expires_at']
        })

    return jsonify(result)


if __name__ == '__main__':
    init_db()
    print("Database initialized.")
    print("Server running at http://localhost:5000")
    app.run(debug=True)
