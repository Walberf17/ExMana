import pygame as pg

######## Initialize pygame
pg.init()
pg.font.init()

######## Create main screen
screen = pg.display.set_mode((800 , 1000))
screen_rect = screen.get_rect()
FPS = 45
map_proportion = pg.Vector2(40 , 40)

######## Groups
text_boxes_group = pg.sprite.Group()
monsters_group = pg.sprite.Group()
players_group = pg.sprite.Group()
characters_group = pg.sprite.Group()
maps_group = pg.sprite.GroupSingle()
cards_group = pg.sprite.Group()
items_group = pg.sprite.Group()
buttons_group = pg.sprite.Group()
buttons_main_scene = pg.sprite.Group()
buttons_equip_scene = pg.sprite.Group()
selection_group = pg.sprite.Group()
effects_group = pg.sprite.Group()
moving_objects_group = set()
pointer_group = set()
decks_group = set()

######## Variables
FORCE_TO_CARDS = 2
CARD_SIZE = [screen_rect.w * 0.15 , screen_rect.h * .15]
BATTLE_DECK = [5, 5 , 5]

######## Fonts for texts
font_size = int(screen_rect.h * .1)
main_menu_font = pg.font.SysFont("Arial" , font_size , False , True)

######## Sets of things
SCENES = {"Main Menu": None ,
          "Main Adventure": None ,
          "Main Battle": None ,
          "Items Menu": None ,
          "Abilities Menu": None ,
          "Testes": None}

buttons_dict = {
	"equip_scene": {
		"head_btn": [[0.1975 , 0.02375 , 0.1375 , 0.175] , "unequip_item('head')"] ,
		"neck_btn": [[0.22125 , 0.21125 , 0.0875 , 0.0875] , "unequip_item('neck')"] ,
		"chest_btn1": [[0.1625 , 0.30375 , 0.2125 , 0.2875] , "unequip_item('chest')"] ,
		"chest_btn2": [[0.08625 , 0.32 , 0.05 , 0.225] , "unequip_item('chest')"] ,
		"chest_btn3": [[0.4 , 0.315 , 0.05 , 0.2375] , "unequip_item('chest')"] ,
		"l_finger_btn": [[0.45875 , 0.53125 , 0.0375 , 0.05] , "unequip_item('l_finger')"] ,
		"r_finger_btn": [[0.03625 , 0.52625 , 0.0375 , 0.05] , "unequip_item('r_finger')"] ,
		"r_hand_btn": [[-0.03625 , 0.59 , 0.175 , 0.2] , "unequip_item('r_hand')"] ,
		"legs_btn": [[0.21 , 0.6 , 0.125 , 0.2875] , "unequip_item('legs')"] ,
		"l_hand_btn": [[0.39875 , 0.58875 , 0.175 , 0.2] , "unequip_item('l_hand')"] ,
		"feet_btn": [[0.1475 , 0.89125 , 0.25 , 0.075] , "unequip_item('feet')"] ,
	}
}

######## Images in General
""""""
# for images in general
IMAGES_PATH = './Images/'

# Images for Characters:
CHARACTER_IMAGES_DICT = {
	'path': 'Characters/' ,
	1: {'adress': "Character1.png" , 'size': [64 , 64]} ,
	2: {'adress': "Character2.png" , 'size': [64 , 64] , 'states': ['idle' , 'death' , 'dash']} ,
}

# Images for Maps
MAPS_IMAGES_DICT = {
	'path': 'Maps/' ,
	1: {'adress': "1.png"} ,
	2: {'adress': "1.png"} ,
	3: {'adress': "1.png"} ,
}

# Images for Effects
EFFECT_DICT = {
	'path': 'Effects/' ,
	"Fire" : {'adress': "1.png" , 'size': [64 , 64]},
}


# Images for Items
ITEMS_IMAGES_DICT = {
	'path': 'Items/',
	'bread1': {'adress': "1.png"}
}

# Images for Cards
CARDS_IMAGES = {
	'path': 'Cards/',
	1 : {'adress': "1.png"},
	2 : {'adress': "2.png"},
	3 : {'adress' : '3.png'}
}

