

from cs50 import SQL
from datetime import datetime, timedelta
from flask import Flask, flash, make_response, redirect, render_template, request, session, url_for
from flask_session import Session
from helpers import encode_state, decode_state
from slugify import slugify


# Configure application
app = Flask(__name__)
app.secret_key = 'c0f9c9533444660bd9686d841d59c4a6fe3dc8b849fc03da8647587bd3e2681a' # REPLACE THIS
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
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def game():
    # get state

    session.setdefault('GAME_STATE', {})

    # update state

    # render
    

    return render_template(room + '.html')
    

@app.route("/stuff/<stuff_slug>", methods=["GET"])
def object(stuff_slug):

    # How do I get specific object now
    # specific_object = objects[object_slug]

    # TODO update state


    return render_template ("object.html", object=specific_object)

@app.route("/stuff/<stuff_slug>/<action_slug>", methods=["GET"])
def action(object_slug, action_slug):

    # encoded_state = request.args.get('state')
    # if encoded_state:
    #     state = decode_state(encoded_state)
    # else:
    #     return render_template('error.html')

    # action = objects[object_slug]['actions'][action_slug]
    # object = objects[object_slug]

    # if 'causes' in action:
    #     for object_name, state_changes in action['causes'].items():
    #         for state_change_name, state_change_value in state_changes.items():
    #             state[object_name][state_change_name] = state_change_value
            

    # encoded_state = encode_state(state)

    return render_template("object.html", action=action, object=object)


