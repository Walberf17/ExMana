"""
Create and manage effects in the field.
"""
from pygame.sprite import AbstractGroup , Sprite

from variables_and_definitions import *

class Effects(Sprite):
	def __init__(self , idx_effect: int = 1 , area = None , time: int = 1 , *groups:AbstractGroup):
		super().__init__(*groups)
		self.idx_effect = idx_effect
		self.image , self.name = EFFECT_IMAGES_DICT.get(idx_effect)
		if area is None:
			area = [1,1]
		self.area = calc_proportional_size(area)
		self.time = FPS*time

	def draw(self , screen_to_draw):
		pass

	def update(self):
		pass

	def do_effect(self):
		pass

	def kill(self):
		super().kill()