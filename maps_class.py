from variables_and_definitions import *
from grid_class import Grid


class MapGrid(Grid):
	def __init__(self , name , size , rect , color):
		super().__init__(size , rect , color)
		self.map_effects = {}  # a dict of dicts for effects in a cell
		self.secret_items = {}
		self.name = name
		try:
			self.original_image = pg.image.load(f'{IMAGES_PATH}Maps/{self.name}.png').convert()
			self.image = pg.transform.scale(self.original_image , [self.rect.w , self.rect.h])
		except FileNotFoundError:
			self.original_image = None
		maps_group.add(self)
		"""
		{
		[1,1]: {"cold" : 2 , "dark": 3}
		}
		"""

	def update(self):
		self.effect_objects()
		self.map_effect_counter()

	def update_map_effects(self):
		"""
		this def work between turns and go down by 1 the counter of the effect in the cells

		remove effects with counter less then 1
		remove cells with no effects on it

		:return: Nothing
		"""
		to_remove_cell = []
		for cell in self.map_effects:
			to_remove_effect = []

			for effect in self.map_effects[cell]:
				if self.map_effects[cell][effect] == 0:
					to_remove_effect.append(effect)

			for effect in to_remove_effect:
				self.map_effects[cell].pop(effect)

			if not self.map_effects[cell]:
				to_remove_cell.append(cell)

		for cell in to_remove_cell:
			self.map_effects.pop(cell)

	def map_effect_counter(self):
		for cell in self.map_effects:
			for effect in self.map_effects[cell]:
				duration = self.map_effects[cell][effect] - 1
				self.map_effects[cell][effect] = duration
		self.update_map_effects()

	def draw(self , screen_to_draw):
		"""
		draw the map_rect in the screen_to_draw
		:param screen_to_draw: pg.Surface object where it will be drawn
		:return:
		"""
		# draws a grid on the screen_to_draw
		# super().draw(screen_to_draw)

		# draw the effects

		if self.original_image:
			self.draw_background(screen_to_draw)
		else:
			super().draw_grid(screen_to_draw)
		for cell in self.map_effects:
			for effect in self.map_effects[cell]:
				color = MAP_EFFECTS[effect].get("color" , "black")  # for now it gets the color
				x , y , w , h = self.create_rect(cell)              # get the x and y position and width and height
				new_surf = pg.Surface((w , h))
				new_surf.set_alpha(100)
				pg.draw.rect(new_surf , color , [0 , 0 , w , h])
				screen_to_draw.blit(new_surf , [x , y])

	def draw_background(self , screen_to_draw):

		screen_to_draw.blit(self.image , self.rect)

	def set_map_effects(self , cell , effect: str , duration: int):
		"""
		set a new effect to the cell,
		if it has the same effect, increase the duration for 1

		:param cell: cell for adding the effects
		:param effect: what is the effect
		:param duration: how many turns
		:return: Nothing
		"""
		cell = tuple(cell)
		if cell in self.map_effects:
			if effect in self.map_effects[cell]:
				duration = self.map_effects[cell][effect] + 2

		else:
			self.map_effects[cell] = {}

		# set the new effect
		self.map_effects[cell][effect] = duration

		# check for interactions
		self.check_interactions()
		self.update_map_effects()

	def check_interactions(self):
		for effect1 , effect2 , new_effect in effect_interations:
			for cell in self.map_effects:
				if effect1 in self.map_effects[cell] and effect2 in self.map_effects[cell]:
					if new_effect:
						duration = min(self.map_effects[cell][effect1] , self.map_effects[cell][effect2])
						self.map_effects[cell][new_effect] = duration
						self.map_effects[cell][effect1] = 0
						self.map_effects[cell][effect2] = 0
					else:
						self.map_effects[cell][effect1] = 0
						self.map_effects[cell][effect2] = 0

		self.update_map_effects()

	def effect_objects(self):
		for cell in self.map_effects:
			for player in players_group:
				self.do_effect(cell , player)
			for monster in monsters_group:
				self.do_effect(cell , monster)

	def do_effect(self , cell , obj):
		if pg.Rect(self.create_rect(cell)).colliderect(obj.rect):
			for effect in self.map_effects[cell]:
				effect_list = MAP_EFFECTS[effect]["effect"]
				obj.effect(effect_list , self)

	def get_cell_pos(self , idx):
		cell = pg.Rect(self.create_rect(idx))
		return cell.center

	def set_secret(self , secret , pos):

		if not tuple(pos) in self.secret_items:
			self.secret_items[tuple(pos)] = []
		self.secret_items[tuple(pos)].append(secret)
