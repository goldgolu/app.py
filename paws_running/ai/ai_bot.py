import sqlite3
import json

def connect_db():
    return sqlite3.connect('database/game_data.db')

class AiRobota:
    def __init__(self):
        self.name = "Ai Robota"
        self.owner = "admin"  # Isse database se fetch karna hoga

    def get_owner(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT owner FROM settings LIMIT 1")
        owner = cursor.fetchone()
        conn.close()
        return owner[0] if owner else "admin"

    def process_command(self, user, command):
        if user != self.get_owner():
            return "Access Denied! Only the owner can give me commands."
        
        if command.startswith("add_feature"):
            feature = command.split(" ", 1)[1]
            return self.add_feature(feature)
        
        if command.startswith("remove_feature"):
            feature = command.split(" ", 1)[1]
            return self.remove_feature(feature)
        
        return "Unknown command."

    def add_feature(self, feature):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO features (name) VALUES (?)", (feature,))
        conn.commit()
        conn.close()
        return f"Feature '{feature}' added successfully!"

    def remove_feature(self, feature):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM features WHERE name = ?", (feature,))
        conn.commit()
        conn.close()
        return f"Feature '{feature}' removed successfully!"

if __name__ == "__main__":
    ai = AiRobota()
    print(ai.process_command("admin", "add_feature leaderboard"))
