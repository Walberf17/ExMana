"""
This file will work with the NPCs in the game
they will inherit from character, but will take the speeches, give quests or items.
"""
from characters import Character
from variables import *
from definitions import *
from npc_infos import *


class NPCs(Character):
	def __init__(self , NPC_kind = 1 , images_idx = None , rect_to_be = screen_rect , groups = None):
		super().__init__(self , images_idx = images_idx , rect_to_be = rect_to_be , groups = groups)
		self.NPC_kind = NPC_kind
		self.speeches = []
		for kind in NPCS_KIND_DICT.get(self.NPC_kind , []):
			self.speeches.extend(kind)

