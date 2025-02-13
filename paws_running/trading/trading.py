import sqlite3

class TradingSystem:
    def __init__(self, db_path="database/game_data.db"):
        self.db_path = db_path

    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def trade_assets(self, sender_id, receiver_id, asset, amount):
        """
        Handle asset trading between users.
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Check sender balance
        cursor.execute("SELECT {0} FROM users WHERE user_id = ?".format(asset), (sender_id,))
        sender_balance = cursor.fetchone()
        
        if sender_balance and sender_balance[0] >= amount:
            # Deduct from sender
            cursor.execute("UPDATE users SET {0} = {0} - ? WHERE user_id = ?".format(asset), (amount, sender_id))
            # Add to receiver
            cursor.execute("UPDATE users SET {0} = {0} + ? WHERE user_id = ?".format(asset), (amount, receiver_id))
            
            conn.commit()
            conn.close()
            return f"Trade successful: {amount} {asset} transferred from {sender_id} to {receiver_id}"
        
        conn.close()
        return "Trade failed: Insufficient balance"

    def get_user_assets(self, user_id):
        """
        Retrieve user asset details.
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT coins, gems, items FROM users WHERE user_id = ?", (user_id,))
        user_assets = cursor.fetchone()
        conn.close()
        
        if user_assets:
            return {"coins": user_assets[0], "gems": user_assets[1], "items": user_assets[2]}
        return "User not found"

# Example Usage
if __name__ == "__main__":
    trade_system = TradingSystem()
    print(trade_system.trade_assets(1, 2, "coins", 50))
    print(trade_system.get_user_assets(1))
