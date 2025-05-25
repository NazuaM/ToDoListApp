import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = 'tasks.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('newTask')
    if new_task:
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (task) VALUES (?)', (new_task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete_tasks():
    completed_tasks = request.form.getlist('taskCheckbox')
    conn = get_db_connection()
    for task_id in completed_tasks:
        conn.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (int(task_id),))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)