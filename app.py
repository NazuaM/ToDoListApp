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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks ORDER BY id')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('newTask')
    if new_task:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (task) VALUES (%s)', (new_task,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete_tasks():
    completed_tasks = request.form.getlist('taskCheckbox')
    conn = get_db_connection()
    cur = conn.cursor()
    for task_id in completed_tasks:
        cur.execute('UPDATE tasks SET completed = TRUE WHERE id = %s', (int(task_id),))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)