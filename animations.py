"""
this class works with the animations

"""
from variables import *
from definitions import *
from pygame.sprite import Sprite
import random


class Animations:
	def __init__(self , images_idx = 1 , area = (1 , 1) , dict_with_image = CHARACTER_IMAGES_DICT , rect_to_be = screen_rect):
		"""
		:param images_idx: int
		:param groups: groups to add
		:param dict_to_image: dictionary from where the image will come
		"""
		if images_idx is None:
			images_idx = 1
		self.images_idx = images_idx
		if not dict_with_image:
			dict_with_image = {}
		this_dict_image = dict_with_image.get(images_idx)
		if this_dict_image is None:
			this_dict_image = dict_with_image.get(1)
		this_path = dict_with_image.get('path')
		if rect_to_be is None:
			rect_to_be = screen_rect
		self.rect_to_be = rect_to_be
		self.default_image_path = IMAGES_PATH+this_path
		images , self.sprite_size = this_dict_image
		self.original_images = pg.image.load(f'{self.default_image_path+images}').convert_alpha()
		self.images = self.original_images.copy()

		# calcs the number of images on the image
		self.sprite_grid = [self.original_images.get_size()[0] / self.sprite_size[0] ,
		                    self.original_images.get_size()[1] / self.sprite_size[1]]
		self.image_index = [0 , 0]
		self.area = area
		self.rect = pg.Rect(self.rect_to_be.topleft , (calc_proportional_size(self.area)))
		self.image_index = [0 , 0]
		self.counter = 0
		self.change_size_proportion()

	def change_size_proportion(self):
		"""
		Change the rect and stuff proportionally to the current map.
		Change the rect and the images
		:return: None
		"""
		self.rect = pg.Rect(self.rect.center , calc_proportional_size(self.area))
		if self.images:
			self.images = pg.transform.scale(self.original_images , (self.rect.w * self.sprite_grid[0] , self.rect.h * self.sprite_grid[1]))

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

	def draw(self ,  screen_to_draw):
		"""
		draw itself on the given surface
		:param screen_to_draw: pg.Surface
		:return: None
		"""
		if self.images:  # draw the image, if any
			new_surf = pg.Surface(self.rect.size).convert_alpha()
			new_surf.fill([0 , 0 , 0 , 0])
			new_surf.blit(self.images , (0,0) , self.create_rect_to_draw())
			screen_to_draw.blit(new_surf , self.rect)
		else:  # draw a rect to debug
			pg.draw.rect(screen_to_draw , "red" , self.rect)

	def update(self , velocity = 6):
		if self.images:
			self.counter += 1
			self.image_index[0] = int((self.counter * velocity / (2 * FPS)) % (self.sprite_grid[0]))

		self.rect.clamp_ip(self.rect_to_be)

"""
	def change_images_idx(self , value):
		self.images_idx = value
		this_character_list = CHARACTER_IMAGES_DICT.get(value)
		if this_character_list is None:
			this_character_list = CHARACTER_IMAGES_DICT.get(1)
		images , self.sprite_size = this_character_list
		self.original_images = pg.image.load(IMAGES_PATH + images).convert_alpha()
		self.images = self.original_images.copy()
		self.sprite_grid = self.original_images.get_size()[0] / self.sprite_size[0] , \
		                   self.original_images.get_size()[1] / self.sprite_size[1]
		self.image_index = [0 , 0]
		self.change_size_proportion()"""

