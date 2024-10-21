# TODO how do I use this?
#use global constants for better error catching
BED = 'bed'

# TODO automatically set up GAME_STATE with default states for each Stuff.

# should GAME_STATE be a class?
GAME_STATE = {
    # current room
    'current_room' : 'bedroom',

    #inventory
    'inventory' : [
        """
        A list of Stuff.
        """
    ],

    # and then here we'll store all the Stuff Values here
    'Stuff' : {
        """
        e.g.    'Stuff-slug' : {
                    'state1' : 'value1',
                    'state2' : 'value2',
                },
        """
    }
}