### Info of things

MAPS_INFO = {
	1: [[50 , 50] , 'Mapa de Teste'] ,
	2: [[5 , 5] , 'Mapa de Teste'] ,
	3: [[10 , 10] , 'Mapa de Teste'] ,

}

EFFECT_INFO = {
	'Fire': 'fire_damage(5)'
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
	"Taste" : {"color": "green" , "effect": []},
	"Sight" : {"color": "green" , "effect": []},
	"Search" : {"color": "green" , "effect": []},
	"Throughtful Search": {"color": "green" , "effect": []},


}

EFFECT_INTERACTIONS = [
	["Oil" , "Fire" , "Firaga"] ,
	["Fire" , "Ice" , None] ,
	["Poison" , "Oxigen" , None] ,
	["Oxigen" , "Fire" , "Explosion"] ,
	["Oxigen" , "Firaga" , "Explosion"] ,
]

######## dicts and lists

scene_test_dict = {
	"draw": [maps_group , text_boxes_group , monsters_group , selection_group , players_group ,
	         cards_group , items_group , buttons_group , pointer_group , decks_group] ,
	"click_down": [buttons_group , selection_group , players_group , decks_group , moving_objects_group] ,
	"update": [buttons_group , maps_group , players_group , selection_group , moving_objects_group] ,
	"move": [buttons_group , players_group, selection_group , moving_objects_group]
}

EQUIPAMENTS_DICT = {  # name:str , description:str , place:str , modifiers: dict of status to modify and number
	1: {"name": "small sword of wood" ,
	    "description": "Is it a toy?!" ,
	    "place": "hand" ,
	    "modifiers": {"attack": 2 ,
	                  "velocity": 3 ,
	                  "mana": 5
	                  }
	    } ,
}

POSSIBLE_CLUES = [
	"sight",
	"smell",
	"search",
	"taste",
	"touch",
	"listen",
]

ITEMS_INFO_DICT = {
	'bread1' : {'size':[.5,.5] , 'clues' : ['sight'] , 'card_idx':2},

}

effects_and_damages = [
	"fire_damage" ,  # usual args = (value)
	"ice_damage" , # usual args = (value)
	"poison_damage" , # usual args = (value)
	"ground_damage" , # usual args = (value)
	"wind_damage" , # usual args = (value)
	"electric_damage" , # usual args = (value)
	"dark_damage" , # usual args = (value)
	"light_damage" , # usual args = (value)
	"time_damage" , # usual args = (value)
	"oil_damage" , # usual args = (value)
	"gravity_damage" , # usual args = (value)
	"space_damage" , # usual args = (value)
	"pure_damage" , # usual args = (value)
	"stress_damage" , # usual args = (value)
	"physical_damage" , # usual args = (value)
	"feel_smell" , # usual args = (pos , area)
	"feel_taste" , # usual args = (pos , area)
	"feel_sight" , # usual args = (pos , area)
	"search" , # usual args = (pos , area)
	"throughtful_search" , # usual args = (pos , area)
	"move_card" , # usual args = (value)
	"get_item", # usual args = (self.rect , size)

]

deck_list_cards_battle = list(x + 1 for x in range(11))

# Cards

