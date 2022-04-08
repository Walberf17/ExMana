"""
This will be all the cards and decks for the player.
deck it the set card of the game.
there will be 2 decks: adventure and battle
"""
import random
import math
from variables_and_definitions import *



class Deck:
	"""
	This is the class that will control the cards.
	Each deck has 3 decks inside: deck , drawn cards , discard cards.
	Each deck:
	    create the cards,
	    shuffle the cards in the deck.
	    move cards from and to deck, drawn or discard cards.
	"""
	def __init__(self , card_indexes , deck_rect , hand_rect , player):
		self.player = player
		self.deck_group = []
		self.hand = pg.sprite.Group()
		self.discard_group = []
		self.card_indexes = card_indexes
		self.deck_rect = pg.Rect(calc_proportional_size(deck_rect))
		self.hand_rect = pg.Rect(calc_proportional_size(hand_rect))
		for player in players_group:
			self.player = player
		self.create_deck()


	# handle cards in the game

	def create_deck(self):
		for card_idx in self.card_indexes:
			self.deck_group.append(Card(card_idx , self.player))

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
		return self.deck_rect.collidepoint(event.pos)

	def click_up(self , event):
		for card in self.hand:
			if card.click_up(event , self.hand_rect):
				self.card_hand_to_discard(card)


class Card(pg.sprite.Sprite):
	"""
	this class works with the cards in hand, the cards that will be shown on the screen.
	"""
	def __init__(self, idx , player , groups = None):
		if groups is None:
			groups = []
		super().__init__(*groups)
		self.rect = pg.Rect([0 , 0] , CARD_SIZE)
		this_dict = CARDS_DICT.get(idx)
		self.original_image = pg.image.load(f'{IMAGES_PATH}Cards/{idx}.png').convert()
		self.image = pg.transform.scale(self.original_image , [self.rect.w , self.rect.h])
		self.close_up_image = pg.transform.scale(self.original_image , [self.rect.w * 4 , self.rect.h * 4])
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
		self.touched = False
		self.vel = pg.Vector2(0,0)

	# handle things in game
	def click_down(self , event):
		"""
		check if the player clicked on itself
		:param pos: a tuple with the x and y position
		:return: nothing
		"""
		if self.rect.collidepoint(event.pos):
			# set itself as clicked for moving and append on clicked list
			self.touched = True
			return True

	def click_up(self , event , hand_map):
		"""
		:param event: pg.Event type
		:return:
		"""
		self.touched = False
		if not self.rect.colliderect(hand_map):
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
		for effect , duration , size in self.active_effects:
			center = pg.Vector2(self.rect.center)
			size = calc_proportional_size(size)
			for character in characters_group:
				if center.distance_to(character.rect.center) <= size:
					character.add_effects(effect , duration)

	def do_map_effects(self):
		for current_map in maps_group:
			pass


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

		# update the close up image if it is touched
		if self.touched:
			self.close_up_image_rect.bottomright = self.rect.bottomright

	def move(self , map_rect):
		"""
		moves itself in the screen_to_draw.
		When clicked, moves with the click, but move itself if not clicked to separate itself from
		:return:
		"""

		if self.touched:
			self.rect.move_ip((pg.mouse.get_rel()))
		else:
			self.rect.move_ip(self.vel)
			self.rect.clamp_ip(map_rect)

	def draw(self , screen_to_draw , central_map_rect):
		# draw a black rect for showing the sign better
		pg.draw.rect(screen_to_draw , "black" , self.rect)
		image = self.image
		rect = self.rect
		if self.touched:
			if central_map_rect.collidepoint(self.rect.center):
				image = self.close_up_image
				rect = self.close_up_image_rect
				self.player.draw_range(screen_to_draw , self.melee)
		screen_to_draw.blit(image , rect)

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