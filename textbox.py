"""

"""
from variables_and_definitions import *


class TextBox(pg.sprite.Sprite):
	""" this will work with long sentences, 
	cutinh then is smaller ones , and drawing 
	each on screen.
	param txt : string
	param rect : pg.Rect
	param font : pg.font.SysFont
	param font_color : pg.color
	param bg_color : pg.color
	"""

	def __init__(self , txt , rect , font , font_color = "white" ,bg_color = "black" ):
		"""
		It takes a string, a pg.Rect , a pg.font, 
		font color and a background color.
		
		:param txt : string
		:param rect : pg.Rect
		:param font : pg.font.SysFont
		:param font_color : pg.color
		:param bg_color : pg.color
		"""
		super().__init__()
		self.txt = txt
		self.font = font
		self.font_color = font_color
		self.bg_color = bg_color
		self.rect = rect
		self.max_size = rect.w*0.9
		self.line_h = self.font.size(str(txt))[1]
		self.lines = self.get_lines()
		self.cliked = False
		text_boxes_group.add(self)
	
	
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
		t = str(self.txt) # makes a copy
		lines = []
		while self.font.size(t)[0] > self.max_size+1:
			one_line , t = self.get_one_line(t)
			lines.append(one_line)
		lines.append(t)
		return lines
		
	def draw(self, screen_to_draw):
		"""
		Draw the text box in the given surface.
		:param screen_to_draw: pg.Surface Object
		:return: None
		"""
		for counter , line in enumerate(self.lines):
			txt = self.font.render(line , True , self.font_color , self.bg_color)
			x , y = self.rect.topleft
			screen_to_draw.blit(txt , (x , (y + self.line_h*counter)))