"""
Class to work with moving objects
"""
from variables import *

class MovingObj:
	def __init__(self):
		self.clicked = False
		moving_objects_group.add(self)


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