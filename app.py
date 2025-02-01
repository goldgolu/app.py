from flask import Flask, render_template, send_from_directory
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from flask import request, redirect, jsonify
import requests
import threading
import os
import time
import random
import sqlite3

# Environment variables for secrets
INSTAGRAM_CLIENT_ID = os.getenv('INSTAGRAM_CLIENT_ID', 'mohammad')
INSTAGRAM_CLIENT_SECRET = os.getenv('INSTAGRAM_CLIENT_SECRET', 'Mohali@321')
REDIRECT_URI = 'http://127.0.0.1:5000/instagram/callback'
BOT_TOKEN = os.getenv('BOT_TOKEN', 'default_token')
FLASK_SERVER_URL = 'http://127.0.0.1:5000'

OWNER_ID = os.getenv('OWNER_ID', '12345678')

if not OWNER_ID.isdigit():
    print(f"⚠ Error: Invalid OWNER_ID: {OWNER_ID}, using default 12345678.")
    OWNER_ID = 12345678
else:
    OWNER_ID = int(OWNER_ID)

import os
app = Flask(_name_, template_folder='my_templates')  # Specify the new template folder name
    
# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game_start')
def game_start():
    return render_template('game.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/logo.png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Database setup
def init_db():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        coins INTEGER DEFAULT 1000,
                        pph INTEGER DEFAULT 0,
                        level INTEGER DEFAULT 1,
                        language TEXT DEFAULT 'English',
                        sound_on BOOLEAN DEFAULT 1
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS lotteries (
                        date TEXT PRIMARY KEY,
                        lottery_number INTEGER,
                        spin_count INTEGER DEFAULT 0
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        task_id INTEGER PRIMARY KEY,
                        description TEXT,
                        reward INTEGER
                    )''')
    conn.commit()
    conn.close()

init_db()

# Helper functions for database operations
def get_or_create_user(user_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        user = (user_id, 1000, 0, 1, 'English', 1)  # Default values
    conn.close()
    return user

def update_user(user_id, coins=None, pph=None, level=None, language=None, sound_on=None):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    if coins is not None:
        cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (coins, user_id))
    if pph is not None:
        cursor.execute("UPDATE users SET pph = ? WHERE user_id = ?", (pph, user_id))
    if level is not None:
        cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", (level, user_id))
    if language is not None:
        cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
    if sound_on is not None:
        cursor.execute("UPDATE users SET sound_on = ? WHERE user_id = ?", (sound_on, user_id))
    conn.commit()
    conn.close()

# Lottery functions
def generate_lottery_number():
    return random.randint(1000, 9999)

def get_or_create_daily_lottery():
    today = time.strftime("%Y-%m-%d")
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lotteries WHERE date = ?", (today,))
    lottery = cursor.fetchone()
    if not lottery:
        lottery_number = generate_lottery_number()
        cursor.execute("INSERT INTO lotteries (date, lottery_number) VALUES (?, ?)", (today, lottery_number))
        conn.commit()
        lottery = (today, lottery_number, 0)
    conn.close()
    return lottery

def spin_lottery(user_id):
    user_lottery_number = generate_lottery_number()
    daily_lottery = get_or_create_daily_lottery()
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE lotteries SET spin_count = spin_count + 1 WHERE date = ?", (daily_lottery[0],))
    conn.commit()
    conn.close()
    is_winner = user_lottery_number == daily_lottery[1]
    return user_lottery_number, is_winner

# Task functions
def get_tasks():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def complete_task(user_id, task_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT reward FROM tasks WHERE task_id = ?", (task_id,))
    reward = cursor.fetchone()
    if reward:
        reward = reward[0]
        cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (reward, user_id))
        conn.commit()
    conn.close()

# Telegram Bot Handlers
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_or_create_user(user_id)
    keyboard = [
        [InlineKeyboardButton("Login with Instagram", url=f"{FLASK_SERVER_URL}/instagram/login")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to PAWS 🐾 RUNNING! Use /menu to access the game or login with Instagram:", reply_markup=reply_markup)

def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Store", callback_data='store')],
        [InlineKeyboardButton("Tasks", callback_data='tasks')],
        [InlineKeyboardButton("Play Business Empire", callback_data='play_business_empire')],
        [InlineKeyboardButton("Leaderboard", callback_data='leaderboard')],
        [InlineKeyboardButton("Wallet", callback_data='wallet')],
        [InlineKeyboardButton("Airdrop", callback_data='airdrop')],
        [InlineKeyboardButton("Trading", callback_data='trading')],
        [InlineKeyboardButton("Settings", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose an option:", reply_markup=reply_markup)

def play_business_empire(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)
    coins = user[1]
    pph = user[2]

    message = (
        f"🎮 Business Empire Game 🎮\n\n"
        f"Current Coins: {coins}\n"
        f"Profit Per Hour (PPH): {pph}\n\n"
        "Play the game and increase your coins by completing tasks or upgrading!"
    )

    keyboard = [
        [InlineKeyboardButton("Complete Task", callback_data='complete_task')],
        [InlineKeyboardButton("Upgrade Business", callback_data='upgrade_business')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.answer()
    query.edit_message_text(text=message, reply_markup=reply_markup)

def complete_task_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    tasks = get_tasks()
    
    if tasks:
        task_buttons = [[InlineKeyboardButton(f"Task {task[0]}: {task[1]} (Reward: {task[2]} coins)", callback_data=f'complete_task_{task[0]}')] for task in tasks]
        keyboard = task_buttons + [[InlineKeyboardButton("Back to Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.answer()
        query.edit_message_text(text="Choose a task to complete:", reply_markup=reply_markup)
    else:
        query.answer()
        query.edit_message_text(text="No tasks available.")

def complete_task_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    task_id = int(query.data.split('_')[2])  # Extract task ID from callback data
    complete_task(user_id, task_id)
    query.answer()
    query.edit_message_text(text=f"✅ Task {task_id} completed! Reward added.")

def trading(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)
    coins = user[1]

    message = (
        f"💹 Trading Section 💹\n\n"
        f"Current Coins: {coins}\n"
        "You can trade your coins for potential profits!\n\n"
        "Choose an action:"
    )

    keyboard = [
        [InlineKeyboardButton("Buy Asset", callback_data='buy_asset')],
        [InlineKeyboardButton("Sell Asset", callback_data='sell_asset')],
        [InlineKeyboardButton("Back to Menu", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.answer()
    query.edit_message_text(text=message, reply_markup=reply_markup)

def buy_asset(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)
    coins = user[1]

    # Example trading logic
    if coins >= 100:  # Assuming buying an asset costs 100 coins
        update_user(user_id, coins=coins - 100)  # Deduct coins
        message = "✅ You have successfully bought an asset!"
    else:
        message = "❌ Not enough coins to buy an asset."

    query.answer()
    query.edit_message_text(text=message)

def sell_asset(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)
    coins = user[1]

    # Example trading logic
    update_user(user_id, coins=coins + 150)  # Assume selling an asset gives 150 coins
    message = "✅ You have successfully sold an asset!"

    query.answer()
    query.edit_message_text(text=message)

def settings(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    user = get_or_create_user(user_id)
    language = user[4]
    sound_on = "On" if user[5] else "Off"

    keyboard = [
        [InlineKeyboardButton(f"Language: {language}", callback_data='toggle_language')],
        [InlineKeyboardButton(f"Sound: {sound_on}", callback_data='toggle_sound')],
        [InlineKeyboardButton("Play Background Music", callback_data='play_music')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Settings:", reply_markup=reply_markup)

def toggle_language(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    user = get_or_create_user(user_id)
    new_language = 'Hindi' if user[4] == 'English' else 'English'
    update_user(user_id, language=new_language)
    settings(update, context)

def toggle_sound(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    user = get_or_create_user(user_id)
    new_sound = 0 if user[5] else 1
    update_user(user_id, sound_on=new_sound)
    settings(update, context)

def play_music(update: Update, context: CallbackContext) -> None:
    music_file_path = '/mnt/data/WhatsApp Audio 2025-01-16 at 10.09.55_ebc49177.mp3'
    
    with open(music_file_path, 'rb') as audio:
        update.callback_query.message.reply_audio(
            audio=audio, 
            caption="Here is your background music! It will automatically loop. 🎵"
        )

    # Send the same file again after a delay to simulate looping
    context.job_queue.run_once(play_music, 10, context=update)

def leaderboard(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, coins FROM users ORDER BY coins DESC")
    sorted_leaderboard = cursor.fetchall()
    conn.close()

    leaderboard_message = "🏆 Leaderboard 🏆\n\n"
    for index, (user_id, coins) in enumerate(sorted_leaderboard, start=1):
        leaderboard_message += f"{index}. User ID: {user_id} - Coins: {coins}\n"

    update.message.reply_text(leaderboard_message)

# Flask route for Instagram login
@app.route('/instagram/login')
def instagram_login():
    if not INSTAGRAM_CLIENT_ID or INSTAGRAM_CLIENT_ID == 'mohammad':
        return jsonify({"error": "Instagram Client ID is not set or invalid"}), 500

    return redirect(f"https://api.instagram.com/oauth/authorize"
                    f"?client_id={INSTAGRAM_CLIENT_ID}"
                    f"&redirect_uri={REDIRECT_URI}"
                    f"&response_type=code")

@app.route('/instagram/callback')
def instagram_callback():
    code = request.args.get('code')

    if not code:
        return jsonify({"error": "Authorization code missing"}), 400

    response = requests.post('https://api.instagram.com/oauth/access_token', data={
        'client_id': INSTAGRAM_CLIENT_ID,
        'client_secret': INSTAGRAM_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    })

@app.route('/get_instagram_data', methods=['POST'])
def get_instagram_data():
    try:
        response = requests.post('https://api.instagram.com/oauth/access_token', data={...})  # Add actual parameters here
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request to Instagram API failed", "details": str(e)}), 500

    if "error" in data:
        return jsonify({"error": data["error_message"]}), 400

    # Assuming the access token is in the data from Instagram
    access_token = data.get('access_token')
    if access_token:
        instagram_data = fetch_instagram_data(access_token)
        return jsonify(instagram_data)
    else:
        return jsonify({"error": "No access token found"}), 400

def fetch_instagram_data(access_token):
    url = "https://graph.instagram.com/me?fields=id,username&access_token=" + access_token
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to fetch Instagram data", "details": str(e)}

    if "error" in data:
        return {"error": data["error"]["message"]}

    return data

# Run Flask and Telegram bot concurrently
def run_flask():
    app.run(port=5000)

def run_telegram():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

      # Existing handlers for different commands
    dp.add_handler(CommandHandler("start", start))
    
    # Here, add the /menu command handler
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CallbackQueryHandler(play_business_empire, pattern='^play_business_empire$'))  # Business Empire game handler
    dp.add_handler(CallbackQueryHandler(complete_task_handler, pattern='^complete_task$'))  # Complete task handler
    dp.add_handler(CallbackQueryHandler(trading, pattern='^trading$'))  # Trading handler
    dp.add_handler(CallbackQueryHandler(buy_asset, pattern='^buy_asset$'))  # Buy asset handler
    dp.add_handler(CallbackQueryHandler(sell_asset, pattern='^sell_asset$'))  # Sell asset handler
    dp.add_handler(CallbackQueryHandler(settings, pattern='^settings$'))
    dp.add_handler(CallbackQueryHandler(toggle_language, pattern='^toggle_language$'))
    dp.add_handler(CallbackQueryHandler(toggle_sound, pattern='^toggle_sound$'))
    dp.add_handler(CallbackQueryHandler(play_music, pattern='^play_music$'))
    dp.add_handler(CallbackQueryHandler(leaderboard, pattern='^leaderboard$'))

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    run_telegram()
    
