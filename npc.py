"""
This file will work with the NPC in the game
they will inherit from character, but will take the speeches, give quests or items.
"""
from characters import Character
from variables import *
from definitions import *
from npcs_infos import *
import json


class NPC(Character):
	def __init__(self , NPC_idx = 1 , *args , **kwargs):
		self.npc_idx = NPC_idx
		super().__init__(*args , **kwargs)
		self.speeches = []

		info_dict = self.load_character()
		self.quests_to_give = info_dict.get("quests_to_give" , list())
		self.given_quests = info_dict.get("given_quests" , list())
		self.disposition = info_dict.get('disposition' , list())
		self.kinds = NPCS_KIND_DICT.get(self.npc_idx , list())


	# Administration of the character

	def save_character(self):
		new_dict = {
			'images_idx': self.images_idx ,
			'default_strength': self.default_strength ,
			'default_resilience': self.default_resilience ,
			'default_height': self.default_height,
			'default_width': self.default_width,
			'default_sight_meters': self.default_sight_meters ,
			'sex': self.sex ,
			'default_mana': self.default_mana ,
			'default_hp': self.default_hp ,
			'default_velocity': self.default_velocity ,
			'default_time': self.default_time ,
			'default_will': self.default_will ,
			'default_wisdom': self.default_wisdom ,
			'default_melee_dist': self.default_melee_dist ,
			'level': self.level ,
			'bag': self.bag ,
			'equipments': self.equipments ,
			'dominant_hand': self.dominant_hand ,
			'other_hand': self.other_hand ,
			'proportion_time_velocity': self.proportion_time_velocity ,
			'effects': self.effects ,
			'abnormal_effects': self.abnormal_effects ,
			'rect_center': self.rect.center ,
			'quests_to_give': self.quests_to_give,
			'given_quests': self.given_quests,
			'disposition': self.disposition,
		}

		with open(f'./DataInfo/NPCs/NPC{self.npc_idx}.json' , 'w') as file:
			json.dump(new_dict , file , indent = 4)

	def load_character(self):
		try:
			with open(f'./DataInfo/NPCs/NPC{self.npc_idx}.json' , 'r') as file:
				new_dict = json.load(file)
				return new_dict
		except FileNotFoundError:
			print('Nenhum arquivo. Vou fechar e vc se vira...')
			return {}

	# for creating NPC
	def click_up(self , event):
		if event.button == 3:
			self.save_character()
		super().click_up(event)

