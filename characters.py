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
		if images_idx is None:
			images_idx = 1
		self.images_idx = images_idx
		this_character_list = CHARACTER_IMAGES_DICT.get(images_idx)
		sight = [5,10]

		# default values for this character
		self.default_strength = 5  # default physical attack
		self.default_resilience = 5  # default physical resilience
		self.default_height = random.randrange(160 , 210) / 100
		self.default_sight_meters = random.randrange(sight[0] , sight[1])
		self.sex = random.choice(["Male" , "Female"])
		if self.sex == "Female":
			self.default_sight_meters *= .9
			self.default_height -= (random.randrange(0 , 10)/100)
		self.default_mana = 10
		self.default_hp = 10
		self.default_velocity = 5
		self.default_time = 20
		self.default_will = 5  # default magical attack and how strong controls mana
		self.default_wisdom = 5  # default magical resilience
		self.default_melee_dist = self.default_height

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

		if this_character_list is None:
			this_character_list = CHARACTER_IMAGES_DICT.get(1)
		images , self.sprite_size = this_character_list

		self.original_images = pg.image.load(IMAGES_PATH + images).convert_alpha()
		self.images = self.original_images.copy()
		self.sprite_grid = self.original_images.get_size()[0] / self.sprite_size[0] , self.original_images.get_size()[1] / \
		                   self.sprite_size[1]
		self.image_index = [0 , 0]
		self.default_width = self.default_height * self.sprite_size[1] / self.sprite_size[0]
		self.rect = pg.Rect((0,0),(calc_proportional_size([self.default_height, self.default_width])))
		self.clicked = False
		self.status = {}  # status to calc in game
		self.equipments = {
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
		self.dominant_hand = "r_hand"
		self.other_hand = "l_hand"
		self.level = 1
		self.side_deck = None
		self.battle_deck = None
		self.adventure_deck = None
		self.counter = 0
		self.time_hud = pg.Rect(0,0,screen_rect.w*.034 , screen_rect.h)
		self.proportion_time_velocity = .2
		self.calc_status()
		self.change_size_proportion()


	### Change things for the game

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
		w , h = self.rect.size
		init_x = (w * i)
		init_y = (h * j)
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

	def change_size_proportion(self):
		"""
		Change the rect and stuff proportionally to the current map.
		Change the rect and the images
		:return: None
		"""
		self.rect = pg.Rect((random.randrange(800) , random.randrange(800)) , calc_proportional_size((self.width , self.height)))
		self.sight_pixels = calc_proportional_size(self.sight_meters)
		self.melee_pixels = calc_proportional_size(self.melee_meters)
		if self.images:
			self.images = pg.transform.scale(self.original_images ,
			                                 (self.rect.w * self.sprite_grid[0] , self.rect.h * self.sprite_grid[1]))
			# new_size = pg.Vector2(self.images.get_size())
			# self.sprite_size = new_size.elementwise() * self.sprite_grid


	### interactions with the player
	def click_down(self , event):
		"""
		for debug
		:param event: pg.Event
		:return: Bool
		"""
		pg.mouse.get_rel()
		if self.rect.collidepoint(event.pos):
			self.clicked = True
		return self.clicked

	def move(self):
		"""
		for debug
		:return: None
		"""
		if self.clicked:
			mouse_move = pg.mouse.get_rel()
			self.rect.move_ip(mouse_move)

	def click_up(self , event):
		"""
		for debug
		:return: None
		"""
		self.clicked = False

	def draw(self , screen_to_draw):
		"""
		draw itself on the given surface
		:param screen_to_draw: pg.Surface
		:return: None
		"""
		if self.images:  # draw the image, if any
			new_surf = pg.Surface((self.rect.size)).convert_alpha()
			new_surf.fill([0,0,0,0])
			new_surf.blit(self.images , (0,0) , self.create_rect_to_draw())
			screen_to_draw.blit(new_surf, self.rect)
		else:  # draw a rect to debug
			pg.draw.rect(screen_to_draw , "red" , self.rect)
		pg.draw.rect(screen_to_draw , "green" , self.rect , 1)
		pg.draw.rect(screen_to_draw , "red" , self.time_hud)
		# self.draw_range(screen_to_draw, False)

		# for debug
		# txt = main_menu_font.render(str(self.duration) , True , "red" , "black")
		# screen_to_draw.blit(txt , (0,0))

	def draw_range(self , screen_to_draw , meele = True):
		"""
		Draw a circle for the given range of the attack
		:param screen_to_draw: pg.Surface
		:param meele: Bool
		:return: None
		"""
		melee_dist = self.melee_pixels
		if meele:  # draws a smaller circle, with the range of the meelee attack
			new_surf = pg.Surface([melee_dist*2]* 2).convert_alpha()
			new_surf.fill([0,0,0,0])
			new_surf_rect = new_surf.get_rect()
			pg.draw.circle(new_surf , [0,0,255,150] , (new_surf_rect.w/2,new_surf_rect.h/2) , melee_dist)
			pg.draw.circle(new_surf , [0,0,0,0] , (new_surf_rect.w/2,new_surf_rect.h/2) , melee_dist /2)
		else: # draws a smaller circle, based on the sight_pixels of the character
			sight_dist = self.sight_pixels
			new_surf = pg.Surface([sight_dist*2] * 2).convert_alpha()
			new_surf.fill([0,0,0 , 0])
			new_surf_rect = new_surf.get_rect()
			pg.draw.circle(new_surf , [0 , 0 , 255 , 150] , (new_surf_rect.w/2,new_surf_rect.h/2) , sight_dist)
			pg.draw.circle(new_surf , [0 , 0 , 0 , 0] , (new_surf_rect.w/2,new_surf_rect.h/2) , melee_dist)

		new_surf_rect.center = self.rect.center
		# pg.draw.rect(screen_to_draw , "black" , new_surf_rect)
		screen_to_draw.blit(new_surf , new_surf_rect)

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
		# updates the image
		if self.images:
			self.counter += 1
			self.image_index[0] = int((self.counter * self.velocity / (2*FPS)) % (self.sprite_grid[0]))

		# updates the hud of duration
		if self.time > 0:
			self.time += - 1/FPS
			dtime = self.time/self.default_time
			self.time_hud.h = screen_rect.h*dtime
			self.time_hud.bottomright = screen_rect.bottomright


	# change Default Status

	def change_images_idx(self , value):
		self.images_idx = value
		this_character_list = CHARACTER_IMAGES_DICT.get(value)
		if this_character_list is None:
			this_character_list = CHARACTER_IMAGES_DICT.get(1)
		images , self.sprite_size = this_character_list
		self.original_images = pg.image.load(IMAGES_PATH + images).convert_alpha()
		self.images = self.original_images.copy()
		self.sprite_grid = self.original_images.get_size()[0] / self.sprite_size[0] , \
		                   self.original_images.get_size()[1] / self.sprite_size[1]
		self.image_index = [0 , 0]
		self.default_width = self.default_height * self.sprite_size[1] / self.sprite_size[0]
		self.change_size_proportion()

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
		self.default_height += value

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
		self.hp = min(self.hp , self.default_hp)

	def change_mana(self , value: int = -2):
		"""
		Do not use this directly, this is a internal to change the mp. It sets the new hp of the character.
		:param value: int
		:return: None
		"""
		self.mana += value


	# actions

	def move_card(self , value):
		pass

	def physical_attack(self , power):
		pass

	def magic_attack(self , power):
		pass

	def calc_status(self):
		"""
		Calc the status of this character
		:return:
		"""
		strength = self.default_strength
		resilience = self.default_resilience
		height = self.default_height
		sight_meters = self.default_sight_meters
		mana = self.default_mana
		hp = self.default_hp
		velocity = self.default_velocity
		time = self.default_time
		will = self.default_will
		wisdow = self.default_wisdom
		melee_dist = self.melee_meters
		for _ , item in self.equipments.items():
			if item is not None:
				dict_item = EQUIPAMENTS_DICT.get(item)
				modifiers = dict_item.get("modifiers")
				for modifier , value in modifiers.items():
					match modifier:
						case "height":
							height += value
						case "melee_meters":
							melee_dist += value
						case "sight":
							sight_meters += value
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
						case "wisdom":
							wisdow += value

		self.strength = strength
		self.resilience = resilience
		self.height = height
		self.sight_meters = sight_meters
		self.sight_pixels = calc_proportional_size(self.sight_meters)
		self.mana = mana
		self.hp = hp
		self.velocity = velocity
		self.default_time = self.time = time + self.proportion_time_velocity*self.velocity
		self.will = will
		self.wisdom = wisdow
		self.width = self.height * self.sprite_size[1] / self.sprite_size[0]
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
		"strength" : self.strength,
		"resilience" : self.resilience,
		"height" : self.height,
		"sight_meters" : self.sight_meters,
		"mana" : self.mana,
		"hp" : self.hp,
		"velocity" : self.velocity,
		"duration" : self.time,
		"will" : self.will,
		"wisdom" : self.wisdom,
		"melee_meters" : self.melee_meters,
		}
		return status_dict

	def get_equipaments(self):
		"""
		returns a dictionary with the current equiped items
		:return:
		"""
		return self.equipments

	# Effects

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
		self.change_hp(4*value)

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
			value = max(0 , value - self.wisdom)
		else:
			value = min(0 , value - self.wisdom)
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
		if value > 0:
			value = max(0 , value - self.wisdom-random.randint(self.will))
		else:
			value = min(0 , value - self.wisdom-random.randint(self.will))
		self.change_hp(value)

	def physical_damage(self , value: int = -2):
		"""
		Deals physical damage to this character. Change if needed.
		:param value:
		:return:
		"""
		if value > 0:
			value = max(0 , value - self.resilience)
		else:
			value = min(0 , value - self.resilience)
		self.change_hp(value)

	def oil_damage(self , value: int = -2):
		if value > 0:
			value = max(0 , value - self.resilience)
		else:
			value = min(0 , value - self.resilience)
		self.velocity -= int(value/2)
		self.change_hp(value)

	def calc_new_size(self):
		"""
		Calculate the new size of the rect, to look proportional to the map
		:return:
		"""
		self.rect = pg.Rect((0 , 0) , calc_proportional_size((self.width , self.height)))

	def save_player(self):
		new_dict = {
			'images_idx'            :       self.images_idx,
			'default_strength'      :       self.default_strength ,
			'default_resilience'    :       self.default_resilience ,
			'default_height'        :       self.default_height ,
			'default_sight_meters'  :       self.default_sight_meters ,
			'sex'                   :       self.sex ,
			'default_mana'          :       self.default_mana ,
			'default_hp'            :       self.default_hp ,
			'default_velocity'      :       self.default_velocity ,
			'default_time'          :       self.default_time ,
			'default_will'          :       self.default_will ,
			'default_wisdom'        :       self.default_wisdom ,
			'default_melee_dist'    :       self.default_melee_dist ,
			'level'                 :       self.level ,
			'bag'                   :       self.bag,
			'equipments'            :       self.equipments,
			'dominant_hand'         :       self.dominant_hand,
			'other_hand'            :       self.other_hand,
		}
		return new_dict

	def load_player(self , new_dict):
		self.images_idx = new_dict.get('images_idx')
		self.default_strength = new_dict.get('default_strength')
		self.default_resilience = new_dict.get('default_resilience')
		self.default_height = new_dict.get('default_height')
		self.default_sight_meters = new_dict.get('default_sight_meters')
		self.sex = new_dict.get('sex')
		self.default_mana = new_dict.get('default_mana')
		self.default_hp = new_dict.get('default_hp')
		self.default_velocity = new_dict.get('default_velocity')
		self.default_time = new_dict.get('default_time')
		self.default_will = new_dict.get('default_will')
		self.default_wisdom = new_dict.get('default_wisdom')
		self.default_melee_dist = new_dict.get('default_melee_dist')
		self.level = new_dict.get('level')
		self.bag = new_dict.get('bag')
		self.equipments = new_dict.get('equipments')
		self.dominant_hand = new_dict.get('dominant_hand')
		self.other_hand = new_dict.get('other_hand')
		self.calc_status()
		self.change_size_proportion()
