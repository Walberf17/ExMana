"""
this class works with the animations

"""
from variables import *
from definitions import *
from pygame.sprite import Sprite
import random


class Animations:
	"""
	This works with the several animations in the game.
	"""
	def __init__(self , images_idx = 1 , area = (1 , 1) ,
	             dict_with_image = CHARACTER_IMAGES_DICT , rect_to_be = screen_rect ,
	             pos = None):
		"""

		:param images_idx: Index in the dictionary for the image
		:param area: Area in meters of the image
		:param dict_with_image: Dictionary with the address of the image.
		:param rect_to_be: the rect that it will be in.
		:param pos: the center of the rect for the image to be
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
		images = this_dict_image.get("adress")
		self.sprite_size = this_dict_image.get("size")
		self.states_names = this_dict_image.get("states")
		self.original_images = pg.image.load(f'{self.default_image_path+images}').convert_alpha()
		if self.sprite_size is None:
			self.sprite_size = self.original_images.get_size()
		if self.states_names is None:
			self.states_names = ['idle']
		self.unique_states = {"death":"kill()" , "attack": "attack()" , "melee attack": "melee_attack()", "magical attack": "magical_attack()"}
		# self.unique_actions = ['kill()' , 'attack()' , 'melee_attack()' , 'magical_attack()']
		self.unique_counter = 0
		self.images = self.original_images.copy()

		# calcs the number of images on the image
		self.sprite_grid = [int(self.original_images.get_size()[0] / self.sprite_size[0]) ,
		                    int(self.original_images.get_size()[1] / self.sprite_size[1])]
		self.image_index = [0 , 0]
		self.area = area
		self.rect = pg.Rect(self.rect_to_be.topleft , (calc_proportional_size(self.area)))
		if pos:
			self.rect.center = pos
		else:
			self.rect.center = self.rect_to_be.center
		self.counter = 0
		self.states_counter = []
		self.change_size_proportion()
		self.get_sprite_grid_count()


	def get_sprite_grid_count(self):
		for j in range(int(self.sprite_grid[1])):
			running = True
			for i in range(int(self.sprite_grid[0])):
				new_surf = pg.Surface(self.rect.size).convert_alpha()
				new_surf.fill([0 , 0 , 0 , 0])
				new_surf.blit(self.images , (0 , 0) , self.sprite_rect_creater((i,j)))
				new_mask = pg.mask.from_surface(new_surf)
				if new_mask.count() == 0:
					self.states_counter.append(i)
					running = False
					break
			if running:
				self.states_counter.append(int(self.sprite_grid[0]))

	def sprite_rect_creater(self , idx):
		i , j = idx
		w , h = self.rect.size
		init_x = (w * i)
		init_y = (h * j)
		return pg.Rect(init_x , init_y , w , h)

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
			if self.states_counter[self.image_index[1]] != 0:
				self.image_index[0] = int((self.counter * velocity / (2 * FPS)) % (self.states_counter[self.image_index[1]]))
				if self.states_names[self.image_index[1]] in self.unique_states:
					self.unique_counter = int((self.counter * velocity / (2 * FPS))) % (self.states_counter[self.image_index[1]]+1)
					if self.unique_counter == self.states_counter[self.image_index[1]]:
						self.unique_counter = 0
						self.do_animated_action()
			else:
				self.image_index[0] = 0
		self.rect.clamp_ip(self.rect_to_be)

	def do_animated_action(self):
		eval(f'self.{self.unique_states.get(self.states_names[self.image_index[1]])}')

	def change_state(self , new_state):
		if new_state in self.states_names:
			self.image_index[1] = self.states_names.index(new_state)
		else:
			self.image_index[1] = 0
		self.image_index[0] = 0

"""
	def change_images_idx(self , value):
		self.images_idx[1] = value

"""

