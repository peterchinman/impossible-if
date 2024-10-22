class Stuff:
   def __init__(self, name, description, state_descriptions, initial_states) -> None:
      self.name = name
      self.description = description
      self.state_descriptions = state_descriptions
      self.states = initial_states

   

   def getStatefulDescription(self):
      stateful_description = self.description

      for state_name, state_value in self.states.items():
         stateful_description += " " + self.state_descriptions[state_name][state_value]
      
      return stateful_description
   
class Action:
   

