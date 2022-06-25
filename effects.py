"""
Create and manage effects in the field.
"""
import random
from animations import Animations
from variables import *
from definitions import *
from pygame.sprite import Sprite
from moving_object import MovingObj

class Effect(Sprite , Animations , MovingObj):
	"""
	This class sets the effects
	it inits
	"""

	def __init__(self , idx_effect: str = "Fire" , pos = None , area = None , duration: int = 1 , action = None , groups: list = None , rect_to_be = screen_rect ):
		"""

		:param idx_effect: str with the name of the image
		:param pos: center of the effect's max_rect
		:param area: area, in meters of the effect
		:param duration: int with the duration of the effect
		:param action: str: the actual effect of this effect
		:param groups: list of groups for the effect to be inserted
		"""

		if pos is None:
			pos = pg.mouse.get_pos()
		if groups is None:
			groups = []
		Sprite.__init__(self , *groups)
		# MovingObj.__init__(self)
		if area is None:
			area = [1 , 1]
		self.name = idx_effect
		Animations.__init__(self , images_idx = self.name , area = area , dict_with_images = EFFECT_DICT , rect_to_be = rect_to_be , pos = pos)
		self.duration = duration
		if action is None:
			action = EFFECT_INFO.get(self.images_idx)
		self.action = action
		self.image_index = [0 , 0]
		if self.images:
			self.image_index_differ = random.randint(0 , self.sprite_grid[0])
		else:
			self.image_index_differ = 0


	def draw(self , screen_to_draw):
		Animations.draw(self , screen_to_draw)
		pg.draw.rect(screen_to_draw , 'red' , self.rect , 4)

	def create_rect_to_draw(self):
		"""
		creates a max_rect to draw the correct sprite
		:return: None
		"""
		i , j = self.image_index
		w , h = self.rect.size
		init_x = (w * i)
		init_y = (h * j)
		return pg.Rect(init_x , init_y , w , h)

	def update(self):
		Animations.update(self , always_on_rect = False)
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
