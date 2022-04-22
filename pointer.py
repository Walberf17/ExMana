from definitions import *
import math

class Pointer:
	def __init__(self , obj , color = 'red'):
		self.pos = screen_rect.center
		self.obj = obj
		self.color = color
		pointer_group.add(self)

	def draw(self , screen):
		ang = self.calc_ang()
		# end_point = math.cos(ang)*300 , math.sin(ang)*300
		end_point = self.obj.rect.center
		pg.draw.rect(screen , self.color , self.obj.rect , 4)
		pg.draw.line(screen , self.color , self.pos , end_point , 5)

	def calc_ang(self):
		x1 , y1 = self.pos
		x2 , y2 = self.obj.rect.center
		return math.atan2(x2-x1 , y2-y1)
