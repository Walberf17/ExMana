"""
Class to work with moving objects
"""
from variables import *
from pygame import Vector2

class MovingObj:
	def __init__(self):
		self.clicked = False
		self.acceleration = Vector2(0 , 0)
		self.moving_velocity = Vector2(0,0)
		moving_objects_group.add(self)


	def click_down(self , event):
		"""
		for debug
		:param event: pg.Event
		:return: Bool
		"""
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
			self.to_move_point = pg.Vector2(pg.mouse.get_pos())
		self.rect.move_ip(self.moving_velocity)


	def click_up(self , event):
		"""
		for debug
		:return: None
		"""
		self.clicked = False


	def update(self):
		"""
		updates the object acceleration and velocity
		:return:
		"""
		self.calc_acceleration()
		self.calc_velocity()

	def calc_acceleration(self):
		pass

	def calc_velocity(self):
		"""
		sums the velocity to the acceleration, zeroes the acceleration, and does a dragging of the velocity
		:return:
		"""
		self.moving_velocity += self.acceleration
		self.moving_velocity *= .9
		self.acceleration *= 0
