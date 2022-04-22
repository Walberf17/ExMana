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

map_rect = pg.Rect(0,0,screen_rect.w , screen_rect.w*.8)
hand_map = pg.Rect(300,300,screen_rect.w , screen_rect.w*.2)
hand_map.bottom = screen_rect.bottom
new_rect = pg.Rect(0,0, screen_rect.w*.8 , screen_rect.h*.8)
new_rect.center = screen_rect.center
map_rect.center = screen_rect.center
maps = Maps(2 , rect = map_rect)
maps.add_effect(idx_effect = 'Fire' , pos = (250,250), duration = 1)
# maps.add_effect(idx_effect = 'Fire' , pos = (0,0) , area = (3,3) , duration = 2)

p1 = Character(images_idx = 2 , groups = [players_group] , rect_to_be = map_rect)
# p1.change_state('death')
# players_group.add(p1)
# pointer = Pointer(maps)
maps.rect.center = screen_rect.center
maps.rect_to_be.center = screen_rect.center






# create objects
test = Scene(screen_to_draw = screen , dicts_to_do = scene_test_dict)

# create scenes


# testes

test.run()

# initialize