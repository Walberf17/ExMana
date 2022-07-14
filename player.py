from quests_info import QUEST_DICT
from definitions import *
import pygame as pg
from characters import Character
from quests import Quest
import json


class Player(Character):

	def __init__(self , *args , **kwargs):
		super().__init__(*args , **kwargs)
		loaded_dict = self.load_character()
		self.quests = set()
		self.to_kill_quest = set()
		self.to_place_quest = set()
		self.to_retrieve_quest = set()
		self.to_collect_quest = set()
		self.to_NPC_quest = set()
		self.quests_indexes = []
		self.completed_quests_indexes = loaded_dict.get('completed_quests_indexes' , list())
		for idx in loaded_dict.get('quests_indexes' , list()):
			self.give_quest(idx)
		self.marks = loaded_dict.get('marks' , list())

	def set_deck(self , deck = None , adventure = None):
		"""
		Set a deck to the player.
		:param deck: Deck object
		:param adventure: boolean
		:return: None
		"""
		if adventure:
			self.adventure_deck = deck
		else:
			self.main_deck = deck

	def get_deck(self):
		"""
		return the current deck the player is using.
		:return: Deck object
		"""
		return self.main_deck

	def create_rect_to_draw_in_status(self , size):
		"""
		creates a max_rect to draw the correct sprite
		:return: None
		"""
		i , j = self.image_index
		n_w , n_h = size
		max_i , max_j = self.sprite_grid
		w = n_w / max_i
		h = n_h / max_j
		init_x = self.rect.left + (w * i)
		init_y = self.rect.top + (h * j)
		return pg.Rect(init_x , init_y , w , h)

	def can_get_quest(self , idx):
		"""
		check if the player can get the quest
		:param idx: Index of the quest in the QUEST_DICT.
		:return: Boolean, True if it can get the quest.
		"""
		this_quest_dict = QUEST_DICT.get(idx)
		requirements = set(this_quest_dict.get('Requirements' , set()))

		if requirements:
			print('tem requerimentos')
			return requirements.issubset(self.get_marks())
		return True

	def give_quest(self , idx):
		"""
		Set a new quest for itself.
		:param idx:
		:return:
		"""
		if idx in self.quests_indexes:
			return
		kind = QUEST_DICT.get(idx).get('Kind')
		groups = []
		groups.append(self.quests)
		kind_dict = {
			'Place': self.to_place_quest ,
			'NPC': self.to_NPC_quest ,
			'Retrieve': self.to_retrieve_quest ,
			'Collect': self.to_collect_quest ,
			'Kill': self.to_kill_quest ,
		}

		self.quests_indexes.append(idx)

		groups.append(kind_dict.get(kind , []))
		Quest(quest_index = idx , groups = groups , player = self)

	def draw(self , screen_to_draw):

		# draw the image
		super().draw(screen_to_draw)

		# draw the time hud
		pg.draw.rect(screen_to_draw , "red" , self.time_hud)

	def update(self , *args , **kwargs):
		super().update(*args , **kwargs)

		# updates the hud of duration
		if self.time > 0:
			self.time += - 1 / FPS
			dtime = self.time / self.default_time
			self.time_hud.h = screen_rect.h * dtime
			self.time_hud.bottomright = screen_rect.bottomright


	# draw things and
	def draw_range(self , screen_to_draw , meele = True):
		"""
		Draw a circle for the given range of the attack
		:param screen_to_draw: pg.Surface
		:param meele: Bool
		:return: None
		"""
		melee_dist = self.melee_pixels
		transparency = 90
		if meele:  # draws a smaller circle, with the range of the meelee attack
			new_surf = pg.Surface([melee_dist * 2] * 2).convert_alpha()
			new_surf.fill([0 , 0 , 0 , 0])
			new_surf_rect = new_surf.get_rect()
			pg.draw.circle(new_surf , [0 , 0 , 255 , transparency] , (new_surf_rect.w / 2 , new_surf_rect.h / 2) , melee_dist)

		else:  # draws a larger circle, based on the sight_pixels of the character
			sight_dist = self.sight_pixels
			new_surf = pg.Surface([sight_dist * 2] * 2).convert_alpha()
			new_surf.fill([0 , 0 , 0 , 0])
			new_surf_rect = new_surf.get_rect()
			pg.draw.circle(new_surf , [0 , 0 , 255 , transparency] , (new_surf_rect.w / 2 , new_surf_rect.h / 2) , sight_dist)
			pg.draw.circle(new_surf , [0 , 0 , 0 , 0] , (new_surf_rect.w / 2 , new_surf_rect.h / 2) , melee_dist)

		new_surf_rect.center = self.rect.center
		# pg.draw.max_rect(screen_to_draw , "black" , new_surf_rect)
		screen_to_draw.blit(new_surf , new_surf_rect)

	def draw_cost(self , card , screen_to_draw):
		cost_hud = self.time_hud
		dtime = card.cost / self.default_time
		cost_hud.h = screen_rect.h * dtime
		color = 'blue2'
		if self.check_cost(cost = card.cost):
			color = 'yellow'
		pg.draw.rect(screen_to_draw , color , cost_hud)

	def draw_equip_screen(self , screen_to_draw , screen_to_draw_rect):
		size = pg.Vector2(screen_to_draw_rect.size).elementwise() * (2 , .5)
		image = pg.transform.scale(self.images , size)
		new_rect = image.get_rect()
		new_clamp_rect = self.create_rect_to_draw_in_status(size)
		new_rect.size = new_clamp_rect.size
		new_rect.midleft = screen_to_draw_rect.center
		pg.draw.rect(screen_to_draw , "red" , new_rect , 4)
		screen_to_draw.blit(image , new_rect , new_clamp_rect)


	# check and use cards
	def check_in_range(self , melee):
		center = pg.Vector2(self.rect.center)
		dist = center.distance_to(pg.mouse.get_pos())
		if melee:
			return dist <= self.melee_pixels
		else:
			return self.sight_pixels >= dist >= self.melee_pixels

	def check_cost(self , cost):
		if type(cost) == int:
			return self.time >= cost
		else:
			time_cost , mana_cost = cost
			return all([self.time >= time_cost , self.mana >= mana_cost])

	def consume_cost(self , cost):
		"""
		Consume the costs of the item or action
		:param cost: Union Int, list
		:return: Nothing
		"""
		if type(cost) == int:
			self.time -= cost
		else:
			time_cost , mana_cost = cost
			self.time -= time_cost
			self.mana -= mana_cost

	def get_multiplier(self , card):
		"""
		Return a multiplier to the calc of the size fo the effects.
		:param card:
		:return:
		"""
		if type(card) not in [list , tuple]:
			card = [card , 0]
		multiplier = 1
		if card[0] in self.abnormal_effects:
			multiplier += self.abnormal_effects.get(card[0] , 0)
		multiplier += self.will//25
		return multiplier

	def get_item(self , size):
		"""
		get the card and add it to the deck
		:param size: area in meters to search
		:return:
		"""
		center = pg.Vector2(pg.mouse.get_pos())
		for obj in items_group:
			if type(size) in (int , float):
					if center.distance_to(obj.rect.center) <= int(size):
						obj.get_me(self.main_deck)
			elif type(size) in [list , tuple] and len(size) == 2:
					effect_rect = pg.Rect((0 , 0) , size)
					effect_rect.center = center
					if obj.rect.colliderect(effect_rect):
						obj.get_me(self.main_deck)

	def check_hit_object(self , obj , pos , size):
		"""
		check if the obj is hit by the size of this effect
		:param obj: a object that has a rect parameter
		:param size: a list of sizes in pixels
		:param pos: the center of the effect
		:return: boolean, True if hit by the effect
		"""
		center = pg.Vector2(pos)
		if type(size) in (int , float):
			if center.distance_to(obj.rect.center) <= size:
				return True
		elif type(size) in [list , tuple] and len(size) == 2:
			effect_rect = pg.Rect((0 , 0) , size)
			effect_rect.center = center
			if obj.rect.colliderect(effect_rect):
				return True
		return False

	# Manage the character
	def save_character(self):
		new_dict = {
			'images_idx':               self.images_idx ,
			'default_strength':         self.default_strength ,
			'default_resilience':       self.default_resilience ,
			'default_height':           self.default_height,
			'default_width':            self.default_width,
			'default_sight_meters':     self.default_sight_meters ,
			'sex':                      self.sex ,
			'default_mana':             self.default_mana ,
			'default_hp':               self.default_hp ,
			'default_velocity':         self.default_velocity ,
			'default_time':             self.default_time ,
			'default_will':             self.default_will ,
			'default_wisdom':           self.default_wisdom ,
			'default_melee_dist':       self.default_melee_dist ,
			'level':                    self.level ,
			'bag':                      self.bag ,
			'equipments':               self.equipments ,
			'dominant_hand':            self.dominant_hand ,
			'other_hand':               self.other_hand ,
			'proportion_time_velocity': self.proportion_time_velocity,
			'effects':                  self.effects,
			'abnormal_effects':         self.abnormal_effects,
			'quests_indexes' :          self.quests_indexes,
			'completed_quests_indexes': self.completed_quests_indexes,
			'marks' :                   self.marks,
			'rect_center':              self.rect.center ,
}
		with open(f'./DataInfo/Players/player1.json' , 'w') as file:
			json.dump(new_dict , file)

	def load_character(self):
		"""
		get a dictionary saved in the correct folder of this character.
		:return:
		"""
		try:
			with open(f'./DataInfo/Players/player1.json' , 'r') as file:
				new_dict = json.load(file)
				return new_dict
		except FileNotFoundError:
			print('Nenhum arquivo. Vou fechar e vc se vira...')
			return {}

	def get_marks(self):
		"""
		Return a set with the marks the player has
		:return: set()
		"""
		return set(self.marks)

	# interactions
	def interact(self , pos , size):
		"""
		check if it can interact with something, then interact with it.
		:param size: the size of the effect, in pixels
		:param pos: list with the [x,y] pos in the screen.
		:return:
		"""
		obj = self.check_interaction_group(pos , size , [characters_group , items_group])
		if obj:
			obj.interact_with(self)

	def check_interaction_group(self , pos , size , groups):
		"""
		check if a obj in a group is in that position, and return the first object in the loop.
		:param pos: list with the [x,y] pos in the screen.
		:param size: the size of the effect, in pixels
		:param groups: list of groups to check, put in order.
		:return: the FIRST object that it hits.
		"""
		for group in groups:
			print(f'trying this group: {group}')
			for obj in group:
				if self.check_hit_object(obj , pos=pos , size=size):
					return obj
		return False

	# for creating player
	def click_up(self , event):
		"""
		Saves the character when clicked with the right mouse button.
		:param event:
		:return:
		"""
		if event.button == 3:
			self.save_character()
		print(self.quests_indexes)
		super().click_up(event)