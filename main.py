# import things
from textbox import TextBox
from buttons import Button
from default_pygame_scene import Scene
from maps_class import MapGrid
from variables_and_definitions import *
from characters import Character

# create objects
p1 = Character(1)
players_group.add(p1)
print(p1.get_status() , 'antes')
p1.equip_item(1)

print(p1.get_status() , "depois")

print(p1.get_equipaments())

test = Scene(screen , dicts_to_do = scene_test_dict)
# text_test = TextBox("esse é um exemplo pra ver como ficará um texto na tela." , screen_rect , main_menu_font)
# test_map = MapGrid('teste' , (5,5) , screen_rect , 'red')
# btn_test = Button([.25,.1,.5,.1],"print('ok')" , txt = "Print")


# create scenes


# testes

test.run()

# initialize