"""
This is a internal class, a class that will be a base for other.

This class will create a character and give it default actions.
"""
import random

from variables_and_definitions import *


class Character(pg.sprite.Sprite):
	"""
	This class is a base class for other players and monsters
	"""

	def __init__(self , images_idx = None):
		"""
		:param images_idx: int
		"""
		super().__init__()

		images , sprite_size = CHARACTER_IMAGES_DICT.get(images_idx)
		sight = [60,100]
		if images:
			self.images = pg.image.load(IMAGES_PATH + images)
			self.sprite_size = sprite_size
			self.sprite_grid = self.images.get_size()[0] / self.sprite_size[0] , self.images.get_size()[1] / \
			                   self.sprite_size[1]
			self.image_index = [0 , 0]
			print(self.images.get_size())
		else:
			self.images = None
			self.sprite_size = None
			self.sprite_grid = None
			self.image_index = None
		self.sex = random.choice(["Male","Female"])
		self.sight = random.randrange(sight[0] , sight[1])/10
		if self.sex == "Female":
			self.sight *= .9
		self.rect = pg.Rect(0 , 0 , 100 , 100)
		self.max_mana = 10
		self.max_hp = 10
		self.velocity = 5
		self.max_time = 15
		self.time = 15
		self.hp = 10
		self.strength = 5  # default physical attack
		self.resilience = 5  # default physical resilience
		self.mana = 10
		self.will = 5  # default magical attack and how strong controls mana
		self.wisdow = 5  # default magical resilience
		self.status = {}  # status to calc in game
		self.equipaments = {
			"head"      : None,
			"r_hand"    : None,
			"l_hand"    : None,
			"chest"     : None,
			"legs"      : None,
			"feets"     : None,
			"r_finger"  : None,
			"l_finger"  : None,
			"neck"      : None,
		}
		self.bag = {}
		self.status = {}
		self.dominant_hand = "r_hand"
		self.ohter_hand = "l_hand"
		self.level = 1
		self.side_deck = None
		self.battle_deck = None
		self.adventure_deck = None
		self.counter = 0
		self.meelee_dist = calc_relative_size(.2)
		self.calc_status()

	def set_deck(self , deck , adventure):
		"""
		Set a deck to the player.
		:param deck: Deck object
		:param adventure: boolean
		:return: None
		"""
		if adventure:
			self.adventure_deck = deck
		else:
			self.battle_deck = deck

	def create_rect_to_draw(self):
		"""
		creates a rect to draw the correct sprite
		:return: None
		"""
		i , j = self.image_index
		w , h = self.sprite_size
		init_x = self.rect.left + (w * i)
		init_y = self.rect.top + (h * j)
		return pg.Rect(init_x , init_y , w , h)

	def create_rect_to_draw_in_status(self , size):
		"""
		creates a rect to draw the correct sprite
		:return: None
		"""
		i , j = self.image_index
		n_w , n_h = size
		max_i , max_j = self.sprite_grid
		w = n_w/max_i
		h = n_h/max_j
		init_x = self.rect.left + (w * i)
		init_y = self.rect.top + (h * j)
		return pg.Rect(init_x , init_y , w , h)

	def draw(self , screen_to_draw):
		"""
		draw itself on the given surface
		:param screen_to_draw: pg.Surface
		:return: None
		"""
		if self.images:  # draw the image, if any
			screen_to_draw.blit(self.images , self.rect , self.create_rect_to_draw())
		else:  # draw a rect to debug
			pg.draw.rect(screen_to_draw , "red" , self.rect)

	def draw_equip_screen(self , screen_to_draw , screen_to_draw_rect):
		size = pg.Vector2(screen_to_draw_rect.size).elementwise()*(2 ,.5)
		image = pg.transform.scale(self.images , size)
		new_rect = image.get_rect()
		new_clamp_rect = self.create_rect_to_draw_in_status(size)
		new_rect.size = new_clamp_rect.size
		new_rect.midleft = screen_to_draw_rect.center
		pg.draw.rect(screen_to_draw , "red" ,new_rect , 4)
		screen_to_draw.blit(image , new_rect , new_clamp_rect)

	def update(self):
		"""
		updates the image index.
		:return: None
		"""
		if self.images:
			self.counter += 1
			self.image_index[0] = int((self.counter * self.velocity / 30) % (self.sprite_grid[0]))

	def change_hp(self , value = -2):
		"""
		Do not use this directly, this is a internal to change the hp. It sets the new hp of the character.
		:param value: int
		:return: None
		"""
		self.hp += value
		self.hp = min(self.hp , self.max_hp)

	def change_mana(self , value: int = -2):
		"""
		Do not use this directly, this is a internal to change the mp. It sets the new hp of the character.
		:param value: int
		:return: None
		"""
		self.mana += value

	def change_strength(self , value):
		"""
		change the strength parameter of the character.
		:param value: int
		:return: None
		"""
		self.strength += value

	def change_resilience(self , value):
		"""
		change the resilience parameter of the character.
		:param value: int
		:return: None
		"""
		self.resilience += value

	def change_will(self , value):
		"""
		change the will parameter of the character.
		:param value: int
		:return: None
		"""
		self.will += value

	def change_wisdow(self , value):
		"""
		change the wisdow parameter of the character.
		:param value: int
		:return: None
		"""
		self.wisdow += value

	def change_max_mana(self , value):
		"""
		change the maximum mana parameter of the character.
		:param value: int
		:return: None
		"""
		self.max_mana += value

	def change_max_hp(self , value):
		"""
		change the maximum health parameter of the character.
		:param value: int
		:return: None
		"""
		self.max_hp += value

	def physical_attack(self , power):
		pass

	def magic_attack(self , power):
		pass

	def calc_status(self):
		"""
		Calc the status of this character
		:return:
		"""

		velocity = self.velocity
		hp = self.hp
		strength = self.strength
		resilience = self.resilience
		mana = self.mana
		will = self.will
		wisdow = self.wisdow
		for _ , item in self.equipaments.items():
			if item is not None:
				dict_item = EQUIPAMENTS.get(item)
				modifiers = dict_item.get("modifiers")
				for modifier , value in modifiers.items():
					match modifier:
						case "velocity":
							velocity += value
						case "hp":
							hp += value
						case "strength":
							strength += value
						case "resilience":
							resilience += value
						case "mana":
							mana += value
						case "will":
							will += value
						case "wisdow":
							wisdow += value
		self.status = {
			"velocity": velocity ,
			"hp": hp ,
			"strength": strength ,
			"resilience": resilience ,
			"mana": mana ,
			"will": will ,
			"wisdow": wisdow
		}

	def equip_item(self , item , place = None):
		"""
		Set the item in a place for the player's equipaments
		:param item: index of the item in the EQUIPAMENTS dictionary
		:param place: str with the place to put the equipaments, if None, gets the Default: 'r_hand' ,
		l_hand , head , neck , foot , legs , chest , r_finger , l_finger
		:return:
		"""
		if place is None:
			place = EQUIPAMENTS.get(item).get("place")
		if place == "2hand":
			self.unequip_item("l_hand")
			self.unequip_item("r_hand")
		if place == "hand":
			if self.equipaments.get(self.dominant_hand):
				place = self.ohter_hand
			else:
				place = self.dominant_hand
		self.equipaments[place] = item
		self.calc_status()

	def unequip_item(self , place):
		"""
		takes an item out of the place
		:param place: str
		:return: None
		"""
		if place in self.equipaments:
			self.equipaments.pop(place)
		self.calc_status()

	def get_status(self):
		"""
		returns a dictionary with the current status of the character.
		:return: dict
		"""
		return self.status

	def get_equipaments(self):
		"""
		returns a dictionary with the current equiped items
		:return:
		"""
		return self.equipaments

	def fire_damage(self , value: int = -2):
		"""
		Deals fire damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def ice_damage(self , value: int = -2):
		"""
		Deals ice damage to this character. Change if needed.
		:param value:
		:return:
		"""
		self.change_hp(value)

	def poison_damage(self , value: int = -2):
		"""
		Deals poison damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def ground_damage(self , value: int = -2):
		"""
		Deals ground damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def wind_damage(self , value: int = -2):
		"""
				Deals wind damage to this character. Change if needed.
				:param value: int
				:return: None
				"""
		self.change_hp(value)

	def electric_damage(self , value: int = -2):
		"""
		Deals electric damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def dark_damage(self , value: int = -2):
		"""
		Deals dark damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def light_damage(self , value: int = -2):
		"""
		Deals light damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def time_damage(self , value: int = -2):
		"""
		Deals time damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(4*value)

	def gravity_damage(self , value: int = -2):
		"""
		Deals gravity damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def space_damage(self , value: int = -2):
		"""
		Deals space damage to this character. Change if needed.
		:param value: int
		:return: None
		"""
		self.change_hp(value)

	def pure_damage(self , value: int = -2):
		"""
		Deals a direct damage to this character. Change if needed.
		:param value:
		:return:
		"""
		self.change_hp(value)

	def stress_damage(self  , value: int = -2):
		"""
		Deals stress damage to this character. Change if needed.
		:param value:
		:return:
		"""
		self.change_hp(value)