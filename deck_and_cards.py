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

	def create_deck(self):
		for card_idx in self.card_indexes:
			self.deck_group.append(Card(card_idx , self, self.player))

	def create_hand_deck(self):
		for card in self.card_indexes:
			self.deck_group.append(Card(card , self.player))

	def shuffle_main_deck(self):
		random.shuffle(self.deck_group)

	def shuffle_discard_group(self):
		random.shuffle(self.deck_group)

	def card_deck_to_hand(self , card = 0):
		"""
		Takes the first card of the deck and add it to hand group.
		:return: None
		"""
		self.hand.add(self.deck_group[card])
		self.deck_group.pop(card)

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
		self.deck_group.insert(0 , card)
		card.kill()

	def card_hand_to_discard(self , card):
		"""
		Takes a given card of the hand and add it to discard group.
		:return: None
		"""
		self.discard_group.append(card)
		card.kill()

	def card_discard_to_hand(self , card = -1):
		self.hand.add(self.discard_group[card])
		self.discard_group.pop(card)

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
			self.card_deck_to_hand()
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
		Animations.__init__(self , images_idx = idx , area = (1,2) , dict_with_image = CARDS_IMAGES , rect_to_be = screen_rect , pos = (random.randint( 1 , screen_rect.w) , screen_rect.h*.95))
		self.rect = pg.Rect([0 , 0] , CARD_SIZE)
		this_dict = CARDS_DICT.get(idx)
		self.close_up_image = pg.transform.scale(self.original_images , [self.rect.w * 4 , self.rect.h * 4])
		self.close_up_image.set_alpha(220)
		self.close_up_image_rect = self.close_up_image.get_rect()
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
	def click_up(self , event):
		"""
		:param event: pg.Event type
		:return:
		"""
		if self.clicked:
			self.clicked = False
			if self.deck.map_rect.collidepoint(self.rect.center):
				if self.player.check_in_range(self.rect.center , self.melee):
					if self.player.check_cost(self.cost):
						self.do_action()
			return True

	def do_action(self):
		self.player.consume_cost(self.cost)
		if self.active_effects:
			self.do_active_effects()
		if self.map_effect:
			self.do_map_effects()

	def do_active_effects(self):
		print(self.active_effects)
		for kind , effect , duration , size in self.active_effects:
			center = pg.Vector2(self.rect.center)
			size = calc_proportional_size(size)
			for character in characters_group:
				if center.distance_to(character.rect.center) <= size:
					character.add_effects(effect , duration)

	def do_map_effects(self):
		pos = pg.mouse.get_pos()
		for current_map in maps_group:
			for kind , action , duration , area in self.map_effect:
				current_map.add_effects(effect_index = kind , pos = pos , area = area , duration = duration , action = action)

	def update(self , hand_cards):
		"""
		calcs the forces to move itself.
		Calcs the position for the close up image
		:return:
		"""

		# calc the force and angule for each card it is touching
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
		# draw a black rect for showing the sign better
		pg.draw.rect(screen_to_draw , "black" , self.rect)
		image = self.images
		rect = self.rect
		if self.clicked:
			if self.deck.map_rect.collidepoint(self.rect.center):
				image = self.close_up_image
				rect = self.close_up_image_rect
				self.player.draw_range(screen_to_draw , self.melee)
		screen_to_draw.blit(image , rect)
		pg.draw.rect(screen_to_draw , 'red' , rect)

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