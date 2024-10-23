class Player:
   def __init__(self, start_Room = None, start_inventory = None) -> None:
      self.current_room = start_Room
      self.game_state = {}
      self.game_state['inventory'] = start_inventory if start_inventory else {}
      self.alerts = []

   def moveToRoom(self, direction):
      next_room = self.current_room.getConnectedRoom(direction, self)
      if next_room:
         self.current_room = next_room
      else:
         self.alerts.append("You try the handle but the door is locked.")

   def describeRoom(self):
      return self.current_room.getDescription()
   
   def getAlerts(self):
      alerts_to_return = self.alerts[:]
      self.alerts.clear()
      return alerts_to_return
