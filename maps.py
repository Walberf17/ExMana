"""
this will work with the maps, it will create a map, give the proportions,
give the size, save the items for the player to discover.
"""
from effects_info import EFFECT_INTERACTIONS
from images_info import MAPS_IMAGES_DICT
from maps_info import *
from variables import *
from definitions import *
from effects import Effect
from items_in_game import ItemsInGame
from pygame.sprite import Sprite , Group
from animations import Animations
from moving_object import MovingObj

class Maps(Animations , MovingObj):
	"""
	This map is not a grid (v2.0)
	it draws itself.
	update the effects and interactions
	gets the virtual size in meters
	"""
	def __init__(self , idx_map , secrets_list = None , rect_to_be = screen_rect , groups = None):
		"""
		this class will be a way to interact with the effects, and locate teh player in the screen,
		also give bounds so that the player is always on screen.
		:param idx_map: int for the MAPS_IMAGES_DICT in variables and definitions.
		:param rect_to_be: pg.Rect to be drawn.
		:param item_dict: a dictionary of the items in this map.
		"""
		# MovingObj.__init__(self)
		if secrets_list is None:
			secrets_list = []
		self.map_idx = idx_map
		self.area , self.name = MAPS_INFO.get(idx_map)
		change_map_proportion(self , rect_to_be)
		Animations.__init__(self , images_idx = idx_map , area = self.area , dict_with_images = MAPS_IMAGES_DICT , rect_to_be = rect_to_be , groups = groups)
		self.secrets = Group()
		self.effects = Group()
		self.create_secrets(secrets_list = secrets_list)

	def create_secrets(self , secrets_list):
		for item_idx , pos in secrets_list:
			ItemsInGame(pos = pos , item_idx = item_idx , groups = [self.secrets , items_group])

	def draw(self , screen_to_draw):
		"""
		Draws the image in the given screen.
		:param screen_to_draw: pg.Surface
		:return:
		"""
		Animations.draw(self  , screen_to_draw)
		self.draw_secrets(screen_to_draw)
		self.draw_effects(screen_to_draw)

	def draw_secrets(self , screen_to_draw):
		for secret in self.secrets:
			secret.draw(screen_to_draw)

	def draw_effects(self , screen_to_draw):
		surf_effects = pg.Surface(screen_rect.size).convert_alpha()
		surf_effects.fill([0,0,0,0])
		for effect in self.effects:
			effect.draw(surf_effects)
		surf_effects.set_alpha(100)
		screen_to_draw.blit(surf_effects , self.rect_to_be , self.rect_to_be)
		pg.draw.rect(screen_to_draw , 'red' , self.rect_to_be , 6)

	def update(self):
		"""
		update itself and effects in this map, checking interaction of the effects and doind the effects.
		:return:
		"""
		# mingle effects
		self.effects_update()

		# sum effects and interactions
		self.check_interations()

		# upadte_image
		Animations.update(self)

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

	def add_effect(self , idx_effect: str = 'Fire' , pos = None , area = None , duration: int = 0, action = None,):
		"""
		Creates a effect somewhere in the
		:param idx_effect: int with the idx in the images for effects dictionary
		:param pos: position of the effect
		:param area: area, in meters of the effect
		:param duration: int duration of the effect, 0 if instantaneous
		:param action: if given, a different action will be taken, meaning, only the image from the dict will be used
		:return: Effect Object
		"""
		Effect(idx_effect , pos , area , duration , action , groups = [self.effects , effects_group] , rect_to_be = self.rect)

	def effects_update(self):
		for effect in self.effects:
			effect.update()

	def get_virtual_size(self):
		return self.area

	def get_map_idx(self):
		return self.map_idx

	def get_secrets(self):
		return self.secrets
