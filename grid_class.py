from variables_and_definitions import *


class Grid:
	def __init__(self , size , rect , color):
		"""
		this class works with a part of the screen_to_draw
		:param size: number or rows and columns of the grid
		:param rect: a pygame Rect object
		:param color: A color to draw the lines
		"""
		self.rows , self.columns = size
		self.rect = rect
		self.cell_w = self.rect.w / self.columns
		self.cell_h = self.rect.h / self.rows
		self.cell_size = [self.cell_w , self.cell_h]
		self.selected_map = []  # selected cells
		self.selected = False  # if it is clicked
		self.selecting = False  # boolean to check if the clicked cells will go in or out the map_rect
		self.color = color

	def draw_grid(self , screen_to_draw):
		"""
		draw the grid in the screen_to_draw
		:param screen_to_draw: pg.Surface
		:return: None
		"""
		for column in range(self.columns):
			for row in range(self.rows):
				pg.draw.rect(screen_to_draw , self.color , self.create_rect([row , column]) , 1)

	def create_rect(self , idx):
		"""
		given a index inside the grid, it returns the x , y position and width and height of a cell
		:param idx: a tuple or list
		:return: pos_x , pos_y , size_x , size_y
		"""
		i , j = idx
		init_x = self.rect.left + (self.cell_w * j)
		init_y = self.rect.top + (self.cell_h * i)
		return [init_x , init_y , self.cell_w , self.cell_h]

	def clicked(self , event):
		"""
		check if the click is
		:param event: Union of pg.MOUSEBUTTONDOWN and pg.FINGERDOWN
		:return: Boolean
		"""
		match event.type:
			case pg.MOUSEBUTTONDOWN:
				return self.rect.collidepoint(event.pos)
			case pg.FINGERDOWN:
				relative_size = event.x , event.y
				return self.rect.collidepoint(calc_relative_size(relative_size))

	def get_index(self , pos):
		"""
		return the position on the grid of a given position
		:param pos: a x,y tuple or list
		:return: [row , column]
		"""
		x , y = pos
		row = (-self.rect.top + y) // self.cell_h
		column = (-self.rect.left + x) // self.cell_w
		return [row , column]

	def create_map(self , idx):
		"""
		when clicked, saves the idx to a internal map,
		or removes it from given map, if not selecting
		:param idx: a i , j tuple or list
		:return: None
		"""
		if self.selecting:
			self.select_index(idx)
		else:
			self.deselect_index(idx)

	def select_index(self , idx):
		"""
		Saves the index to a internal map
		:param idx: a i , j tuple or list
		:return: None
		"""
		i , j = idx
		if i < self.rows and j < self.columns:
			if idx not in self.selected_map:
				self.selected_map.append(idx)

	def deselect_index(self , idx):
		"""
		Removes a index from the map
		:param idx: a i , j tuple or list
		:return:
		"""
		if idx in self.selected_map:
			self.selected_map.remove(idx)

	def get_possibles(self , idx):
		"""
		For Internal Use, get all possibles neighbours
		:param idx: a i , j tuple or list
		:return:
		"""
		i , j = idx
		possible_i = [i - 1 , i , i + 1]
		possible_j = [j - 1 , j , j + 1]
		if i == 0:
			possible_i = [i , i + 1]
		elif i == self.rows - 1:
			possible_i = [i - 1 , i]
		if j == 0:
			possible_j = [j , j + 1]
		elif j == self.columns - 1:
			possible_j = [j - 1 , j]

		return [possible_i , possible_j]

	def get_24_neighborhood(self , idx):
		"""
		Return a list if all cells with a max distance of 2 from the given cell index
		:param idx: a i , j tuple or list
		:return: List with indexes
		"""
		i , j = idx
		i , j = int(i) , int(j)
		possible_i = list(x for x in range(i - 2 , i + 3) if 0 <= x <= self.rows-1)
		possible_j = list(x for x in range(j - 2 , j + 3) if 0 <= x <= self.columns-1)
		neighbors = []
		for i in possible_i:
			for j in possible_j:
				if not [i , j] in neighbors:
					neighbors.append([i , j])
		return neighbors

	def get_8_neighborhood(self , idx):
		"""
		Return a list of indexes with the neighbors from vertical, horizontal and diagonal
		:param idx: a i , j tuple or list
		:return: List with indexes
		"""
		neighbors = []
		possible_i , possible_j = self.get_possibles(idx)
		for i in possible_i:
			for j in possible_j:
				if not [i , j] in neighbors:
					neighbors.append([i , j])
		return neighbors

	def get_4_neighborhood(self , idx):
		"""
		Return a list of indexes with the neighbors from vertical and horizontal.
		:param idx: a i , j tuple or list
		:return: List with indexes
		"""
		neighbors = []
		i , j = idx
		possible_i , possible_j = self.get_possibles(idx)
		for p_i in possible_i:
			neighbors.append([p_i , j])
		for p_j in possible_j:
			if not [i , p_j] in neighbors:
				neighbors.append([i , p_j])
		return neighbors

	def get_2_neighborhood(self , idx):
		"""
		Return a list of indexes with the neighbors from vertical and horizontal.
		:param idx: a i , j tuple or list
		:return: List with indexes
		"""
		neighbors = []
		i , j = idx
		possible_i , possible_j = self.get_possibles(idx)
		for p_i in possible_i:
			neighbors.append([p_i , j])
		return neighbors
