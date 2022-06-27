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

# for images in general
IMAGES_PATH = './Images/'

######## dicts and lists

scene_test_dict = {
	"draw": [maps_group , text_boxes_group , monsters_group , selection_group , players_group ,
	         cards_group , items_group , buttons_group , pointer_group , decks_group] ,
	"click_down": [buttons_group , selection_group , players_group , decks_group , moving_objects_group] ,
	"update": [buttons_group , maps_group , players_group , selection_group , moving_objects_group] ,
	"move": [buttons_group , players_group, selection_group , moving_objects_group]
}

