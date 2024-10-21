from slugify import slugify

class Stuff:
    """
    Class for Things with Descriptions and Actions.
    
    Args:
        name (str): The "name" of the object.
        description (str): A "description of the object".
        state_descriptions (dict): A dictionary of possible states.
                                Key: state name
                                Value: dictionary of {value : desciption}.
                                e.g.    {'bed_made' : {
                                            True : "The bed is neatly made.",
                                            False : "The bed is disheveled.",
                                        },}
        initial_states (dict): Dictionary of inital state values. Keys are state names, Values are state values
                              e.g.  {'bed_made' : True, 'sheets' : 'polar_bear_sheets'}
        actions (list): A list of Action objects associated with the Stuff object.
    """
    def __init__(self, name, description, state_descriptions, initial_states):
        self.name = name
        self.slug = slugify(name)
        self.description = description

        if isinstance(state_descriptions, dict):
            self.state_descriptions = state_descriptions  # Dictionary of possible states
        else:
            raise ValueError("possible_state must be a dict")
        
        self.initial_states = initial_states

        # Ensure actions is a list of Action objects
      #   if isinstance(actions, list) and all(isinstance(action, Action) for action in actions):
      #       self.actions = actions
      #   else:
      #       raise ValueError("actions must be a list of Action objects")
        
        # Update GAME_STATE object with default initial states
      #   for state_name, state_value in self.initial_states.items():
      #       # TODO should this use self.name or should there be some self.id?
      #       GAME_STATE['Stuff'].setdefault(self.name, {}) 
      #       GAME_STATE['Stuff'][self.name][state_name] = state_value

    
    def validate(self): 
        # does Stuff minimally *need* to have?

        # make sure state_descriptions are organized correctly

        # make sure initial_states are organizied correctly
        pass

    def get_description(self, GAME_STATE):
        """
        Returns the description of the Stuff, including any additional details
        from the possible states based on the current state.

        Args:
            GAME_STATE (dict): The current state of the game for this Stuff.

        Returns:
            str: The complete description of the Stuff, including state-based additions.
        """
        full_description = self.description
        # TODO probably shouldn't store state by name, but by some sort of ID?
        stuff_state = GAME_STATE['Stuff'].get(self.name, {})

        # Check the state_descriptions and add to the description if they match the current state
        for state, value_dict in self.state_descriptions.items():
            for value, description in value_dict.items():
                if stuff_state.get(state) == value:
                    # TODO this should... probably be a new line, not a space?
                    full_description += " " + description

        return full_description
    
    def get_actions(self, GAME_STATE):
        """
        Returns a list of actions that are available for the Stuff object,
        after checking if their requirements are met.
        
        Args:
            GAME_STATE (dict): The current state of the game.

        Returns:
            list: A list of dictionaries containing action names and slugs for actions
                  whose requirements are met.
        """
        available_actions = []
        for action in self.actions:
            if action.checkRequirements(GAME_STATE):
                # TODO probably this should return everything we'd want to know about the action?
                available_actions.append({'name': action.name, 'slug': action.slug})
        
        return available_actions
    
    def inspect(self):
        """
        Combines the name, description, and available actions into a structure for rendering.
        
        Returns:
            dict: A dictionary containing the name, description, and actions.
        """
        return {
            'name': self.name,
            'description': self.get_description(GAME_STATE),
            'actions': self.get_actions(GAME_STATE)
        }
    
