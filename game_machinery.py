from slugify import slugify
from player import Player

player = Player()



class Action:
   """
   Actions belong to RoomObjects. They do things.
   """
   def __init__(self, name, description = None, requirements = None, effects = None) -> None:
      """
      Initialize the class with given attributes.

      Args:
         name (string): display name, e.g. "Make Bed"

         description (string)(optional): Describe the action. Should probably be subjunctive. e.g. "You could tuck in all the corners, and make the bed look great."

         requirements(dict or list): can either be an individual dict in the form of:
               {'RoomObject_name': {
                  state_name : state_value
               },
               # include further requirements if any
               }
         OR it can be a list of such requirements, e.g.:
            [
            {'RoomObject_name': {
                  state_name : state_value
            }},
            {'RoomObject_2_name': {
                  state_name : state_value
            }}
            ]
         If ANY of the requirement dicts in the list are met, then checkRequirements returns True. I.e. LIST FUNCTIONS AS OR. INDIVIDUAL DICT FUNCTIONS AS AND.

         effects: dicts of effects in the form of
            {'RoomObject_name' : {
               'state_name': 'state_value'
            },
            # include further effects if any 
            }
      """
      self.name = name
      self.description = description
      self.requirements = requirements
      self.effects = effects

   def _check_single_dict_of_requirement(self, requirement):
      """
      Checks a single dict of requirements and returns whether all of its conditions have been met.
      """
      for room_object, requirement_states in requirement.items():
         for requirement_state_name, requirement_state_value in requirement_states.items():
            if room_object in player.game_state and requirement_state_name in player.game_state[room_object]:
               if player.game_state[room_object][requirement_state_name] != requirement_state_value:
                  return False
            else:
               return False
      return True


   def checkRequirements(self):
      """
      SINGLE DICT functions as AND
      LIST of DICTS functions as OR
      """

      if self.requirements:
         if isinstance(self.requirements, dict):
            return self._check_single_dict_of_requirement(self.requirements)
            
         if isinstance(self.requirements, list):
            for requirement in self.requirements:
               if self._check_single_dict_of_requirement(requirement) == True:
                  return True
            return False  
      else:
         return True
   
   def runEffects(self):
      if self.checkRequirements() == False:
         return False
      for room_object, effect_states in self.effects.items():
         # Ensure room_object exists in player.game_state, or add it as an empty dictionary
         player.game_state.setdefault(room_object, {})
         for effect_state_name, effect_state_value in effect_states.items():
            # Ensure the effect_state_name exists in the room_object, or set a default value
            player.game_state[room_object].setdefault(effect_state_name, effect_state_value)
            
            # Apply the effect (or update the state) in the player.game_state
            player.game_state[room_object][effect_state_name] = effect_state_value

      return True            
         


class RoomObject:
   def __init__(self, name, description = None, state_descriptions = None, initial_states = None, Actions = None) -> None:
      self.name = name
      
      self.description = description
      self.state_descriptions = state_descriptions
      self.initial_states = initial_states
      self.Actions = Actions


      self.slug = slugify(name)
      self.link = f"<a href='object/{self.slug}'>{self.name}</a>"

      # empty init a dict in player.game_state
      # TODO should this use self.name vs an ID??
      player.game_state[self.name] = {}
      if self.initial_states:
         for state_name, state_value in self.initial_states.items():
            player.game_state[self.name][state_name] = state_value

   def getStatefulDescription(self):
      """
      Returns a list of descriptions, starting with the RoomObject's description, and then with each applicable state_description appended.

      State_descriptions can currently be:
         1. Booleans -- evaluated directly against the value recorded in player.game_state[self.name][state_name]
         2. Comparison Strings -- appended to to the value in player.game_state[self.name][state_name] and evaluated.
            So, e.g. if the value of "number_of_pillows" is 3, and the state_description key is ">2", it will evaluate 3>2.
      """
      stateful_description = [self.description]

      if self.state_descriptions:
         for state_name, condition_and_description in self.state_descriptions.items():
            if state_name in player.game_state[self.name]:
               for condition, description in condition_and_description.items():
                  state_value = player.game_state[self.name][state_name]

                  # if boolean, direct comparison
                  if isinstance(condition, bool):
                     if state_value == condition:
                        stateful_description.append(description)
                  
                  # if condition is a string (e.g, ">2"), evaluate it dynamically
                  elif isinstance(condition, str):
                     # construct the comparison
                     expression = f'{state_value}{condition}'
                     if eval(expression):
                        stateful_description.append(description)

      return stateful_description
   
   def getPossibleActions(self):
      possibleActions = []
      for action in self.Actions:
         if action.checkRequirements():
            possibleActions.append(action)
      return possibleActions
   

class Room:
   def __init__(self, name, description = None, roomObjects = None, connections = None):
      """
      Args:
         name (string)
         description (string): 
            can include {} formatted references to RoomObjects in the Room. e.g. "You are standing at the foot of your {bed.link}."
         roomObjects (dict):
            weirdly and annoying this is a dict in the form of:
            {'bed': bed}
            where bed is a roomObject and 'bed' is however you are referring to it in the description
      """
      self.name = name
      self.description = description
      self.roomObjects = roomObjects
      self.connections = connections if connections else {}

   def getDescription(self):
      # Format the description, replacing placeholders with object links
      return self.description.format(**(self.roomObjects or {}))

   def connectRoom(self, direction, room, requirement=None):
      """
      Connect this room to another room in a given direction.
      
      Args:
         direction (str): The direction of the connection (e.g., 'north', 'east').
         room (Room): The room to connect to.
         requirement (func): A function that returns True/False based on whether the connection is allowed.
      """
      self.connections[direction] = {'room': room, 'requirement': requirement}

   def getConnectedRoom(self, direction, player):
      connection = self.connections.get(direction)
      if connection:
         if connection['requirement'] is None:
            return connection['room']
         for requirement_object, requirement_condition in connection['requirement'].items():
            if player.game_state.get(requirement_object):
               for state_name, state_value in requirement_condition.items():
                  if player.game_state[requirement_object][state_name] == state_value:
                     return connection['room']
      return None





   