CARDS_DICT = {
	# 1:{
	# 'name': 'cool name for the card',
	# 'active_effects': [['Fire' , 'fire_damage(-2)' , 0 , [4,4]]], # index , action , duration , size
	# 'map_effect':[[index , 'fire_damage(-2)' , 0 , [4,4]]], # index , action , duration , size
	# 'cost': 15 | (2,15) # time cost | time cost , mana cost,
	# 'melee': False,
	# }
	# index: dict{name:str, active_effects:list , map_effect:list , cost: list of float , melee:boolean
	# effects: [[effect1 , duration1 , size1] , [effect2 , duration2 , size2]]
	# size: list if max_rect , int if circle
	1: {
		"name": 'Descanse em Paz' ,
		'active_effects': [['Get' , "get_item(size)" , 0 , .5]] ,
		'cost': 15 ,
		'melee': False ,
	} ,
	2: {
		'name': 'Cafungada Monstra' ,
		'active_effects': [['Smell' , 'feel_world(size , kind)' , 0, .2]] ,
		'cost': 5 ,
		'melee': True ,
	} ,
	3: {
		'name': 'Assadura Grave' ,
		'active_effects': [['Fire' , 'fire_damage(-10)' , 0 , [1 , 1]] , ['Fire' , 'fire_damage(-5)' , 5 , [1 , 1]]] ,
		'map_effect': [['Fire' , 'fire_damage(-5)' , 1 , [2 , 2]]] ,
		'cost': 15 ,
		'melee': False ,
	} ,
	4: {
		'name': '22º em Moc' ,
		'active_effects': [['Ice' , 'ice_damage(-10)' , 0 , [1 , 1]] , ['Ice' , 'ice_damage(-5)' , 4 , [2 , 2]]] ,
		'map_effect': [['Ice' , 'ice_damage(-5)' , 0 , [2 , 2]]] ,
		'cost': 15 ,
		'melee': False ,
	} ,
	5: {
		'name': 'Movimento - 2m/pixel' ,
		'active_effects': [['Move' , 'move_card(1)' , 0 , .1]] ,
		'cost': 5 ,
		'melee': True ,
	} ,
	6: {
		'name': 'Movimento - Cima' ,
		'active_effects': [['Move' , 'move_card(3)' , 0 , .2]] ,
		'cost': 5 ,
		'melee': True ,
	} ,
	7: {
		'name': 'Movimento - Baixo' ,
		'active_effects': [['Move' , 'move_card([0,1])' , 0 , .2]] ,
		'cost': 5 ,
		'melee': True ,
	} ,
	8: {
		'name': 'Movimento - Esquerda' ,
		'active_effects': [['Move' , 'move_card([0,-1])' , 0 , .2]] ,
		'cost': 5 ,
		'melee': True ,
	} ,
	9: {
		'name': 'Artigo de Luxo' ,
		'active_effects': [["Oil" , 'oil_damage(-10)' , 0 , [1 , 1]] , ['poison_damage(-5)' , 5 , [1 , 1]]] ,
		'map_effect': [['Oil' , 'oil_damage(-5)' , 0 , [2 , 2]]] ,
		'cost': 7 ,
		'melee': False ,
	} ,
	10: {
		'name': 'Água Oxigenada 40 Volumes' ,
		'active_effects': [["Poison" , 'poison_damage(-2)' , 0 , .5] , ] ,
		'map_effect': [['Poison' , 'poison_damage(-5)' , 0 , [2 , 2]]] ,
		'cost': 1 ,
		'melee': True ,
	} ,
	11: {
		'name': 'Demo com Espada' ,
		'active_effects': [["Poison" , 'poison_damage(-4)' , 0 , .5] , ["Poison" , 'stress_damage(-4)' , 0 , .5] ,
		                   ["Poison" , 'physical_damage(-2)' , 5 , .5]] ,
		'cost': 1 ,
		'melee': True ,
	} ,

}
# Quests
QUEST_KIND = [ # kind # exemple of goal
	'Place', # get to a place map001
	'NPC', # talk to a NPC  npc-h-2
	'Retrieve' , # Give something to a NPC [npc-h-2 , [[item_idx , quantity] , [item_idx , quantity]]]
	'Collect', # Collect something [[item_idx , quantity] , [2,4]]
	'Kill', # kill the monsters [[monter001 , 5] , [monter002 , 5]]
]


QUEST_DICT = {
	1:{
		'name': 'Tutorial',
		'Description': 'Find the door and exit',
		'Card_reward': 2,
		'Kind': 'Collect',
		'Goals': [[1,3]]*5,
		'Chain_quest': True
	},
	1.1: {
		'name': 'Tutorial2',
		'Description': 'Find the door and exit',
		'Card_reward': 2,
		'Kind': 'Collect',
		'Goals': [[2 , 3] , [1,5]],

	},
}
