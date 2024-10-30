from cs50 import SQL
from datetime import datetime, timedelta
from flask import Flask, flash, make_response, redirect, render_template, request, session, url_for
from flask_session import Session
from game_machinery import player
from game_map import *


# Configure application
app = Flask(__name__)
app.secret_key = 'asdfghjk' # REPLACE THIS
app.config['TEMPLATES_AUTO_RELOAD'] = True # turn off for production
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # set higher for production
if (__name__ == "__main__"):
    app.run(debug=True)

# Configure session to use filesystem (instead of signed cookies)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///impossible.db")


@app.after_request
def after_request(response):
    """
    Ensure responses aren't cached
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    # Home page, right now consists of a link to /new_game
    
    return render_template('index.html')

@app.route("/new_game", methods=["GET"])
def new_game():

    # initialize player
    player.initialize(bedroom)

    # save to session
    session['game_state'] = player.game_state

    room = player.game_state['current_room']

    # redirect to first room
    return redirect(url_for('room', room_slug=room.slug))


@app.route("/room/<room_slug>", methods=["GET"])
def room(room_slug):

    # load player from session
    player.game_state = session['game_state']

    room = player.game_state['current_room']

    # check events
    # TODO implement events

    # pop player alerts
    alerts = player.getAlerts()

    return render_template("room.html", alerts=alerts, room=room)

@app.route("/room/<room_slug>/move-to/<to_slug>", methods=["GET"])
def move_to(room_slug, to_slug):
    pass
    # check if move to to_slug is valid

    # if yes redirect to /room/<to_slug>

    # if no, send back to /room/room_slug
    # w/ possible alert?


@app.route("/object/<object_slug>", methods=["GET"])
def object(object_slug):
    # HTMX OBJECT INSPECTION LOADER

    # load player from session
    player.game_state = session['game_state']

    room = player.game_state['current_room']

    if object_slug in room.roomObjects:
        roomObject = room.roomObjects[object_slug]
        return render_template("object.html", roomObject=roomObject)
    else:
        return ""


@app.route("/object/<object_slug>/action/<action_slug>", methods=["GET"])
def action(object_slug, action_slug):
    pass




