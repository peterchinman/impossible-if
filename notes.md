
TEMPLATE

Records current state for all Stuff
```
state : {
    current_room : bedroom,
    rooms_visited : [bedroom,],

    # should inventory be it's own thing
    # or do objects store a state of 'in_inventory' = True;

    object1 : {
        state : value,
    },
}
```

```
Stuff : {

    # Display Stuff
    name : Name,
    slug : slugify(name),
    description : Description,

    # A list of states and descriptions.
    # The descriptions are appeneded after the main description.
    state_descriptions : {
        state_1 : {
            value : "Description.",
            value : "Description.",
        },  
    }

    # Should we record WHERE the stuff is? e.g. "ON beside table", "UNDER bed"? So that it can be moved? 

    actions : {
        action 1 : {
            slug : action-1
            description: description
            requires : {
                1 : {
                    object: object_name,
                    state: state_name,
                    value: value_name,
                }
                
            }
            causes : {
                object_2 : {
                    state_1 : value
                },
            }
        }
    }
}

```

Maybe Stuff should have... properties? e.g. both knife and sword "can_cut", and so a paper door would have the requirement of inventory.has_property(can_cut)

When we enter a room:
1. Check current state.
2. Run room Actions:
   a. Check Requires, run Causes.
3.

So, when an Object gets clicked:
1. check it's Current State
2. check if each actions Requirements have been met

When an Action gets clicked:
1. update each state change it Causes


def run_actions(thing):
    for action in thing.actions:
        requirements_met = True
        for r in requires:
            thing = r.thing
            state = r.state
            value = r.value
            if CURRENT_STATE.thing.state != r.state.value
                requirements_met == False
                break
        if requirements_met:
            for c in thing.causes:
                thing = c.thing
                state = c.state
                value = c.value
                CURRENT_STATE.thing.state = value

# What about cascading actions?
# Every time a state changes we should re-check state for whole room, until state stops changing.
# Need to think about loops.

OLD OBJECT DICTS

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

objects = {
    'bed' : {
        'name' : 'Your bed',
        # 'slug' : slugify
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
