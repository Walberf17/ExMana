""" a timer for me to use in the kichen"""

import pygame as pg
import sys
from datetime import timedelta , datetime

delta = timedelta(seconds = 15)
initial = datetime.now()
to_remove = []

timers = set ()
back = "gray"

pg.init()
screen = pg.display.set_mode((2,3))

class Timer:
	"""
	this class works with the duration counter
	this inits
	update
	draw
	calc the remaining duration
	"""
	
	def __init__(self , timer , command):
		"""
		get initial duration and what it does when the duration is right
		"""
		self.initial_time = datetime.now()
		self.size_timer = timer
		self.command = command
		self.end_time = self.initial_time + self.size_timer
		self.running = True
		timers.add(self)
		

	def update(self):
		"""
		check if the duration is come
		"""
		if self.running:
			if datetime.now() >= self.end_time:
				self.do_thing()
		
	def get_remaining_time(self):
		if self.running:
			return self.end_time - datetime.now()	
		
	def do_thing(self):
		"""
		do whatever it is made to do
		and remove itself from list of timers
		"""
		eval(self.command)
		to_remove.append(self)
		self.running = False
	
	
def its_time():
	global back
	back = "blue"
	#print(datetime.now() , " huahuahua")
	
	

def main():
	global to_remove
	while 1:
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				pg.quit()
				sys.exit()
			if ev.type == pg.MOUSEBUTTONDOWN:
				for timer in timers:
					print((timer.get_remaining_time().seconds))
		screen.fill(back)
		a.update()
		for obj in to_remove:
			timers.discard(obj)
		to_remove = []
		pg.display.update()
		
		



	
a = Timer(timedelta(seconds = 3) , "its_time()")

main()