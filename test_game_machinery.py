from unittest.mock import patch
from game_machinery import Action, RoomObject, Room, player


#####################
#      Action      
#####################

# Actions affect Player.game_state

# make an Action
def test_Action_init():
   make_bed = Action("Make Bed")
   assert make_bed.name == "Make Bed"

# Make an Action with a requirement that at first isn't met and the is met1
def test_Action_checkRequirements():
   with patch.dict(player.game_state, {}, clear=True):
      bed = RoomObject("bed",
                     "This is your bed.",
                     {},
                     {'bed_made': True})
      make_bed = Action("Make Bed",
                        "",
                        {'bed': {
                           'bed_made': False
                        }})
      
      assert make_bed.checkRequirements() == False

      player.game_state[bed.name]['bed_made'] = False
      assert make_bed.checkRequirements() == True

# Set a requirement that is not contained in player.game_state
def test_Action_checkRequirements_2():
   with patch.dict(player.game_state, {}, clear=True):
      assert player.game_state == {}
      make_bed = Action("Make Bed",
                        "",
                        {'bed': {
                           'bed_made': True
                        }})
      unmake_bed = Action("Make Bed",
                        "",
                        {'bed': {
                           'bed_made': False
                        }})
      assert make_bed.checkRequirements() == False
      assert unmake_bed.checkRequirements() == False

# multiple requirements ALL of which must be met
def test_Action_checkRequirements_AND():
   with patch.dict(player.game_state, {}, clear=True):
         bed = RoomObject("bed",
                        "",
                        {},
                        {'bed_made': False})
         couch = RoomObject("couch",
                        "",
                        {},
                        {'couch_clean': True})
         clean_room = Action("Clean Room",
                           "",
                           {'bed': {
                              'bed_made': False
                           },
                           'couch' : {
                              'couch_clean': False
                           }})
         assert clean_room.checkRequirements() == False

         player.game_state[couch.name]['couch_clean'] = False
         assert clean_room.checkRequirements() == True


# multiple requirements ANY of which must be met
# List of Dicts for Requirements functions as an OR
def test_Action_checkRequirements_OR():
   with patch.dict(player.game_state, {}, clear=True):
         bed = RoomObject("bed",
                        "",
                        {},
                        {'bed_made': False})
         couch = RoomObject("couch",
                        "",
                        {},
                        {'couch_clean': True})
         clean_room = Action("Clean Room",
                           "",
                           [{'bed': {
                              'bed_made': False
                           }},
                           {'couch' : {
                              'couch_clean': False
                           }}])
         assert clean_room.checkRequirements() == True

         player.game_state[bed.name]['bed_made'] = True
         assert clean_room.checkRequirements() == False



# Effect changes player.game_state and fails if requirement is not met
def test_Action_runEffect():
   with patch.dict(player.game_state, {}, clear=True):
      bed = RoomObject("bed",
                     "This is your bed.",
                     {},
                     {'bed_made': True})
      make_bed = Action("Make Bed",
                        "",
                        {'bed': {
                           'bed_made': False
                        }},
                        {'bed': {
                           'bed_made': True,
                           'recently_made' : True
                        }})
      # checkRequirements fails so .runEffects() returns False and does nothing
      assert player.game_state[bed.name]['bed_made'] == True
      assert make_bed.runEffects() == False
      assert player.game_state[bed.name]['bed_made'] == True
      assert player.game_state[bed.name].get('recently_made', False) == False


      # checkRequirements passes so .runEffects() returns True and changes player.game_state
      player.game_state[bed.name]['bed_made'] = False
      assert make_bed.runEffects() == True
      assert player.game_state[bed.name]['bed_made'] == True
      assert player.game_state[bed.name]['recently_made'] == True



#####################
#      RoomObject      
#####################

# stateful description with no states
def test_RoomObject_getStatefulDescription():
   with patch.dict(player.game_state, {}, clear=True):
      bed = RoomObject("Bed",
                     "This is your bed.")
      assert bed.getStatefulDescription() == ["This is your bed."]

# stateful description with states, state change
def test_RoomObject_getStatefulDescription_2():
   with patch.dict(player.game_state, {}, clear=True):
      bed = RoomObject("bed",
                     "This is your bed.",
                     {'bed_made': {
                        True: 'The bed is made.',
                        False: 'The bed is disgusting.'
                     } },
                     {'bed_made': True})
      assert bed.getStatefulDescription() == ["This is your bed.", "The bed is made."]

      player.game_state[bed.name]['bed_made'] = False
      assert bed.getStatefulDescription() == ["This is your bed.", "The bed is disgusting."]

