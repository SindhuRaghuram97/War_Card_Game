import unittest
from unittest.mock import patch
from source.war_game_flask import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('source.war_game_flask.requests.post')
    def test_start_game(self, mock_post):
        mock_post.return_value.json.return_value = {'winner': 'player1'}
        data = {
            "player1": "player1",
            "player2": "player2"
        }
        response = self.app.post('/start_game', data=data)
        self.assertEqual(response.status_code, 200)

    @patch('source.war_game_flask.requests.get')
    def test_get_player_wins(self, mock_get):
        mock_get.return_value.json.return_value = {'player_wins': {'player1': 5, 'player2': 2}}
        response = self.app.get('/get_player_wins')
        self.assertEqual(response.status_code, 200)

    @patch('source.war_game_flask.requests.get')
    def test_reset_all_scores(self, mock_get):
        mock_get.return_value.status_code = 200
        response = self.app.get('/reset_all_scores')
        self.assertEqual(response.status_code, 200)

    @patch('source.war_game_flask.requests.post')
    def test_get_player_score(self, mock_post):
        mock_post.return_value.json.return_value = {'wins': ['player1', 5]}
        data = {"player_name": "player1"}
        response = self.app.post('/get_player_score', data=data)
        self.assertEqual(response.status_code, 200)

    @patch('source.war_game_flask.requests.get')
    def test_get_logs(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'logs': 'Some logs'}
        response = self.app.get('/get_logs')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
