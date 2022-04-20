"""
default pygame template
"""

# import things
import pygame as pg , sys
from variables import *
from buttons import Button
from definitions import *

# create scene
pg.init()


# variables


# classes
class Scene:
	"""
	this class will help to create diferent scenes for
	the games and apps.
	It creats a default loop:
		check if it stops,
		check events
		update things
		move things
		draw things
		update the display
		
	to run call --> self.run()
	to stop call --> self.stop()
	
	to do the things, creat a dict with the keys:
		"update , move , draw ,click_down , click_up
		key_down , key_up , multi_gesture".
		
		The values have to be a list of pg.groups|set|list.
		
		If no click_up is given , it will save the first object clicked
	and will click up only that object
	"""
	def __init__(self , screen_to_draw = None , dicts_to_do = None , background = "light blue" , fps = 45):
		"""
		creates a scene object that has its own main loop.

		It needs a surface that will work with.

		It can take a dict of list with the objects to do things:
		to do the things, creat a dict with the keys:
			"update , move , draw ,click_down , click_up
		key_down , key_up , multi_gesture".

		:param screen_to_draw pg.Surface
		:param dicts_to_do dict object
		:param background pg.color
		:param FPS int
		"""

		
		self.screen = screen_to_draw
		self.running = 0
		self.FPS = fps
		self.obj_clicked = set()
		if dicts_to_do is None:
			dicts_to_do = {}
		self.to_update = dicts_to_do.get("update" , [])
		self.to_move = dicts_to_do.get("move" , [])
		self.to_draw = dicts_to_do.get("draw" , [])
		self.to_click_down = dicts_to_do.get("click_down" , [])
		self.to_click_up = dicts_to_do.get("click_up" , [])
		self.to_key_down  = dicts_to_do.get("key_down" , [])
		self.to_key_up  = dicts_to_do.get("key_up" , [])
		self.to_multi_gesture = dicts_to_do.get("multi_gesture" , [])
		self.background = background
		
	def run(self):
		"""
		default loop.
		
		for it to stop call --> self.stop()
		
		It works in this order:
			check if stops
			events
			updates
			moves
			draws
			update pg display
		"""
		self.running = 1
		clock = pg.time.Clock()
		while self.running:
			if pg.event.peek(pg.QUIT):
				self.stop()
			self.event_handler()
			self.update_handler()
			self.move_handler()
			self.draw_handler()
			pg.display.update()
			clock.tick(self.FPS)
			
	def event_handler(self):
		"""
		Default event handler.
		It calls the default handlers for given type of event.
		Default events:
			click_down_handler(event)
			click_up_handler(event)
			multi_gesture_handler(event)
			key_down_handler(event)
			key_up_handler(event)
			
		Change if needed.
		"""
		for event in pg.event.get():
			e_t = event.type  # get the type of the event
			if e_t == pg.MOUSEBUTTONDOWN:
				self.click_down_handler(event)
			elif e_t == pg.MOUSEBUTTONUP:
				self.click_up_handler(event)
			elif e_t == pg.MULTIGESTURE:
				self.multi_gesture_handler(event)
			elif e_t == pg.KEYDOWN:
				self.key_down_handler(event)
			elif e_t == pg.KEYUP:
				self.key_up_handler(event)
		
	def click_down_handler(self , event):
		"""
		Default click down handler.
		
		Loops the objects in self.to_click_down.
		
		It calls the default --> obj.click_down(event).
		
		If the obj returns True, it stops the loop.
		
		If there is no objects in self.to_click_up,
		it saves the object in a set with the clicked
		objects in self.obj_clicked.
		
		Change if needed
		
		"""
		pg.mouse.get_rel()  # for smooth movement
		for c_list in self.to_click_down:
			for obj in c_list:
				if obj.click_down(event):
					if not self.to_click_up:
						self.obj_clicked.add(obj)
					return
		
	def click_up_handler(self , event):
		"""
		param: pg.MOUSEBUTTONUP event
		Default click up handler.
		
		Loops the objects in self.to_click_up.
		
		If there is no objects in self.to_click_up,
		it loops throught the objects in self.obj_clicked.

		It calls the default --> obj.click_up(event).
		
		
		Change if needed
		
		"""
		
		# loops if objects in self.to_click_up
		if self.to_click_up:
			for obj in self.to_click_up:
				obj.click_up(event)
				
		# loops from self.obj_clicked
		else:
			for obj in self.obj_clicked:
				obj.click_up(event)
			self.obj_clicked.clear()
		
	def multi_gesture_handler(self , event):
		"""
		Default multi_gesture_handler.
		
		For touch devices 
		
		Loops throught self.to_multi_gesture and 
		calls --> obj.multi_gesture(event)
	
		"""
		for c_list in self.to_multi_gesture:
			for obj in c_list:
				obj.multi_gesture(event)
	
	def key_down_handler(self , event):
		"""
		Default press key handler.
		
		Loops throught self.to_key_down and 
		calls --> obj.key_down(event)
		
		"""
		pg.mouse.get_rel()  # for smooth movement
		for c_list in self.to_key_down:
			for obj in c_list:
				obj.key_down(event)
	
	def key_up_handler(self , event):
		"""
		Default press key handler.
		
		Loops throught self.to_key_up and 
		calls --> obj.key_up(event)
		"""
		for c_list in self.to_key_up:
			for obj in c_list:
				obj.key_up(event)
	
	def update_handler(self):
		"""
		Default press key handler.
		
		Loops throught self.to_update and 
		calls --> obj.update()
		"""
		# pg.mouse.get_rel()
		for c_list in self.to_update:
			for obj in c_list:
				obj.update()
		
	def move_handler(self):
		"""
		Default move handler.
		
		Loops throught self.to_move and 
		calls --> obj.move()		
		"""
		# pg.mouse.get_rel()
		# print(self.to_move)
		for c_list in self.to_move:
			for obj in c_list:
				obj.move()
		
	def draw_handler(self):
		"""
		Default draw handler.
		
		Loops throught self.to_draw and 
		calls --> obj.draw(self.screen)
		
		It fills the screen with the self.background color.
		Than draws the things, then updates the display.
		"""
		
		self.screen.fill(self.background)
		for c_list in self.to_draw:
			for obj in c_list:
				obj.draw(self.screen)

	def stop(self):
		self.running = 0

