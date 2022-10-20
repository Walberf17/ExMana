"""
This will work with the items in the game, that will be added in the map, and the players
"""
from animations_info import ITEMS_IMAGES_DICT
from items_info import *
from variables import *
from definitions import *
from animations import Animations
from moving_object import MovingObj
from pygame.sprite import Sprite

class ItemsInGame(MovingObj , Animations):
	def __init__(self , item_idx = None , pos = None  , groups = None):
		this_dict = ITEMS_INFO_DICT.get(item_idx)
		area = this_dict.get("size")
		clues = this_dict.get('clues')
		card_idx = this_dict.get('card_idx')
		Sprite.__init__(self , *groups)
		Animations.__init__(self ,area = area , pos = pos , images_name = item_idx , dict_with_images =ITEMS_IMAGES_DICT , groups = groups)
		MovingObj.__init__(self)
		self.discovered = False
		if clues is None:
			clues = []
		if type(clues) not in [list , tuple , set]:
			clues = [clues]
		self.card_idx = card_idx
		self.clues = clues
		self.can_be_taken = this_dict.get('take' , False)

	def check_can_be_taken(self):
		return (self.can_be_taken and self.discovered)

	def check_discover(self , clues):
		"""
		check if the given clue or clues is in the options to find this object.
		:param clues: strings or list of strings
		:return: True if at least one of the clues are in self.clues.
		"""

		if type(clues) not in [list , tuple , set]:
			clues = [clues]
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
		"""
		draw the item in the screen
		:param screen_to_draw:
		:return:
		"""
		if self.discovered:
			Animations.draw(self , screen_to_draw)

	def update(self):
		"""
		update handlers
		:return:
		"""
		Animations.update(self)

	def get_me(self , deck = None):
		"""
		add this card to the main battle deck
		:return:
		"""
		if deck is None:
			for player in players_group:
				deck = player.get_deck()
		deck.new_card(self.card_idx)
		self.kill()

	def interact(self , player):
		return False
