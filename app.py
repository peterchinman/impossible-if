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
    # if we're here we are visiting for the first time

    # click a button to start a game

    # 
    
    return render_template('index.html')

@app.route("/new_game", methods=["GET"])
def new_game():

    # initialize player

    player.initialize(bedroom)
    session['game_state'] = player.game_state

    # redirect to first room

    return redirect(url_for('room', room_slug=session['game_state']['current_room'].slug))


@app.route("/room/<room_slug>", methods=["GET"])
def room(room_slug):

    # update current_room

    current_room = bedroom

    # check events

    # check player alerts

    # prepare for rendering

    return render_template("room.html", bedroom=bedroom)


@app.route("/object/<object_slug>", methods=["GET"])
def object(object_slug):


    for object_name, object_object in bedroom.roomObjects.items():
        if object_name == object_slug:
            return render_template("object.html", roomObject=object_object)
    return ""





@app.route("/stuff/<stuff_slug>/<action_slug>", methods=["GET"])
def action(object_slug, action_slug):

    return render_template("object.html", action=action, object=object)


