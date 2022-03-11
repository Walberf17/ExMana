# import things
from variables_and_definitions import *
from textbox import TextBox
from buttons import Button , SelectionBox , DropBox
from default_pygame_scene import Scene , EquipScene , EditScene
from maps_class import MapGrid
from characters import Character


# create objects
p1 = Character(1)
players_group.add(p1)
print(p1.get_status() , 'antes')
p1.equip_item(1)

print(p1.get_status() , "depois")

print(p1.get_equipaments())
main = Scene(screen , scene_test_dict)
print(main)
test = EditScene(screen , dicts_to_do = scene_test_dict)
create_scene("Main Menu" , main)
create_scene("Testes" , test)

# text_test = TextBox("esse é um exemplo pra ver como ficará um texto na tela." , screen_rect , main_menu_font)
# test_map = MapGrid('teste' , (5,5) , screen_rect , 'red')
# btn_test = Button([.25,.1,.5,.1],"print('ok')" , txt = "Print")


# drop_b = DropBox([0.22125 , 0.21125 , 0.0875 , 0.0875] , drop_action = 'SCENES.get("Main Menu").run')
# selection_box = SelectionBox([0.1975 , 0.02375 , 0.1375 , 0.175],arguments = "" , drops = [drop_b])

# create scenes


# testes

test.run()

# initialize