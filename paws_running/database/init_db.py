import sqlite3

def init_db():
    conn = sqlite3.connect("database/game_data.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        coins INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
    )
    """)

    # Inventory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        transaction_type TEXT CHECK(transaction_type IN ('deposit', 'withdrawal')),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Lottery winnings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lottery_winnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        prize INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Guilds table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guilds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        owner_id INTEGER,
        members_count INTEGER DEFAULT 1,
        FOREIGN KEY (owner_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
