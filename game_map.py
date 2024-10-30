from game_machinery import Action, RoomObject, Room

# load up all the classes
lay_in_bed = Action(
   "Lay in Bed",
   "You sprawl across the bed, luxuriously, rolling around like a little prince and cooing softly to yourself.",
   {},
   {'Your Bed': {
      'bed_made' : False
   }}
)
make_bed = Action(
   "Make Bed",
   "You make the bed with an air of moral superiority.",
   {'Your Bed' : {
   'bed_made': False}},
   {'Your Bed' : {
      'bed_made' : True}}
)
bed = RoomObject(
   "Your Bed",
   "A queensize bed with a floral duvet. You've had the mattress for years and it is starting to sag a little in the middle.",
   {'bed_made': {
      True: "The bed is neatly made, serving as a beacon of moral rectictude in this slovenly world.",
      False: "The bed is disheveled, which seems to reflect the state of your soul."
   }},
   {'bed_made': True},
   [lay_in_bed, make_bed]
)

close_doors = Action(
   "Close Doors",
   "The doors, freed of paint, slide closed smoothly",
   {'Sliding Doorss': {'painted_over': False}},
   {'Sliding Doors': {'open' : False} }
)
cut_away_paint = Action(
   "Cut Away the Paint",
   "You take the sharp edge of the knife to the thick layers of paint encasing the sliding doors. With a few deft cuts you are able to peel away the paint like the skin from a sunburn, freeing the doors.",
   {'inventory' : {'knife': True}},
   {'Sliding Doors' : {'painted_over' : False}}
)
sliding_doors = RoomObject(
   "Sliding Doors",
   "A set of sliding doors.",
   {'open': {
      True: "The doors are open. Thru them you can see the living room.",
      False: "The doors are closed."
   },
   'painted_over': {
      True: "The doors seem to have once slid open and closed on a metal track, but your landlord has slathered so many layers of white paint over them that they are now, permanently, open.",
      False : "The doors have been freed from their landlord-imposed paint-bondage."
   }},
   {'open': True,
   'painted_over': True},
   [close_doors, cut_away_paint]
)

bedside_table = RoomObject("Bedside Table")
tarot_cards = RoomObject("Tarot Cards")
lamp = RoomObject("Lamp")
mouthguard = RoomObject("Mouthguard")
add_to_inventory = Action(
   "Take Knife",
   "You pick up the knife with a sense of giddiness.",
   {},
   {'inventory': {'knife': True}}
)
knife = RoomObject(
   "A Knife",
   "It's sharp edge is practically singing to you.",
   {},
   {},
   [add_to_inventory]
)

bedroom = Room(
   "Bedroom",
   "<p>You are standing at the foot of {objects['your-bed'].getLink('your bed')}.</p><p>Beside the bed is a {objects['bedside_table'].getLink('bedside table')}. On the table there is {objects['tarot_cards'].getLink('a deck of tarot cards')}, {objects['lamp'].getLink('a lamp')}, {objects['mouthguard'].getLink('a mouthgard')}, and {objects['knife'].getLink('a knife')}.</p><p>To your left are a set of {objects['sliding-doors'].getLink('sliding doors')}. {objects['sliding-doors'].getStateDescription('open')}</p>",
   {'your-bed': bed, 'bedside_table': bedside_table, 'tarot_cards': tarot_cards, 'lamp': lamp, 'mouthguard': mouthguard, 'sliding-doors': sliding_doors, 'knife': knife}
)
