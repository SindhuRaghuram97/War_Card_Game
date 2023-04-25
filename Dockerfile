FROM python:3.8

WORKDIR /python-docker

RUN pip install flask
RUN pip install requests

COPY . .

EXPOSE 8080 8000

WORKDIR /python-docker/source

CMD sh -c "python war_game_api.py & python war_game_flask.py"
