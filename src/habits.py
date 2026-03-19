from datetime import date
from src.db import get_connection

def add_habit(name, icon="🌸"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO habits (name, icon) VALUES (?, ?)", (name, icon))
    conn.commit()
    conn.close()

def get_habits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, icon FROM habits ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def set_habit_done(habit_id, log_date=None, completed=True):
    if log_date is None:
        log_date = str(date.today())

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM habit_logs WHERE habit_id = ? AND log_date = ?",
        (habit_id, log_date)
    )
    row = cur.fetchone()

    if row:
        cur.execute(
            "UPDATE habit_logs SET completed = ? WHERE id = ?",
            (1 if completed else 0, row[0])
        )
    else:
        cur.execute(
            "INSERT INTO habit_logs (habit_id, log_date, completed) VALUES (?, ?, ?)",
            (habit_id, log_date, 1 if completed else 0)
        )

    conn.commit()
    conn.close()

def is_habit_done_today(habit_id, log_date=None):
    if log_date is None:
        log_date = str(date.today())

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT completed FROM habit_logs WHERE habit_id = ? AND log_date = ?",
        (habit_id, log_date)
    )
    row = cur.fetchone()
    conn.close()
    return bool(row and row[0] == 1)