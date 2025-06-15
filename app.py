import os
import psycopg2
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def get_db_connection():
    result = urlparse(os.environ.get("DATABASE_URL"))
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
        sslmode='require'
    )
    return conn

@app.route('/init-db')
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    return "Database initialized!"

@app.route('/')
def index():
    uid = request.args.get('uid', '')
    if not uid:
        return redirect(url_for('login'))
    return render_template('index.html', uid=uid)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task')  # Changed from 'newTask' to match JS
    uid = request.form.get('uid')
    if new_task and uid:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (user_id, task) VALUES (%s, %s) RETURNING id', (uid, new_task))
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': task_id, 'task': new_task})
    return 'Missing data', 400

@app.route('/get-tasks')
def get_tasks():
    uid = request.args.get('uid')
    if not uid:
        return jsonify([])
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, task, completed FROM tasks WHERE user_id = %s ORDER BY id', (uid,))
    tasks = [{'id': row[0], 'task': row[1], 'completed': row[2]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route('/update-task', methods=['POST'])
def update_task():
    task_id = request.form.get('task_id')
    completed = request.form.get('completed') == 'true'
    uid = request.form.get('uid')
    if task_id and uid:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET completed = %s WHERE id = %s AND user_id = %s', (completed, task_id, uid))
        conn.commit()
        cur.close()
        conn.close()
        return '', 204
    return 'Missing data', 400

@app.route('/update-task-text', methods=['POST'])
def update_task_text():
    task_id = request.form.get('task_id')
    new_text = request.form.get('new_text')
    uid = request.form.get('uid')
    if task_id and new_text and uid:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET task = %s WHERE id = %s AND user_id = %s', (new_text, task_id, uid))
        conn.commit()
        cur.close()
        conn.close()
        return '', 204
    return 'Missing data', 400

@app.route('/delete-task', methods=['POST'])
def delete_task_js():
    task_id = request.form.get('task_id')
    uid = request.form.get('uid')
    if task_id and uid:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, uid))
        conn.commit()
        cur.close()
        conn.close()
        return '', 204
    return 'Missing data', 400

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)