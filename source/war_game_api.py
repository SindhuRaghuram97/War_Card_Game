from flask import Flask, request
#from source.war_game import DatabaseManager, Game, Card, Deck, Player
import war_game

app = Flask(__name__)

logs = []
players = []

@app.route('/api/start_game', methods=['POST'])
def api_start_game():
    """
    API endpoint to start a new game.

    :return: JSON response containing the winner's name and number of wins
    """
    if request.method == 'POST':
        return start_game(request.get_json(force=True))

@app.route('/api/get_player_score', methods=['POST'])
def api_get_player_score():
    """
    API endpoint to get a specific player's score.

    :return: JSON response containing the player's name and number of wins
    """
    if request.method == 'POST':
        return get_player_score(request.get_json(force=True))

@app.route('/api/get_player_wins', methods=['GET'])
def get_player_wins():
    """
    API endpoint to get the win counts for all players.

    :return: JSON response containing a list of players and their respective win counts
    """
    if request.method == 'GET':
        return get_wins()

def start_game(user_details):
    """
    Start a new game with the given user details.

    :param user_details: Dictionary containing player1 and player2 names
    :return: Dictionary containing the winner's name and number of wins
    """
    player1_name = user_details["player1"]
    player2_name = user_details["player2"]

    player1 = war_game.Player(player1_name)
    player2 = war_game.Player(player2_name)
    players.append(player1_name)
    players.append(player2_name)
    game = war_game.Game([player1, player2])
    winner = game.play_game()
    logs.append(winner[2])
    return {"winner": winner[0], "wins": winner[1]}

def get_wins():
    """
    Retrieve the win counts for all players.

    :return: Dictionary containing a list of players and their respective win counts
    """
    db_manager = war_game.DatabaseManager()
    db_manager.create_db()
    players = db_manager.get_all_scores()
    return {"player_wins": players}

def get_player_score(player_name):
    """
    Retrieve the win count for a specific player.

    :param player_name: Dictionary containing the player's name
    :return: Dictionary containing the player's name and number of wins
    """
    name = player_name['player_name']
    db_manager = war_game.DatabaseManager()
    db_manager.create_db()
    wins = db_manager.get_player_score(name)
    if wins is None:
        wins = (name, 0)
    return {"wins": wins}

@app.route('/api/get_logs', methods=['GET'])
def api_get_logs():
    """
    API endpoint to get the logs.

    :return: JSON response containing logs if available, otherwise a message indicating no logs are available
    """
    if logs:
        return {"logs": logs[0]}
    else:
        return {"logs": "No logs available"}

@app.route('/api/reset_all_scores', methods=['GET'])
def api_reset_all_scores():
    """
    API endpoint to reset all scores.

    :return: JSON response containing the reset status
    """
    db_manager = war_game.DatabaseManager()
    db_manager.create_db()
    response = db_manager.reset_all_scores()
    app.logger.info(response)
    return {"response": response}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)