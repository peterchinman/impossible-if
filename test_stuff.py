from stuff import Stuff

# def test_name():
#    bed = Stuff("Bed", "This is your bed.")
#    assert bed.name == "Bed"

# def test_description():
#    bed = Stuff("bed", "This is your bed.", True)
#    assert bed.getStatefulDescription() == "This is your bed. The bed is made."

#    bed.bed_made = False
#    assert bed.getStatefulDescription() == "This is your bed. The bed is disgusting."

# def test_description_2():
#    bed = Stuff("bed", "This is your bed.", True, 3)
#    assert bed.getStatefulDescription() == "This is your bed. The bed is made. You have ample pillows."

# def test_description_3():
#    dresser = Stuff("dresser", "A beautiful chest of drawers.")
#    assert dresser.getStatefulDescription() == "A beautiful chest of drawers."

def test_description_4():
   dresser = Stuff("dresser", "A beautiful chest of drawers.", {'drawers_open' : {True : 'The drawers are open.', False : 'The drawers are close.'}}, {'drawers_open' : True})
   assert dresser.getStatefulDescription() == "A beautiful chest of drawers. The drawers are open."

def test_change_state():
   dresser = Stuff("dresser", "A beautiful chest of drawers.", {'drawers_open' : {True : 'The drawers are open.', False : 'The drawers are close.'}}, {'drawers_open' : True})
   assert dresser.getStatefulDescription() == "A beautiful chest of drawers. The drawers are open."
   dresser.states['drawers_open'] = False
   assert dresser.getStatefulDescription() == "A beautiful chest of drawers. The drawers are close."

def test_action():
   make_the_bed = Action("Make the Bed", "You dutifully make the bed.", {'bed_made': True})
   bed = Stuff("bed", "This is your bed.", {})