class EquipScene(Scene):
	def __init__(self , screen_to_draw , dicts_to_do = None , background = "light blue" , FPS = 45):
		super().__init__(screen_to_draw , dicts_to_do, background , FPS)

	def draw_handler(self):
		self.screen.fill(self.background)
		for player in players_group:
			player.draw_equip_screen(self.screen , screen_rect)

class EditScene(EquipScene):
	def key_down_handler(self , event):
		if event.key == pg.K_n:
			Button([.25 , .1 , .5 , .1] , "print('ok')" , txt = "new")

	def click_down_handler(self , event):
		pg.mouse.get_rel()  # for smooth movement
		for button in buttons_group:
			if button.click_down_edit(event):
				return
		for slc in selection_group:
			if slc.click_down(event):
				return

	def draw_handler(self):
		self.screen.fill(self.background)
		for player in players_group:
			player.draw_equip_screen(self.screen , screen_rect)
		for btn in buttons_group:
			btn.draw(screen)
		for slc in selection_group:
			slc.draw(screen)

	def click_up_handler(self , event):
		for btn in buttons_group:
			btn.click_up(event)

		for slc in selection_group:
			if slc.click_up(event):
				return





# run
if __name__=="__main__":
	screen = pg.display.set_mode((400 , 800))
	screen_rect = screen.get_rect()
	main_menu = EquipScene(screen)
	main_menu.run()