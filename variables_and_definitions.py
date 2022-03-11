import pygame as pg

######## Initialize pygame
pg.init()
pg.font.init()

######## Create main screen
screen = pg.display.set_mode((800 , 800))
screen_rect = screen.get_rect()

######## Groups
text_boxes_group = pg.sprite.Group()
monsters_group = pg.sprite.Group()
players_group = pg.sprite.GroupSingle()
maps_group = set()
cards_group = pg.sprite.Group()
items_group = pg.sprite.Group()
buttons_group = pg.sprite.Group()
buttons_main_scene = pg.sprite.Group()
buttons_equip_scene = pg.sprite.Group()
selection_group = pg.sprite.Group()

######## Fonts for texts
font_size = int(screen_rect.h * .1)
main_menu_font = pg.font.SysFont("Arial" , font_size , False , True)

######## Sets of things
SCENES = {"Main Menu": None ,
           "Main Adventure": None ,
           "Main Battle": None ,
           "Items Menu": None ,
           "Habilities Menu": None ,
           "Testes": None}
buttons_dict = {
	"equip_scene": {
"head_btn" : [[0.1975 , 0.02375 , 0.1375 , 0.175], "unequip_item('head)"],
"neck_btn" : [[0.22125 , 0.21125 , 0.0875 , 0.0875], "unequip_item('neck')"],
"chest_btn1" : [[0.1625 , 0.30375 , 0.2125 , 0.2875], "unequip_item('chest')"],
"chest_btn2" : [[0.08625 , 0.32 , 0.05 , 0.225], "unequip_item('chest')"],
"chest_btn3" : [[0.4 , 0.315 , 0.05 , 0.2375], "unequip_item('chest')"],
"l_finger_btn" : [[0.45875 , 0.53125 , 0.0375 , 0.05], "unequip_item('l_finger')"],
"r_finger_btn" : [[0.03625 , 0.52625 , 0.0375 , 0.05], "unequip_item('r_finger')"],
"r_hand_btn" : [[-0.03625 , 0.59 , 0.175 , 0.2], "unequip_item('r_hand')"],
"legs_btn" : [[0.21 , 0.6 , 0.125 , 0.2875], "unequip_item('legs')"],
"l_hand_btn" : [[0.39875 , 0.58875 , 0.175 , 0.2], "unequip_item('l_hand')"],
"feet_btn" : [[0.1475 , 0.89125 , 0.25 , 0.075], "unequip_item('feet')"],
	}
}


# for images in general
IMAGES_PATH = './Images/'

# Images for Characters:
CHARACTER_IMAGES_DICT = {
	1: ["Characters/Character1.png" , [64,64]],
}

# for maps
MAP_EFFECTS = {
	"Fire": {"color": "red" , "effect": ["fire_effect()"]} ,
	"Ice": {"color": "red" , "effect": ["ice_effect()"]} ,
	"Oil": {"color": "dark gray" , "effect": ["oil_effect()"]} ,
	"Firaga": {"color": "green" , "effect": ["firaga_effect()"]} ,
	"Oxigen": {"color": "pink" , "effect": []} ,
	"Poison": {"color": "dark green" , "effect": ["poison_effect()"]} ,
	"Explosion": {"color": "black" , "effect": ["explosion_effect()"]} ,
	"Light": {"color": "yellow" , "effect": []} ,
	"Smell": {"color": "green" , "effect": []} ,

}
map_effect_sizes = [
	"[idx]" ,  # only the cell
	"grid.get_2_neighborhood(idx)" ,  # up and down neighbohood
	"grid.get_4_neighborhood(idx)" ,  # up , down , left and right
	"grid.get_8_neighbohood(idx)" ,  # plus diagonals
	"grid.get_24_neighborhood(idx)" ,  # a 5x5 square
]
effect_interations = [
	["Oil" , "Fire" , "Firaga"] ,
	["Fire" , "Ice" , None] ,
	["Poison" , "Oxigen" , None] ,
	["Oxigen" , "Fire" , "Explosion"] ,
	["Oxigen" , "Firaga" , "Explosion"] ,
]

######## dicts
scene_test_dict = {
	"draw": [text_boxes_group , monsters_group ,selection_group, players_group , cards_group ,maps_group, items_group , buttons_group] ,
	"click_down": [buttons_group , selection_group] ,
	"update": [buttons_group , players_group , selection_group],
	"move": [buttons_group , selection_group]
}

EQUIPAMENTS = {
	1: {"name" : "small sword of wood",
	    "description" : "Is it a toy?!",
	    "place" : "hand",
	    "modifiers":{ "attack" : 2,
	                  "velocity": 3,
	                  "mana" : 5
	    }
}}

######## Definitions

def create_scene(name , obj):
	SCENES[name] = obj


def calc_relative_size(size , rect = screen_rect):
	"""
	converts a size, position or rect_info to the size of the screen
	:param size: Union of int | [x,y] | [x,y,w,h]
	:param rect: The rect with the proportion
	:return: List
	"""
	# size = list(size)
	match size:
		case int(x)|float(x):
			return x * rect.w
		case [x , y]:
			a = x * rect.w
			b = y * rect.h
			return [a , b]
		case [x , y , w , h]:
			a = x * rect.w
			b = y * rect.h
			c = w * rect.w
			d = h * rect.h
			return [a , b , c , d]
		case _:
			raise TypeError

def equip_item(item , place):
	for player in players_group:
		player.equip_item(item , place)

def unequip_item(place):
	for player in players_group:
		player.unequip_item(place)