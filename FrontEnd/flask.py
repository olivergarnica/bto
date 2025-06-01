from flask import Flask, request, jsonify
from flask_cors import CORS
from BlackJack import BlackJack

app = Flask(__name__)
CORS(app)

# Store game instances; in production, use a more robust solution
games = {}

@app.route('/start', methods=['POST'])
def start_game():
    data = request.get_json()
    game_id = str(len(games) + 1)
    num_hands = data.get('num_hands')
    money = data.get('money')
    hit_on_soft = data.get('hit_on_soft', False)

    game = BlackJack(num_decks=1, money=money, hit_on_soft=hit_on_soft)
    game.start_game(num_hands, money)
    games[game_id] = game

    return jsonify({'game_id': game_id, 'message': 'Game started'})

@app.route('/deal', methods=['POST'])
def deal_cards():
    data = request.get_json()
    game_id = data.get('game_id')
    game = games.get(game_id)

    if not game:
        return jsonify({'error': 'Invalid game ID'}), 400

    result = game.deal_initial_cards()
    return jsonify(result)

# Add more routes for actions like hit, stand, etc.

if __name__ == '__main__':
    app.run(debug=True)
