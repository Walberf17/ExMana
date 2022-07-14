"""
This file will work with the NPC in the game
they will inherit from character, but will take the speeches, give quests or items.
"""
from characters import Character
from variables import *
from definitions import *
from npcs_infos import *
from quests_info import QUEST_DICT
import json
import random


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
		self.create_speeches()


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
		"""
		get a dictionary saved in the correct folder of this character.
		:return:
		"""
		try:
			with open(f'./DataInfo/NPCs/NPC{self.npc_idx}.json' , 'r') as file:
				new_dict = json.load(file)
				return new_dict
		except FileNotFoundError:
			print('Nenhum arquivo. Vou fechar e vc se vira...')
			return {}

	# for creating NPC
	def click_up(self , event):
		"""
		Saves the character when clicked with the right mouse button.
		:param event:
		:return:
		"""
		if event.button == 3:
			self.save_character()
		super().click_up(event)

	def interact_with(self , player):
		"""
		check if it can give a quest to the player, if so, it gives the quest,
		else, it talks to it.
		:param player: Player object
		:return: None
		"""
		if self.quests_to_give and player.can_get_quest(self.quests_to_give[0]):
			self.give_quest_to_player(player)
		else:
			self.talk()


	def give_quest_to_player(self , player):
		"""
		Give a quest to the player, then set it as given, and remove it from its list
		:param player: Player object
		:return: None
		"""
		quest_index = self.quests_to_give.pop(0)
		self.given_quests.append(quest_index)
		player.give_quest(quest_index)
		self.talk(quest_index)
		self.save_character()

	def talk(self , quest_index = None):
		"""
		if quest_index is given, it prints the text of the quest,
		else, it prints a random sentence
		:param quest_index: index from the QUEST_DICT
		:return: None
		"""
		if quest_index is None:
			print(random.choice(self.speeches))
		else:
			this_quest_dict = QUEST_DICT.get(quest_index)
			print(this_quest_dict.get('Talk_text' , 'Eita, faltou texto...'))

	def create_speeches(self):
		"""
		get the list of types this character belongs, then takes all the
		possible speeches.
		:return: None
		"""
		for kind in self.kinds:
			self.speeches.extend(kind)