# stateful description using number key with comparison
def test_RoomObject_getStatefulDescription_3():
   with patch.dict(player.game_state, {}, clear=True):
      bed = RoomObject("bed",
                     "This is your bed.",
                     {'bed_made': {
                        True: 'The bed is made.',
                        False: 'The bed is disgusting.'
                        },'number_of_pillows': {
                        '>2': 'You have ample pillows.',
                        '<=2': 'You do not have enough pillows.'
                     } },
                     {'bed_made': True,
                        'number_of_pillows': 3})
      assert bed.getStatefulDescription() == ["This is your bed.", "The bed is made.", "You have ample pillows."]

# test for missing/mismatched state_descriptions & state, trivially passed! good paradigm
def test_RoomObject_getStatefulDescription_4():
   with patch.dict(player.game_state, {}, clear=True):
      bed = RoomObject("bed",
                     "This is your bed.",
                     {'bed_made': {
                        True: 'The bed is made.',
                        False: 'The bed is disgusting.'
                        }},
                     {'number_of_pillows': 3})
      assert bed.getStatefulDescription() == ["This is your bed."]

############################
#   RoomObject w/ Actions      
############################

def test_RoomObject_getActions():
   with patch.dict(player.game_state, {}, clear=True):
      make_bed = Action("Make Bed",
                        "",
                        {'bed': {
                           'bed_made': False
                        }},
                        {'bed': {
                           'bed_made': True
                        }})
      bed = RoomObject("bed",
                     "This is your bed.",
                     {'bed_made': {
                        True: 'The bed is made.',
                        False: 'The bed is disgusting.'
                     } },
                     {'bed_made': False},
                     [make_bed]
                     )
      assert bed.getPossibleActions() == [make_bed]


############################
#   Room      
############################

# minimum init
def test_Room_init():
   with patch.dict(player.game_state, {}, clear=True):
      bedroom = Room("bedroom",
                     "You are standing in your bedroom.")
      assert bedroom.description == "You are standing in your bedroom."

# getDescription with RoomObject.getLink('string')
def test_Room_getDescription():
   with patch.dict(player.game_state, {}, clear=True):
      make_bed = Action("Make Bed",
                        "",
                        {},
                        {})
      my_bed = RoomObject("Your Bed",
                     "This is your bed.",
                     {},
                     {},
                     [make_bed]
                     )
      sliding_doors = RoomObject("Sliding Doors")
      bedroom = Room("bedroom",
                     "You are standing at the foot of {objects['my_bed'].getLink('your bed')}. To your left are {objects['sliding_doors'].getLink('a set of sliding doors')}.",
                     {'my_bed': my_bed,'sliding_doors': sliding_doors}
                     )
      assert bedroom.getDescription() == "You are standing at the foot of <a href='object/your-bed'>your bed</a>. To your left are <a href='object/sliding-doors'>a set of sliding doors</a>."

# getDescription with RoomObject.getStateDescription('state')
def test_Room_getDescription2():
   with patch.dict(player.game_state, {}, clear=True):
      my_bed = RoomObject("Your Bed",
                     "This is your bed.",
                     {'bed_made': {
                        True: 'The bed is made.',
                        False: 'The bed is disgusting.'
                     } },
                     {'bed_made': True})
      bedroom = Room("bedroom",
                     "You are standing at the foot of {objects['my_bed'].getLink('your bed')}. {objects['my_bed'].getStateDescription('bed_made')}",
                     {'my_bed': my_bed}
                     )

      assert bedroom.getDescription() == "You are standing at the foot of <a href='object/your-bed'>your bed</a>. The bed is made."

# getDescription with RoomObject.getStateDescription('state')
def test_Room_getDescription2():
   with patch.dict(player.game_state, {}, clear=True):
      pass


# move from Room to Room
def test_Room_moveToRoom():
   with patch.dict(player.game_state, {}, clear=True):

      

      bedroom = Room("bedroom",
                     "You are standing in your bedroom.")

      bathroom = Room("bathroom",
                      "You are in the bathroom. It is very clean.")
      
      bedroom.connectRoom("east", bathroom)

      player.game_state['current_room'] = bedroom
      player.moveToRoom('east')

      assert player.describeRoom() == "You are in the bathroom. It is very clean."

# move from Room to Room but check if some condition is set.
# add an alert if you are unable to do so
def test_Room_moveToRoom_with_condition():
   with patch.dict(player.game_state, {}, clear=True):

      bedroom = Room("bedroom",
                     "You are standing in your bedroom.")

      bathroom = Room("bathroom",
                      "You are in the bathroom. It is very clean.")
      
      bedroom.connectRoom("east", bathroom, {'inventory': {'key': True}})

      player.game_state['current_room'] = bedroom
      player.moveToRoom('east')
      assert player.getAlerts() == ["You try the handle but the door is locked."]
      assert player.describeRoom() == "You are standing in your bedroom."

      player.game_state['inventory'] = {'key' : True}
      player.moveToRoom('east')


# FUTURE TESTS

# Inventory management


# Picking Up Objects
def test_Player_pickup():
   pass

# Dropping Objects
def test_Player_drop():
   pass

