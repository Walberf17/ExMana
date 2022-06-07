"""
This will work with the items in the game, that will be added in the map, and the players
"""

from variables import *
from definitions import *
from animations import Animations
from moving_object import MovingObj
from pygame.sprite import Sprite

class MapObject(MovingObj , Sprite , Animations):
	def __init__(self , item_idx = None , pos = None  , groups = None):
		if groups is None:
			groups = []
		if type(groups) not in [list , set , tuple]:
			groups = list(groups)
		this_dict = ITEMS_INFO_DICT.get(item_idx)
		area = this_dict.get("size")
		clues = this_dict.get('clues')
		active_effects = this_dict.get('active_effects')
		Sprite.__init__(self , *groups)
		Animations.__init__(self ,area = area , pos = pos , images_idx = item_idx , dict_with_images =ITEMS_IMAGES_DICT )
		MovingObj.__init__(self)
		self.discovered = True
		if clues is None:
			clues = []
		if type(clues) not in [list , tuple , set]:
			clues = list(clues)
		self.active_effects = active_effects
		self.clues = clues

	def check_discover(self , clues):
		"""
		check if the given clue or clues is in the options to find this object.
		:param clues: strings or list of strings
		:return: True if at least one of the clues are in self.clues.
		"""
		if type(clues) not in [list , tuple , set]:
			clues = list(clues)

		for clue in clues:
			if clue in self.clues:
				return True
		return False

	def find_me(self):
		"""
		set itself as discovered
		:return:
		"""
		self.discovered = True

	def hide_me(self):
		'''
		set itself as hidden
		:return:
		'''
		self.discovered = False

	def draw(self , screen_to_draw):
		if self.discovered:
			Animations.draw(self , screen_to_draw)

	def update(self):
		Animations.update(self)

	def use_me(self , player):
		for kind , effect , duration , size in self.active_effects:
			center = pg.Vector2(self.rect.center)
			for character in characters_group:
				match size:
					case int(x) | float(x):
						size = calc_proportional_size(size)
						if center.distance_to(character.rect.center) <= x:
							character.add_effects(kind , effect , duration)
					case [x , y]:
						effect_rect = pg.Rect((0 , 0) , calc_proportional_size([x , y]))
						effect_rect.center = center
						if character.rect.colliderect(effect_rect):
							character.add_effects(kind , effect , duration)

