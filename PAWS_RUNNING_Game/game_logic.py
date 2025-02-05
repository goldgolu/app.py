import random
from datetime import datetime, timedelta

class GameLogic:
    def __init__(self):
        self.players = {}
        self.lottery_pool = []
        self.tasks = {}
        self.trades = []
        self.ai_bot = "Ai Robota"
    
    def add_player(self, player_id, username):
        if player_id not in self.players:
            self.players[player_id] = {
                "username": username,
                "balance": 100,
                "inventory": [],
                "tasks": []
            }
            return f"{username} added successfully!"
        return "Player already exists."
    
    def add_to_lottery(self, player_id):
        if player_id in self.players:
            self.lottery_pool.append(player_id)
            return "Added to lottery pool."
        return "Player not found."
    
    def draw_lottery(self):
        if self.lottery_pool:
            winner = random.choice(self.lottery_pool)
            self.players[winner]["balance"] += 500
            self.lottery_pool = []  # Reset pool
            return f"Lottery Winner: {self.players[winner]['username']}"
        return "No participants in the lottery."
    
    def add_task(self, task_id, description, reward):
        self.tasks[task_id] = {
            "description": description,
            "reward": reward,
            "completed_by": []
        }
        return "Task added successfully."
    
    def complete_task(self, player_id, task_id):
        if task_id in self.tasks and player_id in self.players:
            if player_id not in self.tasks[task_id]["completed_by"]:
                self.tasks[task_id]["completed_by"].append(player_id)
                self.players[player_id]["balance"] += self.tasks[task_id]["reward"]
                return "Task completed! Reward credited."
            return "Task already completed by this player."
        return "Invalid task or player."
    
    def trade_items(self, sender_id, receiver_id, item):
        if sender_id in self.players and receiver_id in self.players:
            if item in self.players[sender_id]["inventory"]:
                self.players[sender_id]["inventory"].remove(item)
                self.players[receiver_id]["inventory"].append(item)
                self.trades.append({"from": sender_id, "to": receiver_id, "item": item})
                return "Trade successful!"
            return "Item not available."
        return "Invalid trade participants."
    
    def ai_bot_response(self, command):
        responses = {
            "status": "Game is running smoothly!",
            "players": f"Total players: {len(self.players)}",
            "lottery": self.draw_lottery()
        }
        return responses.get(command, "Invalid command.")
