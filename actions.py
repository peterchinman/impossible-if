class Action:
    """
    A class for Actions, which have names, descriptions, causes, and requirements.
    
    Args:
        name (str): The 'name' of the action.
        description (str): A 'description of the action'.
        causes (list): A list of dictionaries specifying the effects of the action.
        requires (list): A list of dictionaries specifying the prerequisites for the action.
    
    Each dictionary element in `causes` and `requires` should have the following format:
    [{  'object': 'object_name',
        'state': 'state_name',
        'value': 'value_name'
    }]
    """
    def __init__(self, name, description, causes, requires):
        self.name = name
        self.slug = slugify(name)
        self.description = description
        
        # Ensure causes and requires are lists of dictionaries
        if isinstance(causes, list) and all(isinstance(c, dict) for c in causes):
            self.causes = causes
        else:
            raise ValueError("causes must be a list of dictionaries")
        
        if isinstance(requires, list) and all(isinstance(r, dict) for r in requires):
            self.requires = requires
        else:
            raise ValueError("requires must be a list of dictionaries")

    def checkRequirements(self, GAME_STATE):
        """
        Checks if the action's requirements are met based on the current game state.

        Args:
            GAME_STATE (dict): The current state of all objects in the game.
                                  Expected format: {'object_name': {'state_name': value}}

        Returns:
            bool: True if all requirements are met, False otherwise.
        """
        for r in self.requires:
            object_name = r['object']
            state_name = r['state']
            required_value = r['value']

            # Check if the object exists in the current game state
            if object_name in GAME_STATE:
                # Check if the specific state of the object matches the required value
                if GAME_STATE[object_name].get(state_name) != required_value:
                    return False  # Requirement not met
            else:
                return False  # Object not found in the current state

        return True  # All requirements met


    def runCauses(self, GAME_STATE):
        """
        Executes the causes for this action by updating the game state.

        Args:
            GAME_STATE (dict): The current state of all objects in the game.
                                  Expected format: {'object_name': {'state_name': value}}

        Returns:
            dict: The updated game state after applying the causes.
        """
        for c in self.causes:
            object_name = c['object']
            state_name = c['state']
            new_value = c['value']

            # Ensure the object exists in the current state
            if object_name in GAME_STATE:
                # Update the specific state of the object
                GAME_STATE[object_name][state_name] = new_value
            else:
                # If the object doesn't exist, initialize it with the new state
                GAME_STATE[object_name] = {state_name: new_value}

        return GAME_STATE  # Return the updated game state
