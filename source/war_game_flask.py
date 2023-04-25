from flask import Flask, render_template, request, send_file
import requests
import json
import os

# Create a Flask app instance
app = Flask(__name__)
players = []
flags = []

def render_index(**kwargs):
    return render_template('index.html', **kwargs)


def handle_response(response, success_message, error_message):
    if response.status_code == 200:
        return success_message
    else:
        return error_message

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the game and get the winner
@app.route('/start_game', methods=['POST'])
def start_game():
    """
    Start a new game and determine the winner.

    :return: Rendered HTML template of index.html with start_game_flag, method_called, and winner
    """
    player1 = request.form['player1']
    player2 = request.form['player2']
    players.append(player1)
    players.append(player2)
    user_details = {'player1': player1, 'player2': player2}
    url = "http://localhost:8080/api/start_game"
    response = requests.post(url=url, data=json.dumps(user_details))
    json_resp = response.json()
    winner = json_resp['winner']
    method_called = False # Used to control the display of certain responses
    flags.append(True)
    return render_index(start_game_flag=True, method_called=method_called, winner=winner)

# Route to get the scores for all the players
@app.route('/get_player_wins', methods=['GET'])
def get_player_wins():
    """
    Retrieve the win counts for all players.

    :return: Rendered HTML template of index.html with get_scores_flag, method_called, player_wins, and output
    """
    output = "The Game Board is empty. Start a new game!"
    url = "http://localhost:8080/api/get_player_wins"
    response = requests.get(url=url)
    if response.status_code == 200 and len(flags) > 0:
        json_resp = response.json()
        player_wins = json_resp['player_wins']
        app.logger.info(player_wins)
        if len(player_wins) > 0:
            return render_index(get_scores_flag=True, method_called=False, player_wins=player_wins)
    return render_index(get_scores_flag=True, method_called=False, output=output)

# Route to reset the game
@app.route('/reset_all_scores', methods=['GET'])
def reset_all_scores():
    """
    Reset scores for all players.

    :return: Rendered HTML template of index.html with reset_scores_flag, method_called, and message
    """
    url = "http://localhost:8080/api/reset_all_scores"
    response = requests.get(url=url)
    message = handle_response(response, "The Game Board has been reset.", "There was an error in resetting the Game Board.")
    return render_index(reset_scores_flag=True, method_called=False, message=message)

# Route to get the score for a specific player
@app.route('/get_player_score', methods=['POST'])
def get_player_score():
    """
    Get the score of a specific player.

    :return: Rendered HTML template of index.html with player_score_flag, player_score, player_name, and method_called
    """
    player_name = request.form['player_name']
    query_param = {'player_name': player_name}
    url = "http://localhost:8080/api/get_player_score"
    response = requests.post(url=url, data=json.dumps(query_param))
    json_resp = response.json()
    player_score = json_resp['wins']
    return render_index( player_score_flag=True, player_score=player_score, player_name=player_name,
                           method_called=False)

# Route to get the logs of the most recent game played
@app.route('/get_logs', methods=['GET'])
def get_logs():
    """
    Retrieve the game logs and provide them as a file download.

    :return: Rendered HTML template of index.html with logs, method_called, filename, and output_message, or file download
    """
    output_message = "A game has not been played so there are no logs at this time.\nPlease play a game before fetching its logs!"
    if len(flags) > 0:
        url = "http://localhost:8080/api/get_logs"
        response = requests.get(url=url)
        if response.status_code == 200:
            json_resp = response.json()
            data = json_resp['logs']
            foldername = "War Game Logs"
            if not os.path.exists(foldername):
                os.makedirs(foldername)
            path = os.path.abspath(foldername)
            if os.path.exists(path):
                os.chdir(path)
                filename = 'War_Game_Logs.txt'
                new_path = os.path.join(path, filename)
                with open(new_path, 'w') as file:
                    for line in data:
                        file.write("%s\n" % line)
                os.chdir('..')
            return send_file(os.path.join(path, filename), as_attachment=True)
        else:
            return render_index(logs=True, method_called=False, filename="", output_message=output_message)
    else:
        return render_index(logs=True, method_called=True, filename="", output_message=output_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
