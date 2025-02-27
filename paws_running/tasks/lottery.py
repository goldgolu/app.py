from celery import Celery
import sqlite3
import random

# Celery Setup
celery = Celery(
    "lottery",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def enter_lottery(user_id, ticket_cost=10):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT coins FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user and user[0] >= ticket_cost:
        cursor.execute("UPDATE users SET coins = coins - ? WHERE id=?", (ticket_cost, user_id))
        cursor.execute("INSERT INTO lottery_entries (user_id) VALUES (?)", (user_id,))
        conn.commit()
        result = f"✅ User {user_id} entered the lottery!"
    else:
        result = f"❌ User {user_id} does not have enough coins."

    conn.close()
    return result

@celery.task
def draw_lottery_winner():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM lottery_entries")
    entries = cursor.fetchall()

    if entries:
        winner = random.choice(entries)[0]
        prize = 100  # Example prize amount

        cursor.execute("UPDATE users SET coins = coins + ? WHERE id=?", (prize, winner))
        cursor.execute("INSERT INTO lottery_winnings (user_id, prize) VALUES (?, ?)", (winner, prize))
        cursor.execute("DELETE FROM lottery_entries")  # Reset lottery entries
        conn.commit()
        result = f"🎉 Lottery Winner: User {winner}, Prize: {prize} Coins!"
    else:
        result = "⚠️ No entries found in the lottery."

    conn.close()
    return result
