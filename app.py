

from cs50 import SQL
from datetime import datetime, timedelta
from flask import Flask, flash, make_response, redirect, render_template, request, session, url_for
from flask_session import Session
from helpers import encode_state, decode_state


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


initial_state = {
    'bed' : {
        'bed_made' : True,
    },
    'sliding_door' : {
        'open' : True,
        'painted_over' : True,
    },
    'inventory' : [
        'knife',
        'tarot cards',
    ],
    'current_room' : 'bedroom',
    'rooms_visited' : [],
}




#   object template
#   'object' : {
#       'name' : Name,
#       'slug' : slug,
#       'description' : Description,
#       'possible_states' : {
#           'state_1' : {
#               True : "Description.",
#               False : "Description.",
#           },  
#        }
#       'actions' : {
#           'action 1' : {
#               'slug' : action-1
#                'description': 
#               'requires' : {
#                   'state_1' : True
#                }
#               'causes' : {
#                   'state_2' : False
#               }
#           }
#       
#  
#       }
#
#
# }


objects = {
    'bed' : {
        'name' : 'Your bed',
        'slug' : 'bed',
        'description' : "A queen-size bed with a floral duvet. You've had the mattress for years and it is starting to sag a little in the middle.",
        'possible_states' : {
            'bed_made' : {
                True : "The bed is neatly made.",
                False : "The bed is disheveled.",
            },
        },
        'actions' : {
            'lay_in_bed' : {
                'name' : "Lay in bed",
                'slug' : 'lay_in_bed',
                'description' : "You sprawl across the bed, luxuriously.",
                'causes' : {
                    'bed' : {
                        'bed_made' : False,
                        'sleepy' : False,
                    },
                },
            },
            'look_underneath_bed' : {
                'name' : 'look underneath bed',
                'slug' : 'look_underneath_bed'
            },
            'make_bed' : {
                'name' : 'make bed',
                'slug' : 'make_bed',
                'description' : 'You make the bed with an air of moral superiority.',
                'requires' : {
                    'bed' : {
                        'bed_made' : False,
                    },
                },
                'causes' : {
                    'bed' : {
                        'bed_made' : True,
                    }
                }
            }
        },
    
    },
    'sliding_door' : {
        'name' : 'Sliding Door',
        'slug' : 'sliding_door',
        'possible_states' : {
            'open' : {
                True : "The doors are open. Thru them you can see <a href='/room/living-room' class='place'>the living room</a>.",
                False : "The doors are closed."
            },
            'painted_over' : {
                True : "The doors seem to have once slid open and closed on a metal track, but your landlord has slathered so many layers of white paint over them that they are now, permanently, open.",
                False : "The doors have been freed from their landlord-imposed paint-bondage."
            }
        },
        'actions' : {
            'close doors' : {
                'slug': 'close-doors',
                'description': 'With great effort, you get the doors to slide closed.',
                'requires' : {
                    'sliding_door' : {
                        'painted_over' : False
                    }
                }
            }
        }
    }
}


@app.route("/", methods=["GET"])
def game():
    encoded_state = request.args.get('state')
    if encoded_state:
        state = decode_state(encoded_state)
    else:
        state = initial_state

    room = state['current_room']
    
    encoded_state = encode_state(state)

    return render_template(room + '.html', objects=objects, state=state, encoded_state=encoded_state)
    

@app.route("/object/<object_slug>", methods=["GET"])
def object(object_slug):

    encoded_state = request.args.get('state')
    if encoded_state:
        state = decode_state(encoded_state)
    else:
        state = initial_state

    specific_object = objects[object_slug]

    # TODO update state

    encoded_state = encode_state(state)

    return render_template ("object.html", object=specific_object, state=state, encoded_state=encoded_state)

@app.route("/object/<object_slug>/<action_slug>", methods=["GET"])
def action(object_slug, action_slug):

    encoded_state = request.args.get('state')
    if encoded_state:
        state = decode_state(encoded_state)
    else:
        return render_template('error.html')

    action = objects[object_slug]['actions'][action_slug]
    object = objects[object_slug]

    if 'causes' in action:
        for object_name, state_changes in action['causes'].items():
            for state_change_name, state_change_value in state_changes.items():
                state[object_name][state_change_name] = state_change_value
    

            

    encoded_state = encode_state(state)

    return render_template("object.html", action=action, object=object, state=state, encoded_state=encoded_state)


