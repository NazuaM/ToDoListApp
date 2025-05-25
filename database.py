import sqlite3

def init_db():
    connect = sqlite3.connect('tasks.db')
    c = connect.cursor()
    # Create table if not exists
    c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        ''')
    c.commit()
    c.close()

