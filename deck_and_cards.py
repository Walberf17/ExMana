"""
This will be all the cards and decks for the player.
deck it the set card of the game.
there will be 2 decks: adventure and battle
"""
import random
import math
from variables import *
from pygame.sprite import Sprite
from animations import Animations
from moving_object import MovingObj
from definitions import *



class Deck:
	"""
	This is the class that will control the cards.
	Each deck has 3 decks inside: deck , drawn cards , discard cards.
	Each deck:
	    create the cards,
	    shuffle the cards in the deck.
	    move cards from and to deck, drawn or discard cards.
	"""
	def __init__(self , card_indexes = None , deck_rect=(0*screen_rect.w,.8*screen_rect.h,.1*screen_rect.w,.1*screen_rect.h) , hand_rect = None , map_rect = None , player = None):
		self.player = player
		self.deck_group = []
		self.hand = pg.sprite.Group()
		self.discard_group = []
		self.card_indexes = card_indexes
		self.deck_rect = pg.Rect(deck_rect)
		self.hand_rect = pg.Rect(hand_rect)
		self.map_rect = map_rect
		self.player = player
		self.clicked =False
		decks_group.add(self)
		self.create_deck()


	# handle cards in the game

	def create_deck(self , card_list = None):
		if card_list is None:
			card_list = self.card_indexes
		self.deck_group.extend(card_list)

	def new_card(self , card_list):
		"""
		adds a new card to the deck in the current play
		:param card_list: Union of float, int,str or list
		:return: None
		"""
		if type(card_list) in [float , int , str]:
			card_list = [card_list]
		self.create_deck(card_list = card_list)
		self.shuffle_main_deck()
		add_cards_to_deck(cards_list = card_list)

	def shuffle_main_deck(self):
		random.shuffle(self.deck_group)

	def shuffle_discard_group(self):
		random.shuffle(self.deck_group)

	def card_deck_to_hand(self , card_idx = 0):
		"""
		Takes the first card of the deck and add it to hand group.
		:return: None
		"""
		# Card(card , self.player)
		Card(idx = self.deck_group[card_idx], deck = self, player = self.player , groups = [self.hand])
		self.deck_group.pop(card_idx)

	def card_deck_to_discard(self , card = 0):
		"""
		Takes the first card of the deck and add it to discard group.
		:return: None
		"""
		self.discard_group.append(self.deck_group[card])
		self.deck_group.pop(card)

	def card_hand_to_deck(self , card):
		"""
		Takes a given card of the hand and add it to deck group.
		:return: None
		"""
		self.deck_group.insert(0 , card.idx)
		card.kill()

	def card_hand_to_discard(self , card):
		"""
		Takes a given card of the hand and add it to discard group.
		:return: None
		"""
		self.discard_group.append(card.idx)
		card.kill()

	def card_discard_to_hand(self , card_idx = -1):
		self.hand.add(Card(idx = self.deck_group[card_idx], deck = self, player = self.player , groups = [self.hand]))
		self.discard_group.pop(card_idx)

	def card_discard_to_deck(self , card = -1):
		self.deck_group.append(self.discard_group[card])
		self.discard_group.pop(card)

	# update, movement and stuff
	def click_down(self , event):
		"""
		check if the player clicked on itself
		:param pos: a tuple with the x and y position
		:return: nothing
		"""
		self.clicked = self.deck_rect.collidepoint(event.pos)
		if self.clicked:
			if self.deck_group:
				self.card_deck_to_hand()
			else:
				print('no more cards')
		return self.clicked

	def click_up(self , event):
		return

	def draw(self , screen_to_draw):
		pg.draw.rect(screen_to_draw , 'green' , self.deck_rect)
		for card in self.hand:
			card.draw(screen_to_draw)

