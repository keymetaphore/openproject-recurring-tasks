import sqlite3
from scheduler.scheduler import schedule_task
from settings import DB_PATH

def initialize_db_and_schedule():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        interval TEXT,
        project_id TEXT,
        user_id TEXT,
        description TEXT,
        status TEXT DEFAULT 'active'
    )''')

    c.execute("SELECT title, interval, project_id, user_id, description FROM tasks WHERE status = 'active'")
    for row in c.fetchall():
        try:
            schedule_task(*row)
        except Exception as e:
            print(f"Could not schedule task {row[0]}: {e}")
    conn.close()
