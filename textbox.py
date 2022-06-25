"""

"""
# from variables_and_definitions import *
from definitions import *
from variables import *
import pygame as pg
from pygame.sprite import Sprite

# Some Default Font
font_size = int(screen_rect.h / 20)
main_menu_font = pg.font.SysFont("arial" , font_size , False , False)


class TextBox(Sprite):
	""" this will work with long sentences,
	cutinh then is smaller ones , and drawing
	each on screen.
	param txt : string
	param rect : pg.Rect
	param font : pg.font.SysFont
	param font_color : pg.color
	param bg_color : pg.color
	"""

	def __init__(self , text , rect , rect_to_be, centered_x = True , centered_y = False, font = None , font_color = "white" ,bg_color = "black" , groups = None):
		"""
		It takes a string, a pg.Rect , a pg.font,
		font color and a background color.

		:param text : string
		:param centered_x: if the text should be centered in the x axis
		:param rect : pg.Rect
		:param font : pg.font.SysFont
		:param font_color : pg.color
		:param bg_color : pg.color
		"""
		if groups is None:
			groups = []
		if type(groups) not in [set , list , tuple]:
			groups = list(groups)
		super().__init__(*groups)
		if font is None:
			font = main_menu_font
		self.text = text
		self.font = font
		self.font_color = font_color
		self.bg_color = bg_color
		self.rect = pg.Rect(calc_proportional_size(expected = rect , max_area = [1,1] , max_rect = rect_to_be))
		self.centered_x = centered_x
		self.centered_y = centered_y
		if centered_x:
			self.rect.centerx = rect_to_be.centerx
		if centered_y:
			self.rect.centery = rect_to_be.centery
		self.max_size = self.rect.w*0.9
		self.line_w , self.line_h = self.font.size(str(text))
		self.lines = []
		self.get_lines()
		self.cliked = False

	def get_one_line(self , te):
		"""
		Gets a full txt and extract a number of words
		enought to fill a line.
		return : the first line and the rest of the text

		:param te : str
		"""
		words = te.split(' ')
		line = ''
		while self.font.size(line)[0] <= self.max_size +1:
			x = str(line) +' '+ words[0]
			if self.font.size(x)[0] <= self.max_size+1:
				line = str(x)
				words.pop(0)
			else:
				te = te[ len(line) : ]
				return line[1:] , te

	def get_lines(self):
		"""
		Create all the lines needed to fill the box
		"""
		t = str(self.text) # makes a copy
		lines = []
		while self.font.size(t)[0] > self.max_size+1:
			one_line , t = self.get_one_line(t)
			lines.append(one_line)
		lines.append(t)
		self.lines = lines

	def draw(self, screen_to_draw):
		"""
		Draw the text box in the given surface.
		:param screen_to_draw: pg.Surface Object
		:return: None
		"""
		new_surface = pg.Surface((self.rect.w , self.line_h*len(self.lines)))
		new_surface_rect = new_surface.get_rect()
		for counter , line in enumerate(self.lines):
			txt = self.font.render(line , True , self.font_color , self.bg_color)
			txt_rect = txt.get_rect()
			txt_rect.top = counter*self.line_h
			if self.centered_x:
				txt_rect.centerx = new_surface_rect.centerx
			new_surface.blit(txt , txt_rect)
		new_surface_rect.topleft = self.rect.topleft
		if self.centered_y:
			new_surface_rect.centery = self.rect.centery
		screen_to_draw.blit(new_surface , new_surface_rect)
