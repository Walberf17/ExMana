"""
a class to create some boxes that when released in some other box will act as a button
"""

from variables_and_definitions import *

class SelectionBox:
	def __init__(self , rect , image , arguments , drops):
		self.rect = rect
		if image:
			self.image = pg.image.load(image).convert()

		self.arguments = arguments
		self.clicked = False
		self.drops = drops

	def draw(self , screen_to_draw):
		if self.image:
			screen_to_draw.blit(self.image , self.rect)
		else:
			pg.draw.rect(screen_to_draw , "red" , self.rect , 5)

	def click_down(self , event):
		if self.rect.collidepoint(event.pos):
			self.clicked = True
			return True

	def move(self):
		if self.clicked:
			self.rect.move_ip(pg.mouse.get_rel())

	def click_up(self , event):
		if self.clicked:
			for box in self.drops:
				if box.rect.collidepoint(self.rect.center):
					box.do_command(self.args)
					return True


class Dropbox:
	def __init__(self , rect , command = None , drop_command = None, arguments = None , image = None):
		self.command = command
		self.arguments = arguments
		self.drop_command = drop_command
		if image:
			self.image = pg.image.load(image).convert_alpha()
		else:
			self.image = None
		self.rect = rect

	def draw(self , screen_to_draw):
		if self.image:
			screen_to_draw.blit(self.image , self.rect)
		else:
			pg.draw.rect(screen_to_draw , "green" , self.rect , 10)
			
	def drop_command(self , arguments):
		if self.command:
			if self.arguments:
				eval(f'{self.command}({self.arguments} , {arguments})')
			else:
				eval(f'{self.command}({arguments})')