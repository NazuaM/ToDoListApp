import os
import psycopg2
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    result = urlparse(os.environ.get("DATABASE_URL"))
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
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
        # Redirect to login page if no uid provided
        return redirect(url_for('login'))  # Create a login route to serve login.html

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE user_id = %s ORDER BY id', (uid,))
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tasks=tasks, uid=uid)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('newTask')
    uid = request.form.get('uid')
    if new_task and uid:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (user_id, task) VALUES (%s, %s)', (uid, new_task))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index', uid=uid))

@app.route('/complete', methods=['POST'])
def complete_tasks():
    completed_tasks = request.form.getlist('taskCheckbox')
    uid = request.form.get('uid')
    if uid:
        conn = get_db_connection()
        cur = conn.cursor()
        for task_id in completed_tasks:
            cur.execute('UPDATE tasks SET completed = TRUE WHERE id = %s AND user_id = %s', (int(task_id), uid))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index', uid=uid))

@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')
    uid = request.form.get('uid')
    if task_id and uid:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, uid))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index', uid=uid))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)