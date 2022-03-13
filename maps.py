"""
this will work with the maps, it will create a map, give the proportions,
give the size, save the items for the player to discover.
"""


from variables_and_definitions import *

class Maps:
	def __init__(self , idx_map = 1 , rect = screen_rect , item_dict = None):
		if item_dict is None:
			item_dict = {}
		map_image_path , self.virtual_size , self.name = MAPS_IMAGES_DICT.get(idx_map)
		if map_image_path:
			self.image = pg.image.load(f'{IMAGES_PATH}{map_image_path}').convert_alpha()
		else:
			self.image = None
		self.rect = rect
		self.image = pg.transform.scale(self.image , self.rect.size)
		self.secrets = item_dict
		self.effects = {}
		change_map_proportion(self)
		maps_group.add(self)

	def draw(self , screen_to_draw):
		if self.image:
			screen_to_draw.blit(self.image , self.rect)
		else:
			pg.draw.rect(screen_to_draw , "red" , self.rect)

	def draw_effects(self , screen_to_draw):
		for effect in self.effects:
			effect.draw(screen_to_draw)

	def update(self):
		# mingle effects
		self.effects_update()

		# sum effects and interactions
		self.check_interations()


	def check_interations(self):
		for effect1, effect2 , new_effect in effect_interations:
			if effect1 in self.effects and effect2 in self.effects:
				time1 = self.effects.get(effect1)
				time2 = self.effects.get(effect2)
				self.effects.pop(effect1)
				self.effects.pop(effect2)
				self.effects[new_effect] = min([time1 , time2])

	def effects_update(self):
		for_delete_effect = []
		for effect , time in self.effects.items():
			if time is not None:
				effect.time -= 1
			if time < 1 or time is None:
				for_delete_effect.append(effect)

		for effect in for_delete_effect:
			self.effects.pop(effect)

	def get_virtual_size(self):
		return self.virtual_size