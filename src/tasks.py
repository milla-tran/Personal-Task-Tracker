from src.db import get_connection

def add_task(title, category=None, due_date=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, category, due_date) VALUES (?, ?, ?)",
        (title, category, due_date)
    )
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, category, due_date, completed FROM tasks ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def toggle_task(task_id, completed):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
    conn.commit()
    conn.close()