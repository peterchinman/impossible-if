class Player:
   def __init__(self, start_Room = None, start_inventory = None) -> None:
      """
      Player.games_state is a dict that stores all the values unique to the current play_thru:
      1. {'current_room' : Room}
      2. {'inventory' : {'key': True, 'matches': 6}}
      3. {'RoomObject.name': {state_name: state_value}}
      4. {'Room.name': {state_name: state_value}}
      5. {'alerts' : ["list", "of", "alerts"]}
      """
      self.game_state = {}
      self.game_state['current_room'] = start_Room
      self.game_state['inventory'] = start_inventory if start_inventory else {}
      self.game_state['alerts'] = []

   def moveToRoom(self, direction):
      next_room = self.game_state['current_room'].getConnectedRoom(direction, self)
      if next_room:
         self.game_state['current_room'] = next_room
      else:
         if 'alerts' in self.game_state:
            self.game_state['alerts'].append("You try the handle but the door is locked.")
         else:
            self.game_state['alerts'] = []
            self.game_state['alerts'].append("You try the handle but the door is locked.")

   # start fresh, set current room
   def initialize(self, start_Room = "bedroom"):
      # reset everything
      self.game_state = {}
      self.game_state['current_room'] = start_Room
      self.game_state['inventory'] = []
      self.game_state['alerts'] = []


   def describeRoom(self):
      return self.game_state['current_room'].getDescription()
   
   def getAlerts(self):
      alerts_to_return = self.game_state['alerts'][:]
      self.game_state['alerts'].clear()
      return alerts_to_return
