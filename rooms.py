class Room:
    """
    A class for Rooms, a.k.a Places, which have names, descriptions, list of connected Rooms, 
    """
    def __init__(self, name, description, connected_rooms):
        self.name = name
        self.slug = slugify(name)
        self.description = description
        self.connected_rooms = connected_rooms
        
