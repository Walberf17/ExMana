"""
Create and manage effects in the field.
"""
from variables_and_definitions import *

class Effect(pg.sprite.Sprite):
	def __init__(self , idx_effect: int = 1 , pos = [0,0] , area = None , duration: int = 1 , groups = None):
		if groups is None:
			groups = []
		super().__init__(*groups)
		self.idx_effect = idx_effect
		self.image_index = [0 , 0]
		if area is None:
			area = [4,4]
		self.area = area
		self.rect = pg.Rect((0 , 0) , (calc_proportional_size(self.area)))
		image , self.name , self.sprite_size = EFFECT_IMAGES_DICT.get(idx_effect)
		if image:
			self.original_images = pg.image.load(f'{IMAGES_PATH}{image}').convert_alpha()
			self.images = self.original_images.copy()
			self.sprite_grid = self.original_images.get_size()[0] / self.sprite_size[0] ,\
			                   self.original_images.get_size()[1] / self.sprite_size[1]
		else:
			self.image = None
		self.counter = 0
		self.duration = duration
		print(self.sprite_size , "sprite size")
		print(self.sprite_grid , "sprite grid")
		self.change_size_proportion()

	def change_size_proportion(self):
		"""
		Change the rect and stuff proportionally to the current map.
		Change the rect and the images
		:return: None
		"""
		self.rect = pg.Rect((0 , 0) , calc_proportional_size(self.area))
		if self.images:
			self.images = pg.transform.scale(self.original_images ,
			                                 (self.rect.w * self.sprite_grid[0] , self.rect.h * self.sprite_grid[1]))


	def draw(self , screen_to_draw):
		if self.images:  # draw the image, if any
			new_surf = pg.Surface((self.rect.size)).convert_alpha()
			new_surf.fill([0 , 0 , 0 , 0])
			new_surf.blit(self.images , (0 , 0) , self.create_rect_to_draw())
			screen_to_draw.blit(new_surf, self.rect)
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
			self.image_index[0] = int((self.counter * 10 / (2 * FPS)) % (self.sprite_grid[0]))

		if self.duration < 0 or self.duration is None:

			self.kill()

	def do_effect(self):
		pass

	def kill(self):
		super().kill()

	def update_duration(self):
		self.duration -= 1
		print(self.duration)

	def check_colision_effect(self , group_effects):
		interactions = set()
		for effect in group_effects:
			if effect != self:
				if self.rect.colliderect(effect.rect):
					new_interaction = {self , effect}
					interactions.add(new_interaction)
		return interactions