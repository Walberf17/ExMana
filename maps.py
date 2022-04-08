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
		interactions = []
		for effect in self.effects:
			new_interaction = effect.check_collision_effect(self.effects)
			if new_interaction:
				for interaction in new_interaction:
					if interaction and interaction not in interactions:
						interactions.append(interaction)
		for effect1 , effect2 , result in EFFECT_INTERACTIONS:
			test_effect = {effect1 , effect2}
			for interaction in interactions:
				kinds = set()
				duration = None
				for effect in interaction:
					kinds.add(effect.get_kind())
					if duration:
						duration = min(effect.get_duration() , duration)
					else:
						duration = effect.get_duration()
				if test_effect == kinds:
					self.add_effect(result , duration)

	def effect_interact(self , effects):
		durations = []
		pos_x = 0
		pos_y = 0
		size = []
		for effect in effects:
			durations.append(effect.get_duration())
			x , y = effect.get_pos()
			pos_x += x
			pos_y += y
			effect.set_duration(None)
		return min(durations) , (int(pos_x/2) , int(pos_y/2))




	def add_effect(self , idx_effect: int = 1 , pos = None , area = None , duration: int = 0, action = None,):
		"""
		Creates a effect somewhere in the
		:param idx_effect: int with the idx in the images for effects dictionary
		:param pos: position of the effect
		:param area: area, in meters of the effect
		:param duration: int duration of the effect, 0 if instantaneous
		:param action: if given, a different action will be taken, meaning, only the image from the dict will be used
		:return: Effect Object
		"""
		Effect(idx_effect , pos , area , duration , action , groups = [self.effects , effects_group])

	def effects_update(self):
		for effect in self.effects:
			effect.update()

	def get_virtual_size(self):
		return self.virtual_size