class Card(Sprite , Animations , MovingObj):
	"""
	this class works with the cards in hand, the cards that will be shown on the screen.
	"""
	def __init__(self, idx , deck , player , groups = None):
		if groups is None:
			groups = []
		Sprite.__init__(self , *groups)
		MovingObj.__init__(self)
		Animations.__init__(self , images_idx = idx , area = (1,1.4) , dict_with_images = CARDS_IMAGES , rect_to_be = screen_rect , pos = (random.randint( 1 , screen_rect.w) , screen_rect.h*.95))
		this_dict = CARDS_DICT.get(idx)
		if self.images:
			self.close_up_image = pg.transform.scale(self.original_images , [self.rect.w * 3 , self.rect.h * 3])
			self.zoom_out_image = pg.transform.scale(self.original_images , (self.rect.w*.4 , self.rect.h*.4))
		else:
			self.close_up_image = pg.Surface(self.rect.size)
			self.zoom_out_image = pg.Surface((self.rect.w * .4 , self.rect.h * .4))
		self.close_up_image.set_alpha(200)
		self.zoom_out_image.set_alpha(200)
		self.close_up_image_rect = self.close_up_image.get_rect()
		self.zoom_out_image_rect = self.zoom_out_image.get_rect()
		self.idx = idx
		self.name = this_dict.get('name')
		self.active_effects = this_dict.get('active_effects')
		self.map_effect = this_dict.get('map_effect')
		self.cost = this_dict.get('cost')
		self.melee = this_dict.get('melee')
		self.player = player
		self.acc = [0,0]
		self.clicked = False
		self.vel = pg.Vector2(0,0)
		self.deck = deck

	# handle things in game
	def change_size_proportion(self):
		"""
		Change the max_rect and stuff proportionally to the current map.
		Change the max_rect and the images
		:return: None
		"""
		self.rect = pg.Rect(self.rect.topleft , calc_proportional_size(self.area , max_area = [7,7], max_rect = self.rect_to_be ))
		if self.images:
			self.images = pg.transform.scale(self.original_images , (self.rect.w * self.sprite_grid[0] , self.rect.h * self.sprite_grid[1]))

	def click_up(self , event):
		"""
		:param event: pg.Event type
		:return:
		"""
		if self.clicked:
			self.clicked = False
			if self.deck.map_rect.collidepoint(self.rect.center):
				if self.player.check_in_range(self.melee):
					if self.player.check_cost(self.cost):
						self.do_action()
						self.kill()
			return True

	def do_action(self):
		self.player.consume_cost(self.cost)
		if self.active_effects:
			self.do_active_effects()
		if self.map_effect:
			self.do_map_effects()

	def do_active_effects(self):
		for kind , effect , duration , size in self.active_effects:
			multiplier = self.player.get_multiplier(effect)
			size = calc_proportional_size(size)
			if type(size) == list:
				size = [size[0]*multiplier , size[1] * multiplier]
			else:
				size *= multiplier
			if kind in ["Smell" , "Taste" , "Sight" , "Search" , "Throughtful Search" , 'Get' , 'Move']:
				eval(f'self.player.{effect}')
			else:
				center = pg.Vector2(self.rect.center)
				for character in characters_group:
					match size:
						case int(x) | float(x):
							if center.distance_to(character.rect.center) <= x:
								character.add_effects(kind , effect , duration)
						case [x , y]:
							effect_rect = pg.Rect((0,0) , calc_proportional_size([x,y]))
							effect_rect.center = center
							if character.rect.colliderect(effect_rect):
								character.add_effects(kind , effect , duration)

	def do_map_effects(self):
		pos = pg.mouse.get_pos()
		for current_map in maps_group:
			for kind , action , duration , area in self.map_effect:
				multiplier = self.player.get_multiplier(kind)
				if type(area) == list:
					area = [area[0] * multiplier , area[1] * multiplier]
				else:
					area *= multiplier
				current_map.add_effect(idx_effect = kind, pos = pos , area = area , duration = duration , action = action)

	def update(self):
		"""
		calcs the forces to move itself.
		Calcs the position for the close up image
		:return:
		"""

		# calc the force and angule for each card it is touching
		hand_cards = self.deck.hand

		for card in hand_cards:
			if card != self:  # not checking with itself
				if self.rect.colliderect(card):  # if card collide
					if self.rect.center == card.rect.center:  # move a little bit if 2 rects are the same possition
						self.rect.move_ip(int(random.random()*10),0)
					ang = get_ang(self , card)  # calcs the angule
					self.acc += pg.math.Vector2(-math.cos(ang) * FORCE_TO_CARDS , -math.sin(
						ang) * FORCE_TO_CARDS)  # sums all the vector acc with the new vector from the force for the angule

		# calcs the new velocity
		self.vel += self.acc
		self.vel *= 0.9

		# set the acc 0 for the new cycle
		self.acc = (0 , 0)

		# update the close up image if it is clicked
		if self.clicked:
			self.close_up_image_rect.bottomright = self.rect.bottomright

	def move(self):
		"""
		moves itself in the screen_to_draw.
		When clicked, moves with the click, but move itself if not clicked to separate itself from
		:return:
		"""
		MovingObj.move(self)
		if not self.clicked:
			self.rect.move_ip(self.vel)
			self.rect.clamp_ip(self.deck.hand_rect)

	def draw(self , screen_to_draw):
		"""
		draw itself on the surface.
		If not clicked, draw from Animations,
		if clicked and not in the map, zoom, else, draw the ranges of its use.
		:param screen_to_draw:
		:return:
		"""
		if self.clicked:
			if self.deck.map_rect.collidepoint(self.rect.center):
				self.zoom_out_image_rect.center = pg.mouse.get_pos()
				if self.images:
					screen_to_draw.blit(self.zoom_out_image , self.zoom_out_image_rect)
				if self.player.check_in_range(self.melee) or self.images is None:
					self.draw_range(screen_to_draw)
			else:
				image = self.close_up_image
				rect = self.close_up_image_rect
				rect.bottomright = self.rect.bottomright
				screen_to_draw.blit(image , rect)
			self.player.draw_range(screen_to_draw , self.melee)
			self.player.draw_cost(self , screen_to_draw)
		else:
			Animations.draw(self , screen_to_draw)

	def draw_range(self , screen_to_draw):
		"""
		Draw a rect_to_be in the ranges of the effects on the screen
		:param screen_to_draw:
		:return:
		"""
		if self.active_effects:
			self.draw_range_active(screen_to_draw)

		if self.map_effect:
			self.draw_range_map(screen_to_draw)

	def draw_range_map(self , screen_to_draw):
		"""
		draw the range of the effects that will be added to the map.
		:param screen_to_draw: pg.Surface
		:return:
		"""
		for effect in self.map_effect:
			color = pg.Color('green')
			dist = calc_proportional_size(effect[3])
			multiplier = self.player.get_multiplier(effect)
			if type(dist) in [float , int]:
				new_surf = pg.Surface([x * 2 * multiplier] * 2).convert_alpha()
				new_surf.fill([0 , 0 , 0 , 0])
				new_surf_rect = new_surf.get_rect()
				pg.draw.circle(new_surf , color , (new_surf_rect.w / 2 , new_surf_rect.h / 2) , dist)
				new_surf.set_alpha(160)
				screen_to_draw.blit(new_surf , (-pg.Vector2(new_surf_rect.size) / 2 + self.zoom_out_image_rect.center) , new_surf_rect)
			elif len(dist) == 2:
				x , y = dist
				new_surf = pg.Surface([x * multiplier , y * multiplier]).convert_alpha()
				new_surf.fill(color)
				new_surf_rect = new_surf.get_rect()
				new_surf.set_alpha(160)
				screen_to_draw.blit(new_surf , (-pg.Vector2(new_surf_rect.size) / 2 + self.zoom_out_image_rect.center) , new_surf_rect)

	def draw_range_active(self , screen_to_draw):
		"""
		draw the range of the active effects of the card
		:param screen_to_draw: pg.Surface
		:return: None
		"""

		for effect in self.active_effects:
			color = pg.Color('blue')
			dist = calc_proportional_size(effect[3])
			alpha = 160
			multiplier = self.player.get_multiplier(effect)
			if type(dist) in [float , int]:
				new_surf = pg.Surface([dist * 2 * multiplier] * 2).convert_alpha()
				new_surf.fill([0 , 0 , 0 , 0])
				new_surf_rect = new_surf.get_rect()
				pg.draw.circle(new_surf , color , (new_surf_rect.w / 2 , new_surf_rect.h / 2) , dist)
				new_surf.set_alpha(alpha)
				screen_to_draw.blit(new_surf , (-pg.Vector2(new_surf_rect.size) / 2 + self.zoom_out_image_rect.center) , new_surf_rect)
			elif len(dist) == 2:
				x , y = dist
				new_surf = pg.Surface([x * multiplier , y * multiplier]).convert_alpha()
				new_surf.fill(color)
				new_surf_rect = new_surf.get_rect()
				new_surf.set_alpha(alpha)
				screen_to_draw.blit(new_surf , (-pg.Vector2(new_surf_rect.size) / 2 + self.zoom_out_image_rect.center) , new_surf_rect)

def get_ang(card1 , card2):
	"""
	calcs the angle from 2 diferent cards
	:param card1: Card object
	:param card2: Card object
	:return: angle in radians
	"""
	x1 , y1 = card1.rect.center
	x2 , y2 = card2.rect.center
	return math.atan2((y2 - y1) , (x2 - x1))