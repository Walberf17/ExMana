from variables import *


def set_scene(name , obj):
	SCENES[name] = obj


def calc_proportional_size(old_size):
	"""
	Converts the size of a given object relative to the actual map
	:param old_size: size in the same unit as the map
	:return: new sizes proportional to the image
	"""
	match old_size:
		case int(x) | float(x):
			return map_proportion.x * x
		case [x , y] | (x , y):
			a = map_proportion.x * x
			b = map_proportion.y * y
			return [a , b]
		case [x , y , w , h]:
			a = map_proportion.x * x
			b = map_proportion.y * y
			c = map_proportion.x * w
			d = map_proportion.y * h
			return [a , b , c , d]




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
