"""

Doing now:
	cards

Things to do:
	monsters
	do attacks
	deck

Things Done:
	character module (doesn't move or attacks)
	scene module
	buttons
	animations class with animations and action after animations
	moving object with click

"""

# import things
from variables import *
from definitions import *
from textbox import TextBox
from buttons import Button , SelectionBox , DropBox
from default_pygame_scene import Scene , EquipScene , EditScene
from deck_and_cards import Deck , Card
from characters import Character
from maps import Maps
from pointer import Pointer

map_rect = pg.Rect(0 , screen_rect.h * 0.1 , screen_rect.w , screen_rect.h * .6)
hand_map = pg.Rect(0 , 0 , screen_rect.w , screen_rect.h * .3)
hand_map.bottom = screen_rect.bottom
maps = Maps(2 , rect = map_rect)
maps.add_effect(idx_effect = 'Fire' , pos = (250 , 250) , duration = 1)
maps.add_effect(idx_effect = 'Fire' , pos = (0 , 0) , area = (3 , 3) , duration = 2)
p1 = Character(images_idx = 2 , groups = [players_group] , rect_to_be = map_rect)
# p1.change_state('death')
deck_test = Deck([1,1,1,2,2,2] , (0*screen_rect.w,.5*screen_rect.h,.1*screen_rect.w,.1*screen_rect.h) , hand_map , map_rect , p1)
# deck_test.card_deck_to_hand()
# deck_test.card_deck_to_hand()
# deck_test.card_deck_to_hand()

# players_group.add(p1)
# pointer = Pointer(maps)


# create objects
test = Scene(screen_to_draw = screen , dicts_to_do = scene_test_dict)

# create scenes


# testes

test.run()

# initialize
