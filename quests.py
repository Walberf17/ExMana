from definitions import *
from quests_info import QUEST_DICT
from variables import *

class Quest:
	"""
	This is a class that will save and calc the completition of the quests,
	"""
	def __init__(self, quest_index = 1 , groups = None , player = None):
		"""
		this will init the quest, taking the Quest index for retrieving the info.
		it also takes the player and groups that it will be part of.
		:param idx:
		:param groups:
		:param player:
		"""
		if groups is None:
			groups = []
		for group in groups:
			group.add(self)
		self.groups = groups
		self.player = player
		self.quest_index = quest_index
		this_dict = QUEST_DICT.get(quest_index)
		self.name = this_dict.get('Name')
		self.description = this_dict.get('Description')
		self.card_reward = this_dict.get('Card_reward')
		self.kind = this_dict.get('Kind')
		self.goals = this_dict.get('Goals')
		self.chain_quest = this_dict.get('Chain_quest' , False)
		self.completion = {}
		self.is_complete = False
		self.stage = 0
		if self.kind in ['Retrieve']:
			goals = self.goals[1:]
		elif self.kind in ['Collect' , 'Kill']:
			goals = self.goals
		else:
			goals = []
		for idx_name , _ in goals:
			self.completion[idx_name] = 0

	def check_completition(self):
		"""
		return if it is is_complete or not
		:return: Boolean
		"""
		return self.is_complete

	def check_place(self):
		"""
		check if the current map is the place it has to be.
		:return: boolean
		"""
		for maps in maps_group:
			this_map = maps
		return this_map.get_map_idx == self.goals

	def check_npc(self , npc):
		"""
		check if the current talking NPC is the one it needs.
		:param npc: :param npc: NPC class
		:return: boolean
		"""
		return npc.get_npc_idx == self.goals

	def check_retrieve(self , npc):
		"""
		check if when talking to the NPC it has all the items in the bag
		:param npc: NPC class
		:return: boolean
		"""
		player = self.player
		npc_idx , item_lists = self.goals
		ready = []
		if npc.get_npc_idx() == npc_idx:
			deck = player.get_deck()
			for item , quantity in item_lists:
				if item in deck and quantity < deck.count(item):
					ready.append(True)
				else:
					ready.append(False)
					break
			return all(ready)
		return False

	def update_counter(self , thing , qnt = 1):
		"""
		increment the counter of the given monster to check how much of the quest is is_complete.
		:param thing: monster to count
		:param qnt: int
		:return: boolean
		"""
		if thing in self.completion:
			self.completion[thing] += qnt

	def check_collect_kill(self):
		"""
		check if the goal of collector or kill is is_complete
		:return: boolean
		"""
		ready = []
		deck = self.player.get_deck()
		for item , quantity in self.goals:
			if item in deck and quantity < deck.count(item):
				ready.append(True)
			else:
				ready.append(False)
				break
		return all(ready)

	def complete(self):
		"""
		set itself as completed
		:return: None
		"""
		self.is_complete = True
		if self.chain_quest:
			int_part = self.quest_index//1
			next_idx = round(self.quest_index%1,4)
			while next_idx%1 != 0:
				next_idx *= 10
			new_idx = int_part+(round((next_idx+1)/(10**len(str(next_idx+1))) , 4))
			print(new_idx)
			Quest(new_idx , self.groups, self.player)




