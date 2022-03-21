"""
this will work with the maps, it will create a map, give the proportions,
give the size, save the items for the player to discover.
"""


from variables_and_definitions import *
from effects import Effect

class Maps(pg.sprite.Sprite):
	"""
	This map is not a grid (v2.0)
	it draws itself.
	update the effects and interactions
	gets the virtual size in meters
	"""
	def __init__(self , idx_map , rect , item_dict = None):
		"""
		this class will be a way to interact with the effects, and locate teh player in the screen,
		also give bounds so that the player is always on screen.
		:param idx_map: int for the MAPS_IMAGES_DICT in variables and definitions.
		:param rect: pg.Rect to be drawn.
		:param item_dict: a dictionary of the items in this map.
		"""
		super().__init__()
		if item_dict is None:
			item_dict = {}
		map_image_path , self.virtual_size , self.name = MAPS_IMAGES_DICT.get(idx_map)
		if map_image_path:
			self.image = pg.image.load(f'{IMAGES_PATH}{map_image_path}').convert_alpha()
		else:
			self.image = None
		self.rect = rect
		if self.image:
			self.image = pg.transform.scale(self.image , self.rect.size)
		self.secrets = item_dict
		self.effects = pg.sprite.Group()
		change_map_proportion(self)
		maps_group.add(self)

	def draw(self , screen_to_draw):
		"""
		Draws the image in the given screen.
		:param screen_to_draw: pg.Surface
		:return:
		"""
		if self.image:
			screen_to_draw.blit(self.image , self.rect)
		else:
			pg.draw.rect(screen_to_draw , "red" , self.rect)
		self.draw_effects(screen_to_draw)

	def draw_effects(self , screen_to_draw):
		surf_effects = pg.Surface(self.rect.size).convert_alpha()
		surf_effects.fill([0,0,0,0])
		for effect in self.effects:
			effect.draw(surf_effects)
		surf_effects.set_alpha(100)
		screen_to_draw.blit(surf_effects , (0,0))

	def update(self):
		"""
		update itself and effects in this map, checking interaction of the effects and doind the effects.
		:return:
		"""
		# mingle effects
		self.effects_update()

		# sum effects and interactions
		self.check_interations()


	def check_interations(self):
		interactions = set()
		for effect in self.effects:
			interactions.update(effect.check_colision_effect(self.effects))


	def add_effect(self , effect_idx , pos , area , duration):
		new_effect = Effect(effect_idx , pos , area , duration , [self.effects , effects_group])

	def effects_update(self):
		for effect in self.effects:
			effect.update()

	def get_virtual_size(self):
		return self.virtual_size
