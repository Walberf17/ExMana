"""
This will be all the cards and decks for the player.
deck it the set card of the game.
there will be 2 decks: adventure and battle
"""
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
	def __init__(self , card_indexes , proportional_rect , hand_rect):
		self.deck_group = pg.sprite.Group()
		self.hand = pg.sprite.Group()
		self.discard_group = pg.sprite.Group()
		self.card_indexes = card_indexes
		self.deck_rect = pg.Rect(calc_proportional_size(proportional_rect))
		self.hand_rect = pg.Rect(calc_proportional_size(hand_rect))

	def create_hand_deck(self):
		for card in self.card_indexes:
			aqui


class Card(pg.sprite.Sprite):
	"""
	this class works with the cards in hand, the cards that will be shown on the screen.
	"""
