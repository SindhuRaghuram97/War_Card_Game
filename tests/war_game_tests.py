import unittest
from unittest.mock import patch
import os
from source.war_game import Card, Deck, Player, DatabaseManager, Game
import tempfile


class TestDatabaseManager(unittest.TestCase):

    def test_ensure_directory_exists(self):
        with tempfile.TemporaryDirectory() as test_data_directory:
            test_db_path = os.path.join(test_data_directory, "player_wins.db")
            db_manager = DatabaseManager(test_db_path)
            self.assertTrue(os.path.exists(test_data_directory))

    @patch('sqlite3.connect')
    def test_create_db(self, mock_connect):
        with tempfile.TemporaryDirectory() as test_data_directory:
            test_db_path = os.path.join(test_data_directory, "player_wins.db")
            db_manager = DatabaseManager(test_db_path)
            mock_connect.assert_called_with(test_db_path)

    def test_get_player_score(self):
        with tempfile.TemporaryDirectory() as test_data_directory:
            test_db_path = os.path.join(test_data_directory, "player_wins.db")
            db_manager = DatabaseManager(test_db_path)
            db_manager.update_score("Alice")
            player_score = db_manager.get_player_score("Alice")
            self.assertEqual(player_score, ("Alice", 1))

    def test_update_score(self):
        with tempfile.TemporaryDirectory() as test_data_directory:
            test_db_path = os.path.join(test_data_directory, "player_wins.db")
            db_manager = DatabaseManager(test_db_path)
            db_manager.update_score("Alice")
            player_score = db_manager.get_player_score("Alice")
            self.assertEqual(player_score, ("Alice", 1))
            db_manager.update_score("Alice")
            player_score = db_manager.get_player_score("Alice")
            self.assertEqual(player_score, ("Alice", 2))

    def test_get_all_scores(self):
        with tempfile.TemporaryDirectory() as test_data_directory:
            test_db_path = os.path.join(test_data_directory, "player_wins.db")
            db_manager = DatabaseManager(test_db_path)
            db_manager.update_score("Alice")
            db_manager.update_score("Bob")
            db_manager.update_score("Alice")
            all_scores = db_manager.get_all_scores()
            self.assertEqual(all_scores, [{"name": "Alice", "wins": 2}, {"name": "Bob", "wins": 1}])

    def test_reset_all_scores(self):
        with tempfile.TemporaryDirectory() as test_data_directory:
            test_db_path = os.path.join(test_data_directory, "player_wins.db")
            db_manager = DatabaseManager(test_db_path)
            db_manager.update_score("Alice")
            db_manager.update_score("Bob")
            db_manager.update_score("Alice")
            reset_scores = db_manager.reset_all_scores()
            self.assertEqual(reset_scores, [{"name": "Alice", "wins": 2}, {"name": "Bob", "wins": 1}])
            all_scores = db_manager.get_all_scores()
            self.assertEqual(all_scores, [])


class TestCard(unittest.TestCase):
    def test_card_str(self):
        card = Card(2, 'Hearts')
        self.assertEqual(str(card), '2 of Hearts')

class TestDeck(unittest.TestCase):
    def test_deck_initialization(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    @patch('source.war_game.random.shuffle')
    def test_deck_shuffle(self, mock_shuffle):
        deck = Deck()
        deck.shuffle()
        mock_shuffle.assert_called_with(deck.cards)

    def test_deck_deal(self):
        deck = Deck()
        card = deck.deal()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), 51)

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player('Stefan')
        self.assertEqual(player.name, 'Stefan')
        self.assertEqual(player.hand, [])
        self.assertEqual(player.wins, 0)

    @patch('source.war_game.logs')
    def test_player_play_card(self, mock_logs):
        player = Player('Stefan')
        card = Card(2, 'Hearts')
        player.hand.append(card)
        result = player.play_card()
        self.assertEqual(result, [card, 'Stefan'])
        mock_logs.append.assert_called_with('Stefan has 1 cards')

    def test_player_add_cards(self):
        player = Player('Stefan')
        cards = [Card(2, 'Hearts'), Card(3, 'Hearts')]
        player.add_cards(cards)
        self.assertEqual(player.hand, cards)

class TestGame(unittest.TestCase):
    def test_game_initialization(self):
        players = [Player('Stefan'), Player('Damon')]
        game = Game

if __name__ == '__main__':
    test_suite = unittest.TestLoader().discover('..', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(test_suite)
