import unittest
from unittest.mock import patch

import war_game
from source.war_game_api import app

class war_game_api_test(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('source.war_game_api.start_game')
    def test_api_start_game(self, mock_start_game):
        mock_start_game.return_value = {"winner": "player1", "wins": 1}
        response = self.client.post('/api/start_game', json={"player1": "Alice", "player2": "Bob"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"winner": "player1", "wins": 1})

    @patch('source.war_game_api.get_wins')
    def test_api_get_player_wins(self, mock_get_wins):
        mock_get_wins.return_value = {"player_wins": [{"name": "Alice", "wins": 2}, {"name": "Bob", "wins": 1}]}
        response = self.client.get('/api/get_player_wins')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"player_wins": [{"name": "Alice", "wins": 2}, {"name": "Bob", "wins": 1}]})


    @patch('source.war_game_api.get_player_score')
    def test_get_player_score(self, mock_get_player_score):
        mock_get_player_score.return_value = {"wins": ["Alice", 1]}
        response = self.client.post('/api/get_player_score', json={"player_name": "Alice"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"wins": ["Alice", 1]})

    @patch('source.war_game_api.logs')
    def test_api_get_logs_no_logs(self, mock_logs):
        mock_logs.__bool__.return_value = False
        response = self.client.get('/api/get_logs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"logs": "No logs available"})

    @patch.object(war_game.DatabaseManager, 'create_db')
    @patch.object(war_game.DatabaseManager, 'reset_all_scores')
    def test_reset_all_scores(self, mock_api_reset_all_scores, db_manager_mock):
        mock_api_reset_all_scores.return_value = [{"name": "Alice", "wins": 2}, {"name": "Bob", "wins": 1}]
        response = self.client.get('/api/reset_all_scores')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"response": [{"name": "Alice", "wins": 2}, {"name": "Bob", "wins": 1}]})

if __name__ == '__main__':
    unittest.main()
