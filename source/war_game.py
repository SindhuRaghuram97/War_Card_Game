import random
import sqlite3
import os
import logging
from typing import List, Dict, Union

# Configure the logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

logs = []

class DatabaseManager:
    def __init__(self, db_path: str = "data/player_wins.db"):
        self.db_path = os.path.abspath(db_path)
        self.ensure_directory_exists()
        self.create_db()

    def ensure_directory_exists(self):
        """
        Ensure the directory containing the database file exists.
        """
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        logger.info("Directory checks done!")

    def create_db(self):
        """
        Create the database table if it does not exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS PlayerWins (Name text, Wins int);')
            conn.commit()
            logger.info("Database and table checks done!")

    def get_player_score(self, player_name: str) -> Union[tuple, None]:
        """
        Get the player's score from the database.

        :param player_name: The name of the player.
        :return: A tuple containing the player's name and score or None if not found.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM PlayerWins WHERE Name = ?', (player_name,))
            data = c.fetchone()
        return data

    def update_score(self, winner_name: str) -> None:
        """
        Update the score for the given winner.

        :param winner_name: The name of the winner.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM PlayerWins WHERE Name = ?', (winner_name,))
            data = c.fetchone()
            if data:
                c.execute('UPDATE PlayerWins SET Wins = Wins + 1 WHERE Name = ?', (winner_name,))
            else:
                c.execute('INSERT INTO PlayerWins VALUES (?,?)', (winner_name, 1))
            conn.commit()
            logger.info("Database updated.")

    def get_all_scores(self) -> List[Dict[str, Union[str, int]]]:
        """
        Get all player scores from the database.

        :return: A list of dictionaries containing player names and their scores.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM PlayerWins')
            data = c.fetchall()

        players = [{'name': row[0], 'wins': row[1]} for row in data]
        return players

    def reset_all_scores(self) -> List[Dict[str, Union[str, int]]]:
        """
        Reset all scores in the database and return the reset scores.

        :return: A list of dictionaries containing player names and their reset scores.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM PlayerWins')
            data = c.fetchall()
            players_check = [{'name': row[0], 'wins': row[1]} for row in data]
            c.execute('DELETE FROM PlayerWins;')
            conn.commit()
        return players_check

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    def __init__(self):
        self.cards = []
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in range(2, 15):
                self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self):
        """
        Shuffle the cards in the deck.
        """
        random.shuffle(self.cards)

    def deal(self):
        """
        Deal one card from the deck.

        :return: A card object
        """
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.wins = 0

    def play_card(self):
        """
        Play a card from the player's hand.

        :return: A list containing the card played and the player's name
        """
        log_entry = self.name + " has " + str(len(self.hand)) + " cards"
        logger.info(log_entry)
        logs.append(log_entry)
        card = self.hand.pop()

        return [card, self.name]

    def add_cards(self, cards):
        """
        Add cards to the player's hand.

        :param cards: A list of card objects
        """
        self.hand.extend(cards)


class Game:
    def __init__(self, players):
        """
        Initialize a Game object.

        :param players: List of Player objects participating in the game.
        """
        self.players = players
        logs = []
        self.deck = Deck()
        log_entry = f"Deck size: {len(self.deck.cards)}"
        logger.info(log_entry)
        logs.append(log_entry)
        self.deal_cards()
        self.db_manager = DatabaseManager()


    def deal_cards(self):
        """
        Deal cards to each player.
        """
        for _ in range(26):
            for player in self.players:
                card = self.deck.deal()
                player.hand.append(card)

    def players_play_card(self):
        """
        Get the cards played by the players.

        :return: A list of cards played by the players
        """
        cards_played = []
        for player in self.players:
            play_card_result = player.play_card()
            card_play = play_card_result[0]
            cards_played.append(card_play)
            log_entry = str(play_card_result[1]) + " played " + str(card_play.rank) + ". Total cards left = " + str(
                len(player.hand))
            logger.info(log_entry)
            logs.append(log_entry + "\n")
        return cards_played

    def play_round(self):
        """
        Play a round of the game and update the players' hands.

        :return: The player object who won the round
        """
        cards_played = self.players_play_card()
        ranks_played = [card.rank for card in cards_played]

        if len(set(ranks_played)) == 1:
            winner = self.resolve_war(cards_played, ranks_played)
        else:
            winner = self.players[ranks_played.index(max(ranks_played))]
            winner.add_cards(cards_played)
            log_entry = f"{winner.name} won {len(cards_played)} cards.\n"
            logger.info(log_entry)
            logs.append(log_entry)

        return winner

    def resolve_war(self, cards_played, ranks_played):
        logger.info('War!')
        logs.append('\nWar!\n')
        while len(set(ranks_played)) == 1:
            cards_played.extend(self.players_play_card())
            new_cards = self.players_play_card()
            cards_played.extend(new_cards)
            ranks_played = [card.rank for card in new_cards]
            if len(set(ranks_played)) != 1:
                logger.info('War continued!')
                logs.append('\nWar continued!\n')

        winner = self.players[ranks_played.index(max(ranks_played))]
        winner.add_cards(cards_played)
        log_entry = f"{winner.name} won {len(cards_played)} cards.\n"
        logger.info(log_entry)
        logs.append(log_entry)
        return winner

    def play_game(self):
        """
        Play the game and update the players' scores.

        :return: A tuple containing the winner's name, the number of wins, and a list of logs.
        """

        logs.append(f"{self.players[0].name} has {len(self.players[0].hand)} cards.")
        logs.append(f"{self.players[1].name} has {len(self.players[1].hand)} cards.")
        logger.info(logs[-2])
        logger.info(logs[-1])

        round_count = 0

        try:
            while all(player.hand for player in self.players):
                round_count += 1
                print(f'\nRound {round_count} -')
                logs.append(f"\nRound {round_count} -")
                self.play_round()
        except IndexError:
            print("A player's deck is empty")
            logs.append("\nA player's deck is empty")

        for player in self.players:
            logs.append(f"{player.name} has {len(player.hand)}")

        winner = max(self.players, key=lambda player: len(player.hand))
        winner.wins += 1
        log_winner = f"Winner: {winner.name}"
        log_wins = f"Wins: {winner.wins}"
        logger.info(log_winner)
        logger.info(log_wins)
        logs.append("\n" + log_winner)
        logs.append(log_wins)
        self.db_manager.update_score(winner.name)
        player_score = self.db_manager.get_player_score(winner.name)[1]
        log_end = f'\nGame Over!\n{winner.name} won the game with {player_score} total wins'
        print(log_end)
        logs.append("\n" + log_end)
        return winner.name, winner.wins, logs

