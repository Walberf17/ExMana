"""

Doing now:
	map and effects
	do map effect in card
	effect check_effect_on_obj

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
from deck_and_cards import Deck , Card
from characters import Character
from maps import Maps

map_rect = pg.Rect(0,0,screen_rect.w , screen_rect.y*.8)
hand_map = pg.Rect(0,0,screen_rect.w , screen_rect.y*.2)
hand_map.bottom = screen_rect.bottom
maps = Maps(2, screen_rect)
maps.add_effect(idx_effect = 'Fire' , pos = (250,250), duration = 1)
maps.add_effect(idx_effect = 'Fire' , pos = (300,300) , area = (2,2) , duration = 2)

p1 = Character(1)
players_group.add(p1)





# create objects
test = Scene(dicts_to_do = scene_test_dict)

# create scenes


# testes

test.run()

# initialize