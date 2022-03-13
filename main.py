"""

Doing now:
	map

Things to do:
	Maps
	monsters
	do attacks
	cards
	deck

Things Done:
	character module (doesn't move or attacks)
	scene module
	buttons

"""



# import things
from variables_and_definitions import *
from textbox import TextBox
from buttons import Button , SelectionBox , DropBox
from default_pygame_scene import Scene , EquipScene , EditScene
from maps_class import MapGrid
from characters import Character
from maps import Maps


maps = Maps(1 , screen_rect)
p1 = Character(4)
players_group.add(p1)


# create objects
test = Scene(dicts_to_do = scene_test_dict)

# create scenes


# testes

test.run()

# initialize