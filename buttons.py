"""
Buttons class
This class makes buttons_group,
do the click down and up stuffs,
change color when roovered
stuff in general
"""
from variables_and_definitions import *


class Button(pg.sprite.Sprite):
	def __init__(self , relative_size: tuple|list , action = None , image: str = None , txt = None , action_on_click = False , colors = None , groups= None):
		"""
		It creates a rect in the screen, and does a action when interacted. If calls update, when hoovered it slightly change the color.
		:param relative_size: a list or tuple with float numbers from 0 to 1.0
		:param action: str with the action to do.
		:param image: str with path to the image
		:param txt: str with what should it show
		:param action_on_click: bool
		:param colors: list of pg.color
		"""
		if groups is None:
			groups = []
		super().__init__(*groups)
		if colors is None:
			colors = ['orange' , 'orange4' , 'orange2']
		self.rect = pg.Rect(calc_relative_size(relative_size))
		self.action = action
		self.image = image
		self.clicked = False
		self.action_on_click = action_on_click
		self.color = 0
		self.colors = colors
		self.txt = txt

	def draw(self , screen_to_draw):
		"""
		draw itself on the surface given
		:param screen_to_draw: pg.Surface
		:return: None
		"""

		if self.image:
			pass

		else:
			pg.draw.rect(screen_to_draw , self.colors[self.color] , self.rect)

		if self.txt:
			button_text = main_menu_font.render(str(self.txt) , True , "black")
			text_rect = button_text.get_rect()
			text_rect.center = self.rect.center
			screen.blit(button_text , text_rect)

	def click_down_edit(self , event , button_pressed = None):
		"""
		create and put buttons_group in place, then print them
		:param event: pg.Event
		:return: boo
		"""
		if self.rect.collidepoint(event.pos):
			if button_pressed:
				ev_btn = button_pressed
			else:
				ev_btn = event.button
			if ev_btn == 1:
				self.clicked = True
				return True

			elif ev_btn == 4:
				self.rect.inflate_ip(10 , 0)

			elif ev_btn == 5:
				self.rect.inflate_ip(-10 , 0)

			elif ev_btn == 7:
				self.rect.inflate_ip(0 , 10)

			elif ev_btn == 6:
				self.rect.inflate_ip(0 , -10)

			elif ev_btn == 3:
				x , y , w , h = self.rect
				x = x / screen_rect.w
				y = y / screen_rect.h
				w = w / screen_rect.w
				h = h / screen_rect.h
				print(f'{x} , {y} , {w} , {h}' , f'"{self.txt}"')
			return True

	def click_down(self , event):
		"""
		Check if it is clicked, and it set to do action on click, do the action
		:param event: pg.MOUSEBUTTONDOWN
		:return: bool
		"""
		if self.rect.collidepoint(event.pos): # cheeck click
			self.clicked = True
			self.color = 1
			if self.action_on_click: # check if do the action now
				self.do_action()
		return self.clicked

	def move(self):
		"""
		move itself in clicked
		:return:
		"""
		if self.clicked:
			self.rect.move_ip(pg.mouse.get_rel())

	def click_up(self , event):
		"""
		Set itself as not clicked, and it set to do a action, do the action if the mouse it in the rect
		:param event: pg.MOUSEBUTTONUP event
		:return:
		"""
		if self.clicked:
			self.clicked = False
			self.color = 0
			if not self.action_on_click:
				if self.rect.collidepoint(event.pos):
					self.do_action()

	def do_action(self):
		"""
		Do whatever the action set to do.
		:return: None
		"""
		if self.action:
			self.action()

				
	def update(self):
		"""
		Just change its color when hoovered or clicked
		:return:
		"""
		mouse_pos = pg.mouse.get_pos()
		if mouse_pos:
			if self.rect.collidepoint(mouse_pos):
				if self.clicked:
					self.color = 1
				else:
					self.color = 2
			else:
				self.color = 0

		# if self.clicked:
		# 	self.rect.move_ip(pg.mouse.get_rel())

class SelectionBox(pg.sprite.Sprite):
	def __init__(self , rect , image: str = None , arguments: str = None , drops = None):
		super().__init__()
		self.rect = pg.Rect(calc_relative_size(rect))
		self.image = None
		if image:
			self.image = pg.image.load(image).convert()

		self.arguments = arguments
		self.clicked = False
		if drops:
			self.drops = drops
		else:
			self.drops = []
		self.second_rect = None
		selection_group.add(self)

	def draw(self , screen_to_draw):
		if self.image:
			screen_to_draw.blit(self.image , self.rect)
		else:
			pg.draw.rect(screen_to_draw , "red" , self.rect , 5)

		if self.clicked:
			pg.draw.rect(screen_to_draw , "blue" , self.second_rect , 7)

	def click_down(self , event):
		if self.rect.collidepoint(event.pos):
			self.clicked = True
			self.second_rect = self.rect.copy()
			return True

	def move(self):
		if self.clicked:
			mouse_move = pg.mouse.get_rel()
			self.second_rect.move_ip(mouse_move)

	def click_up(self , event):
		if self.clicked:
			self.clicked = False
			for box in self.drops:
				if self.second_rect.colliderect(box.rect):
					box.do_drop_action(self.arguments)
					return True
				self.second_rect = None
				return True

class DropBox(Button):

	def __init__(self , relative_size: tuple|list , drop_action: str = None , arguments: str = None , action: str = None , image: str = None , txt = None , action_on_click = False , colors = ['orange' , 'orange4' , 'orange2']):
		"""
		It creates a rect in the screen, and does a action when interacted. If calls update, when hoovered it slightly change the color.
		:param relative_size: a list or tuple with float numbers from 0 to 1.0
		:param action: str with the action to do.
		:param image: str with path to the image
		:param txt: str with what should it show
		:param action_on_click: bool
		:param colors: list of pg.color
		"""
		super().__init__( relative_size , action, image , txt, action_on_click , colors)
		self.drop_action = drop_action
		self.arguments = arguments

	def do_drop_action(self , arguments):
		if self.drop_action:
			if self.arguments:
				eval(f'{self.drop_action}({self.arguments} , {arguments})')
			else:
				eval(f'{self.drop_action}({arguments})')