"""
default pygame template
"""

# import things
import pygame as pg , sys
from variables import *
from definitions import *



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
	def __init__(self , screen_to_draw, dicts_to_do = None , background = "light blue" , fps = 45):
		"""
		creates a scene object that has its own main loop.

		It needs a surface that will work with.

		It can take a dict of list with the objects to do things:
		to do the things, creat a dict with the keys:
			"update , move , draw ,click_down , click_up
		key_down , key_up , multi_gesture , finger_down , finger_up".

		exemple_dict = {
		'update': [], 
		'move': [], 
		'draw': [], 
		'click_down': [], 
		'click_up': [], 
		'key_down': [], 
		'key_up': [], 
		'multi_gesture': [], 
		'finger_down': [], 
		'finger_up': []},
		'finger_motion' : []
		}

		:param screen_to_draw pg.Surface
		:param dicts_to_do dict object
		:param background pg.color
		:param FPS int
		"""

		
		self.screen = screen_to_draw
		self.screen_rect = self.screen.get_rect()
		self.running = False
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
		self.to_finger_down = dicts_to_do.get("finger_down" , [])
		self.to_finger_up = dicts_to_do.get("finger_up" , [])
		self.to_finger_motion = dicts_to_do.get("finger_motion" , [])
		self.background = background
		pg.event.set_blocked([4352, 32768, 1541, 32775, 32783, 32784, 32785, 3278,768,32768, 32786,32768, 259, 32780, 260, 257, 32768, 261, 262, 32782])
		
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
		self.running = True
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
	#	t = set()
		for event in pg.event.get():
			#print(pg.event.get_blocked())
			#print(pg.event.event_name(event.type))
			#pg.event.set_blocked()
#			t.add(event.type)
			#print(event)
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
			elif e_t == pg.FINGERDOWN:
				self.finger_down_handler(event)
			elif e_t == pg.FINGERUP:
				self.finger_up_handler(event)
			elif e_t == pg.FINGERMOTION:
				self.finger_motion_handler(event)
	
	def finger_motion_handler(self , event):
		for c_list in self.to_finger_motion:
			for obj in c_list:
				if obj.finger_motion(event):
					self.obj_clicked.add(obj)
					return 
	
	
	def finger_down_handler(self , event):
		"""
		Default finger down handler.
		
		Loops the objects in self.to_finger_down.
		
		It calls the default --> obj.finger_down(event).
		
		If the obj returns True, it stops the loop.
		
		If there is no objects in self.to_finger_down,
		it saves the object in a set with the clicked
		objects in self.obj_clicked.
		
		Change if needed
		
		"""
		for c_list in self.to_finger_down:
			for obj in c_list:
				if obj.finger_down(event):
					self.obj_clicked.add(obj)
					return
					
	def finger_up_handler(self , event):
		"""
		param: pg.FINGERUP event
		Default finger up handler.
		
		Loops the objects in self.to_finger_up.
		
		It loops throught the objects in self.obj_clicked,
		then in self.to_finger_up, then if interacted with
		anything, it breaks the loop

		It calls the default --> obj.finger_up(event).
		
		
		Change if needed
		
		"""
		
		# loops from self.obj_clicked
		for obj in self.obj_clicked:
			if obj.finger_up(event):
				self.obj_clicked.clear()
				return
		
		
		if self.to_finger_up:
			# loops if objects in self.to_finger_up
			for c_list in self.to_finger_up:
				for obj in c_list:
					if obj.finger_up(event):
						return
		else:
			for c_list in self.to_finger_down:
				for obj in c_list:
					if obj.finger_up(event):
						return
					
	
		
	def click_down_handler(self , event):
		"""
		Default click down handler.
		
		Loops the objects in self.to_click_down.
		
		It calls the default --> obj.click_down(event).
		
		If the obj returns True, it stops the loop.
		
		It saves the object in a set with the clicked
		objects in self.obj_clicked.
		
		Change if needed
		
		"""
		pg.mouse.get_rel()  # for smooth movement
		for c_list in self.to_click_down:
			for obj in c_list:
				if obj.click_down(event):
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
		
		# loops from self.obj_clicked
		for obj in self.obj_clicked:
			if obj.click_up(event):
				self.obj_clicked.clear()
				return
		
		
		
		# loops if objects in self.to_click_up
		for c_list in self.to_click_up:
			for obj in c_list:
				if obj.click_up(event):
					return
				
		
		
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
				
		#txt = pg.Surface(500,500).convert_alpha()
		

	def stop(self):
		self.running = False

class PauseMenu(Scene):
	def draw_handler(self):
		"""
		Default draw handler.
		
		Loops throught self.to_draw and 
		calls --> obj.draw(self.screen)
		
		It fills the screen with the self.background color.
		Than draws the things, then updates the display.
		"""
		
		#self.screen.fill(self.background)
		for c_list in self.to_draw:
			for obj in c_list:
				obj.draw(self.screen) 
				
class EditScene(Scene):
	
	
	def click_down_handler(self , event):
		pg.mouse.get_rel()  # for smooth movement
		for c_list in self.to_click_down:
			for obj in c_list:
				if obj.click_down_edit(event):
					if not self.to_click_up:
						self.obj_clicked.add(obj)
					return
	
	def click_up_handler(self , event):
		# loops if objects in self.to_click_up
		if self.to_click_up:
			for obj in self.to_click_up:
				obj.click_up_edit(event)
				
		# loops from self.obj_clicked
		else:
			for obj in self.obj_clicked:
				obj.click_up_edit(event)
			self.obj_clicked.clear()
	
	def move_handler(self):
		"""
		Move handler.
		
		Loops throught self.to_move and self.to_click
		calls --> obj.move()		
		"""

		for c_list in self.to_move:
			for obj in c_list:
				obj.move()


		for c_list in self.to_click_down:
			for obj in c_list:
				obj.move()
		
		for c_list in self.to_finger_down:
			for obj in c_list:
				obj.move()


class CreateWayScene(Scene):
	pos = []
	def click_down_handler(self , event):
		self.pos.append(event.pos)
		print(f"{self.pos},")
	
	def draw_handler(self):
		self.screen.fill(self.background)
		for pos in self.pos:
			#print(pos)
			pg.draw.circle(self.screen , "green2" , pos , 50)


class Canvas:
	def __init__(self):
		self.points = set()
	
	def finger_down(self , event):
		pos_x = event.x*screen_rect.w
		pos_y = event.y*screen_rect.h
		self.points.add((pos_x , pos_y))
	
	def finger_up(self , event):
		pos_x = event.x*screen_rect.w
		pos_y = event.y*screen_rect.h
		pos = pg.Vector2((pos_x , pos_y))
		to_remove = set()
		for pt in self.points:
			if pos.distance_to(pt) <= 30:
				to_remove.add(pt)
		for pt in to_remove:
			self.points.discard(pt)
		return
		
	def draw(self , screen_to_draw):
		for x , y in self.points:
			pg.draw.line(screen_to_draw , "red" , (x , 0) , (x,screen_rect.h) , 6)
			pg.draw.line(screen_to_draw , "red" , (0 , y) , (screen_rect.w , y) , 6)

# run
if __name__=="__main__":
	screen = pg.display.set_mode((400,800))
	screen_rect = screen.get_rect()
	a = Canvas()
	main_menu = Scene(screen , dicts_to_do={"finger_down": [[a]] , "draw": [[a]] , "finger_up": [[a]]})
	main_menu.run()