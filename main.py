"""

Doing now:
	map and effects

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


maps = Maps(2, screen_rect)
maps.add_effect(1 , [0,0] , [1,1] , 1)

p1 = Character(1)
players_group.add(p1)



# create objects
test = Scene(dicts_to_do = scene_test_dict)

# create scenes


# testes

test.run()

# initialize