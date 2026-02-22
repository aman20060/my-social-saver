import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "social_saver.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            category TEXT,
            summary TEXT,
            title TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_link(url, category, summary, title):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO links (url, category, summary, title) VALUES (?, ?, ?, ?)', 
              (url, category, summary, title))
    conn.commit()
    conn.close()

def get_all_links():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM links ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

init_db()