from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is your Flask app with a favicon!"

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
