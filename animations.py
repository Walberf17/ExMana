"""


this class works with the animations





"""
from pygame.sprite import Sprite
import os
from definitions import *
import pygame as pg

"""
Exemple of image dict:
"""
dict_with_images = {
	'path' : 'Images',
	1:{
		"adress": '1.png',
	}
}

class Animations(Sprite):
	"""
	This works with the several animations in the game.
	"""
	def __init__(self , image_name = None , area = (1 , 1) ,
	             dict_with_images = None , rect_to_be = None ,
	             center = None , relative_pos = None , color = "red" , groups = None,
	             absolute_pos  = None):
		"""
		:param image_name: Index in the dictionary for the image
		:param area: Area in meters of the image
		:param dict_with_images: Dictionary with the address of the image.
		:param rect_to_be: the max_rect that it will be in.
		:param center: the center of the max_rect for the image to be
		"""
		if groups is None:
			groups = []
		if type(groups) not in [list , tuple , set]:
			groups = [groups]
		Sprite.__init__(self, *groups)

		self.images_name = None
		self.default_image_path = None
		self.sprite_size = None
		self.states_names = None
		self.active_animations = None
		self.original_images = None
		self.images = None
		self.sprite_grid = None
		self.image_index = None
		self.image_counter = 0
		self.states_counter = []  # a list with the number of images in each line of the spritesheet

		self.color = color
		if rect_to_be is None:
			rect_to_be = screen_rect
		self.rect_to_be = rect_to_be

		# self.unique_states = {"death":"kill()", "physic": "attack()", "magic": "attack()"}
		self.unique_counter = 0

		# calcs the number of images on the image

		self.area = area

		if relative_pos is None:
			relative_pos = [0 , 0]
		relative_pos.extend(self.area)

		self.rect = pg.Rect(calc_proportional_size(relative_pos , max_rect = self.rect_to_be))

		if absolute_pos is not None:
			self.rect.center = absolute_pos

		if center is not None:
			self.rect.center = calc_proportional_size(center , max_rect = self.rect_to_be) + self.rect_to_be.topleft

		if image_name and dict_with_images:
			self.define_images(image_name , dict_with_images)

	def define_images(self , image_name , dict_with_images):
		this_path = dict_with_images.get('path')

		this_dict_images = dict_with_images.get(image_name)
		if this_dict_images is None:
			return
		image = this_dict_images.get("adress")
		self.default_image_path = os.path.join(IMAGES_PATH, this_path , image)
		self.sprite_size = this_dict_images.get("size")
		self.states_names = this_dict_images.get("states")
		self.active_animations = this_dict_images.get("active animations")
		if self.active_animations is None:
			self.active_animations = {}
		self.original_images = pg.image.load(f'{self.default_image_path}').convert_alpha()
		if self.sprite_size is None:
			self.sprite_size = self.original_images.get_size()
		self.images = self.original_images.copy()
		self.sprite_grid = [int(self.original_images.get_size()[0] / self.sprite_size[0]) ,
		                    int(self.original_images.get_size()[1] / self.sprite_size[1])]

		if self.states_names is None:
			self.states_names = ['idle']

		self.image_index = [0 , 0]
		self.change_size_proportion()
		self.get_sprite_grid_count()  # get the states_counter

		if len(self.states_counter) != len(self.states_names):
			raise TypeError(
				f'Tamanhos diferentes da states_counter {len(self.states_counter)} e states_names {self.states_names}.')

	def get_sprite_grid_count(self):

		for j in range(int(self.sprite_grid[1])):
			running = True
			for i in range(int(self.sprite_grid[0])):
				new_surf = pg.Surface(self.rect.size).convert_alpha()
				new_surf.fill([0 , 0 , 0 , 0])
				new_surf.blit(self.images , (0 , 0) , self.sprite_rect_creater((i,j)))
				new_mask = pg.mask.from_surface(new_surf)
				if new_mask.count() <= 5:
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
		Change the max_rect and stuff proportionally to the current map.
		Change the max_rect and the images
		:return: None
		"""
		# self.rect = pg.Rect(self.rect.topleft , calc_proportional_size(self.area , max_rect = self.rect_to_be))
		if self.images:
			self.images = pg.transform.scale(self.original_images , (self.rect.w * self.sprite_grid[0] , self.rect.h * self.sprite_grid[1]))

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

	def draw(self ,  screen_to_draw , angle = None , alpha = None):
		"""
		draw itself on the given surface
		:param screen_to_draw: pg.Surface
		:return: None
		"""
		if self.images:  # draw the image, if any
			new_surf = pg.Surface(self.rect.size).convert_alpha()
			new_surf.fill([0 , 0 , 0 , 0])
			new_surf.blit(self.images , (0,0) , self.create_rect_to_draw())
			if angle is not None:
				new_surf = pg.transform.rotate(new_surf , angle)
			if alpha is not None:
				new_surf.set_alpha(alpha)
			new_rect_rect = new_surf.get_rect()
			new_rect_rect.center = self.rect.center
			screen_to_draw.blit(new_surf , new_rect_rect)
		else:  # draw a max_rect if no image
			pg.draw.rect(screen_to_draw , self.color , self.rect)

	def update(self , velocity = 6 , always_on_rect = True):
		if self.images:
			self.image_counter += 1
			FPS_multiplier = .8 # for speed of the animation
			self.image_index[0] = int((self.image_counter * velocity / (FPS_multiplier * FPS)) % (self.states_counter[self.image_index[1]]))
			if self.states_names[self.image_index[1]] in self.get_animated_actions():

				self.unique_counter = int((self.image_counter * velocity / (FPS_multiplier * FPS))) % (self.states_counter[self.image_index[1]]+1)
				if self.unique_counter == self.states_counter[self.image_index[1]]:
					self.do_animated_action()
					self.change_state('idle')

	def do_animated_action(self):
		"""
		Do the action set in the CARDS_KINDS dict
		:return:
		"""
		action = self.active_animations.get(self.states_names[self.image_index[1]])
		if action:
			eval(f'self.{action}')

	def get_animated_actions(self):
		"""
		Get the list of the animated actions of this image.
		:return: List
		"""
		return list(self.active_animations.keys())

	def change_state(self , new_state = 'idle'):
		"""
		Change the current state of the sprite if it is in its possible states, or set it to idle
		:param new_state: string
		:return:
		"""
		self.image_index = [0 , 0]
		self.image_counter = 0
		self.unique_counter = 0
		if self.states_names:
			if new_state in self.states_names:
				self.image_index[1] = self.states_names.index(new_state)
				return True
		return False