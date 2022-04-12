"""
Create and manage effects in the field.
"""
import random

from variables_and_definitions import *


class Effect(pg.sprite.Sprite):
	def __init__(self , idx_effect: str = "Fire" , pos = None , area = None , duration: int = 1 , action = None ,
	             groups: list = None):
		"""

		:param idx_effect: str with the name of the image
		:param pos: center of the effect's rect
		:param area: area, in meters of the effect
		:param duration: int with the duration of the effect
		:param action: str: the actual effect of this effect
		:param groups: list of groups for the effect to be inserted
		"""
		if pos is None:
			pos = [0 , 0]
		if groups is None:
			groups = []
		super().__init__(*groups)
		if area is None:
			area = [1 , 1]
		self.area = area
		self.rect = pg.Rect((0 , 0) , (calc_proportional_size(self.area)))
		self.rect.center = pos
		self.name = idx_effect
		self.original_images = None
		self.images = None
		self.sprite_grid = None
		self.sprite_size = None
		self.action = action
		self.counter = 0
		self.duration = duration
		self.get_info()
		self.image_index = [0 , 0]
		self.image_index_differ = random.randint(0 , self.sprite_grid[0])

	def get_info(self , idx = None):
		if idx is not None:
			self.name = idx
		image , self.sprite_size , self.action = EFFECT_DICT.get(self.name)
		if image:
			self.original_images = pg.image.load(f'{IMAGES_PATH}Effects/{image}.png').convert_alpha()
			self.images = self.original_images.copy()
			self.sprite_grid = self.original_images.get_size()[0] / self.sprite_size[0] , \
			                   self.original_images.get_size()[1] / self.sprite_size[1]
		else:
			self.image = None
		self.change_size_proportion()

	def change_size_proportion(self):
		"""
		Change the rect and stuff proportionally to the current map.
		Change the rect and the images
		:return: None
		"""
		self.rect = pg.Rect(self.rect.center , calc_proportional_size(self.area))
		if self.images:
			self.images = pg.transform.scale(self.original_images ,
			                                 (self.rect.w * self.sprite_grid[0] , self.rect.h * self.sprite_grid[1]))

	def draw(self , screen_to_draw):
		if self.images:  # draw the image, if any
			new_surf = pg.Surface((self.rect.size)).convert_alpha()
			new_surf.fill([0 , 0 , 0 , 0])
			new_surf.blit(self.images , (0 , 0) , self.create_rect_to_draw())
			screen_to_draw.blit(new_surf , self.rect)
		else:
			pg.draw.rect(screen_to_draw , "green" , self.rect)

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

	def update(self):
		if self.images:
			self.counter += 1
			self.image_index[0] = (
						int((self.counter * 10 / (2 * FPS)) + self.image_index_differ) % (self.sprite_grid[0]))

		if self.duration <= 0 or self.duration is None:
			self.kill()

	def next_time_click(self):
		self.update_duration()
		self.check_effect_on_obj()

	def check_effect_on_obj(self):
		# self.mask = self.image.get_masks()
		for character in characters_group:
			if self.rect.colliderect(character.rect):
				offset = pg.Vector2(character.rect.topleft) - self.rect.topleft
				a = self.get_mask().overlap_area(character.get_mask() , offset)
				if a > 0:
					eval(f'character.{self.action}')

	def get_mask(self):
		new_surf = pg.Surface((self.rect.size)).convert_alpha()
		new_surf.fill([0 , 0 , 0 , 0])
		new_surf.blit(self.images , (0 , 0) , self.create_rect_to_draw())
		mask = pg.mask.from_surface(new_surf)
		return mask

	def kill(self):
		super().kill()

	def update_duration(self):
		self.duration -= 1

	def get_kind(self):
		return self.name

	def get_size(self):
		return self.area

	def get_duration(self):
		return self.duration

	def get_pos(self):
		return self.rect.center

	def set_duration(self , value):
		self.duration = value

	def check_collision_effect(self , group_effects):
		interactions = []
		for effect in group_effects:
			if effect is not self:
				if self.rect.colliderect(effect.rect):
					new_interaction = {self , effect}
					interactions.append(new_interaction)
		return interactions
