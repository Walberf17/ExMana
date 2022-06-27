from variables import *
import math

def set_scene(name , obj):
	SCENES[name] = obj

def calc_proportional_size(expected = None , max_area = None , max_rect = None):
	"""

	:param expected:
	:param max_area:
	:param max_rect:
	:return:
	"""
	if max_rect is None:
		for maps in maps_group:
			max_rect = maps.rect
	if max_area is None:
		for maps in maps_group:
			max_area = maps.get_virtual_size()
	max_sizes = pg.Vector2(max_rect.size)
	proportion = max_sizes.elementwise() / max_area
	if expected is None:
		expected = [1 , 1]
	if type(expected) in [float , int]:
		return (proportion[0]*expected)
	elif len(expected) == 2:
		return proportion.elementwise()*expected
	elif len(expected) == 4:
		pos = proportion.elementwise()*expected[:2] + max_rect.topleft
		size = proportion.elementwise()*expected[2:]
		return [pos , size]
	else:
		raise TypeError(f'value not good enought, {expected}')


def equip_item(item , place):
	for player in players_group:
		player.equip_item(item , place)


def unequip_item(place):
	for player in players_group:
		player.unequip_item(place)


def change_map_proportion(map_in_use , rect = screen_rect):
	global map_proportion
	new_size = map_in_use.get_virtual_size()
	rect_size = pg.Vector2(rect.size)
	map_proportion = rect_size.elementwise() / new_size

def add_cards_to_deck(cards_list: list):
	"""
	adds the list of card indexes to the main battle deck.
	:param cards_list: list of card indexes
	:return: None
	"""
	BATTLE_DECK.extend(cards_list)

def remove_cards_from_deck(cards_list):
	"""
	Removes the list of cards of the Battle Deck
	:param cards_list:
	:return:
	"""
	for card in cards_list:
		if card in BATTLE_DECK:
			BATTLE_DECK.remove(card)

def get_ang(card1 , card2):
	"""
	calcs the angle from 2 diferent cards
	:param card1: Card object
	:param card2: Card object
	:return: angle in radians
	"""
	x1 , y1 = card1.rect.center
	x2 , y2 = card2.rect.center
	return math.atan2((y2 - y1) , (x2 - x1))

