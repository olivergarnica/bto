from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
from BlackJack import BlackJack
from User import User

app = Flask(__name__, static_folder='.')
# CORS(app)  # Enable CORS if running frontend separately

game_instances = {}  # simple in-memory store

@app.route("/")
def index():
    return send_from_directory('.', 'game.html')

@app.route("/start", methods=["POST"])
def start_game():
    data = request.get_json()
    num_hands = data.get("num_hands")
    money = data.get("money")

    if not (1 <= num_hands <= 4):
        return jsonify({"error": "Number of hands must be between 1 and 4"}), 400
    if not (10 <= money <= 10000):
        return jsonify({"error": "Money must be between 10 and 10000"}), 400

    game = BlackJack()
    game.user = User(num_hands, money)
    game_id = "game_1"  # or use session/user-specific ID
    game_instances[game_id] = game

    return jsonify({
        "message": "Game started",
        "num_hands": num_hands,
        "money": money
    })

if __name__ == "__main__":
    app.run(debug=True)