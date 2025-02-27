from celery import Celery
import sqlite3

# Celery Setup
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def add_task(user_id, task_name, status="pending"):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (user_id, task_name, status) VALUES (?, ?, ?)", (user_id, task_name, status))
    conn.commit()
    conn.close()
    return f"Task '{task_name}' added for user {user_id}."

@celery.task
def complete_task(task_id):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status='completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return f"Task {task_id} marked as completed."

def get_tasks(user_id):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks
