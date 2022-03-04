"""
Buttons class
This class makes buttons_group,
do the click down and up stuffs,
change color when roovered
stuff in general
"""
from variables_and_definitions import *


class Button(pg.sprite.Sprite):
	def __init__(self , relative_size: tuple|list , action: str = "None" , image: str = None , txt = None , action_on_click = False , colors = ['orange' , 'orange4' , 'orange2']):
		"""
		It creates a rect in the screen, and does a action when interacted. If calls update, when hoovered it slightly change the color.
		:param relative_size: a list or tuple with float numbers from 0 to 1.0
		:param action: str with the action to do.
		:param image: str with path to the image
		:param txt: str with what should it show
		:param action_on_click: bool
		:param colors: list of pg.color
		"""
		super().__init__()
		self.rect = pg.Rect(calc_relative_size(relative_size))
		self.action = action
		self.image = image
		self.clicked = False
		self.action_on_click = action_on_click
		self.color = 0
		self.colors = colors
		self.txt = txt
		buttons_group.add(self)

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
		eval(self.action)
				
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
