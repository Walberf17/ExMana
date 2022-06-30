"""
This is a internal class, a class that will be a base for other.

This class will create a character and give it default actions.
"""
import random
from images_info import CHARACTER_IMAGES_DICT
from items_info import *
from variables import *
from definitions import *
from animations import Animations
from moving_object import MovingObj
from math import cos , sin
import json


class Character(Animations , MovingObj):
	"""
	This class is a base class for other players and monsters
	"""

	def __init__(self , images_idx = None , rect_to_be = screen_rect ,
	             groups = None , pos = None , relative_pos = None , dict_with_images = CHARACTER_IMAGES_DICT):
		"""

		:param images_idx: image from the dictionary to get
		:param groups: groups to add
		"""
		MovingObj.__init__(self)
		self.images_idx = images_idx
		loaded_dict = self.load_character()
		if loaded_dict:
			self.default_width = float(loaded_dict.get('default_width'))
			self.default_height = float(loaded_dict.get('default_height'))
			self.images_idx = float(loaded_dict.get('images_idx'))
			self.default_strength = float(loaded_dict.get('default_strength'))
			self.default_resilience = float(loaded_dict.get('default_resilience'))
			self.default_sight_meters = float(loaded_dict.get('default_sight_meters'))
			self.sex = loaded_dict.get('sex')
			self.default_mana = float(loaded_dict.get('default_mana'))
			self.default_hp = float(loaded_dict.get('default_hp'))
			self.default_velocity = float(loaded_dict.get('default_velocity'))
			self.default_time = float(loaded_dict.get('default_time'))
			self.default_will = float(loaded_dict.get('default_will'))
			self.default_wisdom = float(loaded_dict.get('default_wisdom'))
			self.default_melee_dist = float(loaded_dict.get('default_melee_dist'))
			self.level = float(loaded_dict.get('level'))
			self.bag = loaded_dict.get('bag')
			self.equipments = loaded_dict.get('equipments')
			self.dominant_hand = loaded_dict.get('dominant_hand')
			self.other_hand = loaded_dict.get('other_hand')
			self.proportion_time_velocity = loaded_dict.get('proportion_time_velocity')
			self.effects = loaded_dict.get('effects')
			self.abnormal_effects = loaded_dict.get('abnormal_effects')
			rect_center = loaded_dict.get('rect_center')
			print(self.default_width , 'width')
			Animations.__init__(self , images_idx = self.images_idx , area = [self.default_width , self.default_height] ,
			                    dict_with_images = dict_with_images , rect_to_be = rect_to_be , pos = pos ,
			                    groups = groups)
			self.rect.center = rect_center

		else:
			self.default_height = random.randrange(160 , 210) / 100
			self.default_width = random.randrange(30 , 60) / 100
			Animations.__init__(self , images_idx = self.images_idx , area = [self.default_width , self.default_height] ,
			                    dict_with_images = dict_with_images , rect_to_be = rect_to_be , pos = pos ,
			                    relative_pos = relative_pos , groups = groups)
			sight = [5 , 10]

			# default values for this character
			self.default_strength = 5  # default physical attack
			self.default_resilience = 5  # default physical resilience
			self.default_sight_meters = random.randrange(sight[0] , sight[1])
			self.sex = random.choice(["Male" , "Female"])
			if self.sex == "Female":
				self.default_sight_meters *= .9
				self.default_height -= (random.randrange(0 , 10) / 100)
			self.default_mana = 10
			self.default_hp = 10
			self.default_velocity = 5
			self.default_time = 10000
			self.default_will = 5  # default magical attack and how strong controls mana
			self.default_wisdom = 5  # default magical resilience
			self.default_melee_dist = self.default_height/2

		# changed status
		self.strength = self.default_strength
		self.resilience = self.default_resilience
		self.height = self.default_height
		self.sight_meters = self.default_sight_meters
		self.sigh_pixels = calc_proportional_size(self.sight_meters)
		self.mana = self.default_mana
		self.hp = self.default_hp
		self.velocity = self.default_velocity
		self.time = self.default_time
		self.will = self.default_will
		self.wisdom = self.default_wisdom
		self.melee_meters = self.default_melee_dist
		self.melee_pixels = calc_proportional_size(self.melee_meters)
		self.clicked = False
		self.status = {}  # status to calc in game
		self.equipments = {
			"head": None ,
			"r_hand": None ,
			"l_hand": None ,
			"chest": None ,
			"legs": None ,
			"feets": None ,
			"r_finger": None ,
			"l_finger": None ,
			"neck": None ,
		}
		self.bag = {}
		self.dominant_hand = "r_hand"
		self.other_hand = "l_hand"
		self.level = 1
		self.side_deck = None
		self.main_deck = None
		self.time_hud = pg.Rect(0 , 0 , screen_rect.w * .034 , screen_rect.h)
		self.proportion_time_velocity = .2
		self.effects = []
		self.abnormal_effects = {}
		self.next_action = []
		self.calc_status()
		self.change_sizes_proportion()
		self.to_move_point = pg.Vector2(self.rect.center)


	# Administration of the character

	def save_character(self):
		new_dict = {
			'default_height': self.default_height,
			'default_width': self.default_width,
			'images_idx': self.images_idx ,
			'default_strength': self.default_strength ,
			'default_resilience': self.default_resilience ,
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
			'proportion_time_velocity': self.proportion_time_velocity,
			'effects': self.effects,
			'abnormal_effects': self.abnormal_effects,
			'rect_center': self.rect.center,
		}
		with open(f'./DataInfo/character{self.images_idx}.json' , 'w') as file:
			json.dump(new_dict , file)

	def load_character(self):
		try:
			with open(f'./DataInfo/character{self.images_idx}.json' , 'r') as file:
				new_dict = json.load(file)
				return new_dict
		except FileNotFoundError:
			print('Nenhum arquivo. Vou fechar e vc se vira...')
			return {}

	### Change things for the game

	def change_sizes_proportion(self):
		"""
		Change the max_rect and stuff proportionally to the current map.
		Change the max_rect and the images
		:return: None
		"""
		Animations.change_size_proportion(self)
		self.sight_pixels = calc_proportional_size(self.sight_meters)
		self.melee_pixels = calc_proportional_size(self.melee_meters)

	### interactions with the player

	def draw(self , screen_to_draw):
		"""
		draw itself on the given surface
		:param screen_to_draw: pg.Surface
		:return: None
		"""
		Animations.draw(self , screen_to_draw)

	def update(self , **kwargs):
		"""
		updates the image index.
		:param **kwargs:
		:return: None
		"""
		MovingObj.update(self)
		Animations.update(self , self.velocity)


		# do the next action
		if self.next_action and self.image_index[1] in [0]:
			kind = self.next_action[0][0].get_kind()
			self.change_state(kind)

		# check if it stopped moving
		if self.states_names[self.image_index[1]] in ['Run']:
			x , y = self.moving_velocity
			x , y = abs(x) , abs(y)
			if x < 1 and y <1:
				self.change_state()

		# check hp
		if self.hp <= (0 - self.will // 10):
			self.kill()

	def get_mask(self):
		new_surf = pg.Surface(self.rect.size).convert_alpha()
		new_surf.fill([0 , 0 , 0 , 0])
		new_surf.blit(self.images , (0 , 0) , self.create_rect_to_draw())
		mask = pg.mask.from_surface(new_surf)
		return mask

	def kill(self):
		Animations.kill(self)

	# change Default Status

	def change_default_strength(self , value):
		"""
		change the strength parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_strength += value

	def change_default_resilience(self , value):
		"""
		change the resilience parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_resilience += value

	def change_default_height(self , value):
		proport = 1 + (value / self.default_height)
		self.default_height *= proport
		self.area[1] *= proport
		self.change_sizes_proportion()

	def change_default_width(self):
		proport = 1 + (value / self.default_width)
		self.default_width *= proport
		self.area[0] *= proport
		self.change_sizes_proportion()

	def change_default_sight(self , value):
		self.default_sight_meters += value

	def change_sex(self , value):
		self.sex = value

	def change_default_mana(self , value):
		"""
		change the maximum mana parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_mana += value

	def change_default_hp(self , value):
		"""
		change the maximum health parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_hp += value

	def change_default_velocity(self , value):
		"""
		change the maximum velocity parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_velocity += value

	def change_default_time(self , value):
		"""
		change the maximum duration parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_time += value

	def change_default_will(self , value):
		"""
		change the will parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_will += value

	def change_default_wisdom(self , value):
		"""
		change the wisdom parameter of the character.
		:param value: int
		:return: None
		"""
		self.default_wisdom += value

	def change_default_melee_dist(self , value):
		self.default_melee_dist += value

	def change_level(self , value = 1):
		self.level += value

	def change_dominant_hand(self , value):
		self.dominant_hand = value

	def change_other_hand(self , value):
		self.other_hand = value

	# Change Status

	def change_strength(self , value):
		"""
		change the current strength parameter of the character.
		:param value: int
		:return: None
		"""
		self.strength += value

	def change_resilience(self , value):
		"""
		change the current resilience parameter of the character.
		:param value: int
		:return: None
		"""
		self.resilience += value

	def change_height(self , value):
		"""
		change the current height parameter of the character.
		:param value: int
		:return: None
		"""
		self.height += value

	def change_sight(self , value):
		"""
		change the current sight in meters parameter of the character.
		:param value: int
		:return: None
		"""
		self.sight_meters += value

	def change_velocity(self , value):
		"""
		change the current velocity parameter of the character.
		:param value: int
		:return: None
		"""
		self.velocity += value

	def change_time(self , value):
		"""
		change the current duration parameter of the character.
		:param value: int
		:return: None
		"""
		self.time += value

	def change_will(self , value):
		"""
		change the will parameter of the character.
		:param value: int
		:return: None
		"""
		self.will += value

	def change_wisdom(self , value):
		"""
		change the current wisdom parameter of the character.
		:param value: int
		:return: None
		"""
		self.wisdom += value

	def change_melee_dist(self , value):
		"""
		change the current melee distance parameter of the character.
		:param value: int
		:return: None
		"""
		self.melee_meters += value

	def change_hp(self , value = -2):
		"""
		Do not use this directly, this is a internal to change the hp. It sets the new hp of the character.
		:param value: int
		:return: None
		"""
		self.hp += value
		self.hp = min([self.hp , self.default_hp])

	def change_mana(self , value: int = -2):
		"""
		Do not use this directly, this is a internal to change the mp. It sets the new hp of the character.
		:param value: int
		:return: None
		"""
		self.mana += value
		self.mana = min([self.mana , self.default_mana])

	# actions

	def set_action(self , card , pos):
		"""
		set the next action to take
		:param card:
		:return:
		"""
		self.next_action.append([card , pos])

	def move_card(self , meters , pos = None):
		"""
		not ready yet, it will move the players up to that many meters
		:param meters: size in meters
		:return: None
		"""
		if pos is None:
			pos = pg.Vector2(pg.mouse.get_pos()) # the position of the mouse
		else:
			pos = pg.Vector2(calc_proportional_size(pos))+self.rect.center
		max_dist = calc_proportional_size(meters) # max distance to travel
		if pos.distance_to(self.rect.center) <= max_dist:
			self.to_move_point = pos
		else:
			ang = get_ang(self.rect.center , pos)
			self.to_move_point = pg.Vector2(max_dist*cos(ang) , max_dist*sin(ang))+self.rect.center
		self.change_state('Run')
		self.next_action.clear()

	def calc_acceleration(self):
		return

	def calc_velocity(self):
		ang = get_ang(self.rect.center , self.to_move_point)
		max_vel = 15 + self.velocity*10/100
		dist_to_point = self.to_move_point.distance_to(self.rect.center)
		max_dist = 300
		vel = dist_to_point * max_vel / max_dist
		real_vel = min([vel , max_vel])
		self.moving_velocity = pg.Vector2([(real_vel*cos(ang)) , (real_vel*sin(ang))])

	def attack(self):
		card , pos = self.next_action[0]
		card.do_action(pos)
		self.next_action.pop(0)

	def calc_status(self):
		"""
		Calc the status of this character
		:return:
		"""
		strength = self.default_strength
		resilience = self.default_resilience
		height = self.default_height
		width = self.default_width
		sight_meters = self.default_sight_meters
		mana = self.default_mana
		hp = self.default_hp
		velocity = self.default_velocity
		time = self.default_time
		will = self.default_will
		wisdom = self.default_wisdom
		melee_dist = self.melee_meters
		for _ , item in self.equipments.items():
			if item is not None:
				dict_item = EQUIPAMENTS_DICT.get(item)
				modifiers = dict_item.get("modifiers")
				modifier_dict = {"height": height,
							'width': width,
							"melee_meters": melee_dist,
							"sight": sight_meters,
							"velocity": velocity,
							"hp": hp,
							"strength": strength,
							"resilience": resilience,
							"mana": mana,
							"will": will,
							"wisdom": wisdom,
				            }
				for modifier , value in modifiers.items():
					modifier_dict[modifier] += value

		self.strength = strength
		self.resilience = resilience
		self.height = height
		self.width = width
		# self.area[0] = width
		self.sight_meters = sight_meters
		self.sight_pixels = calc_proportional_size(self.sight_meters)
		self.mana = mana
		self.hp = hp
		self.velocity = velocity
		self.default_time = self.time = time + self.proportion_time_velocity * self.velocity
		self.will = will
		self.wisdom = wisdom
		self.melee_meters = melee_dist
		self.melee_pixels = calc_proportional_size(self.melee_meters)

	def equip_item(self , item , place = None):
		"""
		Set the item in a place for the player's equipments
		:param item: index of the item in the EQUIPAMENTS_DICT dictionary
		:param place: str with the place to put the equipments, if None, gets the Default: 'r_hand' ,
		l_hand , head , neck , foot , legs , chest , r_finger , l_finger
		:return:
		"""
		if place is None:
			place = EQUIPAMENTS_DICT.get(item).get("place")
		if place == "2hand":
			self.unequip_item("l_hand")
			self.unequip_item("r_hand")
		if place == "hand":
			if self.equipments.get(self.dominant_hand):
				place = self.other_hand
			else:
				place = self.dominant_hand
		self.equipments[place] = item
		self.calc_status()

	def unequip_item(self , place):
		"""
		takes an item out of the place
		:param place: str
		:return: None
		"""
		if place in self.equipments:
			self.equipments.pop(place)
		self.calc_status()

	def get_status(self):
		"""
		returns a dictionary with the current status of the character.
		:return: dict
		"""
		status_dict = {
			"strength": self.strength ,
			"resilience": self.resilience ,
			"height": self.height ,
			"sight_meters": self.sight_meters ,
			"mana": self.mana ,
			"hp": self.hp ,
			"velocity": self.velocity ,
			"duration": self.time ,
			"will": self.will ,
			"wisdom": self.wisdom ,
			"melee_meters": self.melee_meters ,
		}
		return status_dict

	def get_equipaments(self):
		"""
		returns a dictionary with the current equiped items
		:return:
		"""
		return self.equipments

	# Effects

	def add_effects(self , kind , effect , duration):
		if duration == 0:
			eval(f'self.{effect}')
		else:
			self.effects.add([kind , effect , duration])

	def do_effects(self):
		to_remove = []
		for idx , kind , effect , duration in enumerate(self.effects):
			duration -= 1
			eval(f'self.{effect}')
			self.effects[idx][-1] = duration
			if duration == 0:
				to_remove.append(idx)
		for idx in to_remove:
			self.effects.pop(idx)

	def fire_damage(self , value: int = -2):
		"""
		Deals fire damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def ice_damage(self , value: int = -2):
		"""
		Deals ice damage to this character. Change if needed.
		:param value:
		:return:
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def poison_damage(self , value: int = -2):
		"""
		Deals poison damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def ground_damage(self , value: int = -2):
		"""
		Deals ground damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def wind_damage(self , value: int = -2):
		"""
		Deals wind damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def electric_damage(self , value: int = -2):
		"""
		Deals electric damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def dark_damage(self , value: int = -2):
		"""
		Deals dark damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def light_damage(self , value: int = -2):
		"""
		Deals light damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def time_damage(self , value: int = -2):
		"""
		Deals duration damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(4 * value)

	def gravity_damage(self , value: int = -2):
		"""
		Deals gravity damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
		self.change_hp(value)

	def space_damage(self , value: int = -2):
		"""
		Deals space damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		if value > 0:
			value = max([0 , value - self.wisdom])
		else:
			value = min([0 , value - self.wisdom])
		self.change_hp(value)

	def pure_damage(self , value: int = -2):
		"""
		Deals a direct damage to this character. Change if needed.
		:param value:
		:return:
		"""
		self.change_hp(value)

	def stress_damage(self , value: int = -2):
		"""
		Deals stress damage to this character. Change if needed.
		:param value:
		:return:
		"""
		if value > 0:
			value = max([0 , value - self.wisdom - random.randint(self.will)])
		else:
			value = min([0 , value - self.wisdom - random.randint(self.will)])
		self.change_hp(value)

	def physic_damage(self , value: int = -2):
		"""
		Deals physical damage to this character. Change if needed.
		:param value:
		:return:
		"""
		if value > 0:
			value = max([0 , value - self.resilience])
		else:
			value = min([0 , value - self.resilience])
		self.change_hp(value)

	def oil_damage(self , value: int = -2):
		if value > 0:
			value = max([0 , value - self.resilience])
		else:
			value = min([0 , value - self.resilience])
		self.velocity -= int(value / 2)
		self.change_hp(value)

	# Feels the world

	def feel_world(self , size , kind , pos = None):
		"""
		this will discover the world around the player
		:param size: the area, in meters, of the effect
		:param kind: the type sensation the player will use to discover the things
		:return: None
		"""
		if pos is None:
			pos = pg.mouse.get_pos()
		for current_map in maps_group:
			for obj in current_map.get_secrets():

				if type(size) in (int , float):
						pos = pg.Vector2(pos)
						if pos.distance_to(obj.rect.center) <= size:
							if obj.check_discover(kind):
								obj.find_me()
				elif type(size) in [list , tuple] and len(size) == 2:
						effect_rect = pg.Rect((0 , 0) , size)
						effect_rect.center = pos
						if obj.rect.colliderect(effect_rect):
							if obj.check_discover(kind):
								obj.find_me()

def get_ang(p1 , p2):
	"""
	calcs the angle from 2 diferent cards
	:param card1: Card object
	:param card2: Card object
	:return: angle in radians
	"""
	x1 , y1 = p1
	x2 , y2 = p2
	return math.atan2((y2 - y1) , (x2 - x1))