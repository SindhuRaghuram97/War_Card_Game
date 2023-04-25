# War Card Game

This repository contains the implementation of the classic card game "War" using Python, Flask, Docker and SQLite. The game is playable through a web interface, and the backend is powered by a RESTful API.

## Game Rules

The goal of War is to be the first player to win all 52 cards.

### The Deal

The deck is divided evenly, with each player receiving 26 cards, dealt one at a time, face down. Anyone may deal first. Each player places their stack of cards face down, in front of them.

### The Play

Each player turns up a card at the same time, and the player with the higher card takes both cards and puts them, face down, on the bottom of their stack.

If the cards are the same rank, it is War. Each player turns up one card face down and one card face up. The player with the higher cards takes both piles (six cards). If the turned-up cards are again the same rank, each player places another card face down and turns another card face up. The player with the higher card takes all 10 cards, and so on.

### How to Keep Score

The game ends when one player has won all the cards.

## Project Structure

This project has the following files in the `source` folder:

- `war_game.py`: Contains the code to play the card game "War" and stores the results of each game in the `player_wins.db` SQL database.
- `war_game_api.py`: Provides APIs for starting a game, getting player scores, getting wins of a particular player, fetching game logs, and resetting all players' scores. The associated port is 8080.
- `war_game_flask.py`: Creates the web interface with buttons for each API and makes corresponding calls upon a click. The associated port is 8000.

The `tests` folder contains unit tests for each file.

## Docker Setup

A Dockerfile is provided to build a Docker image of the game. The Dockerfile has the following content:

```Dockerfile
FROM python:3.8

WORKDIR /python-docker

RUN pip install flask
RUN pip install requests

COPY . .

EXPOSE 8080 8000

WORKDIR /python-docker/source

CMD sh -c "python war_game_api.py & python war_game_flask.py"
```

## Getting Started

To run the game using Docker, follow these steps:

1. Pull the Docker image:

```bash
docker pull sindhuraghuram97/war-game:latest
```

2. Run the Docker container:

```bash
docker run
```

3. Access the game in your web browser by navigating to:

```
http://localhost:8000
```

Enjoy the game!
