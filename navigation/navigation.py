import pygame
import numpy
import math
from queue import PriorityQueue
import json

file_path = 'C:/UW/4B/MTE482/items.txt'
file_found = 'C:/UW/4B/MTE482/path.txt'
create_path = 'C:/UW/4B/MTE482/path_created.txt'

item_name = []
item_location = []

product_name = ""
product_location = []
location_of_cart = []

with open(file_path, 'r') as file:
	for line in file:
		values = line.strip().split()

		if len(values) >= 3:
			item_name.append(values[0])
			temp = [(values[1]), (values[2])]
			item_location.append(temp)
    # data = file.read()

print(item_location)
# text = data.split('\n')
# two_d_array = [t.split() for t in text]
# print(two_d_array[1][1])

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
PINK = (255, 192, 203)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE
	
	def is_item(self):
		return self.color == PINK

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def make_item(self):
		self.color = PINK

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

def receive_info(product_info, location_info):
	product_name = product_info[0]
	item_name.append(values[0])
	temp = [(values[1]), (values[2])]
	item_location.append(temp)

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def create_string(prev_spot, curr_spot, next_spot):
    dir = ""
	# everything is in reverse, so if it says left, logically it should be right
    if (next_spot.col > curr_spot.col and curr_spot.row == next_spot.row and prev_spot.row > curr_spot.row):
        dir = "right"
    elif (next_spot.col > curr_spot.col and curr_spot.row == next_spot.row and prev_spot.row < curr_spot.row): 
        dir = "left"
    elif (next_spot.col < curr_spot.col and curr_spot.row == next_spot.row and prev_spot.row > curr_spot.row):
        dir = "left"
    elif (next_spot.col < curr_spot.col and curr_spot.row == next_spot.row and prev_spot.row < curr_spot.row):
        dir = "right"
    elif (next_spot.row > curr_spot.row and curr_spot.col == next_spot.col and prev_spot.col > curr_spot.col):
        dir = "left"
    elif (next_spot.row > curr_spot.row and curr_spot.col == next_spot.col and prev_spot.col < curr_spot.col):
        dir = "right"
    elif (next_spot.row < curr_spot.row and curr_spot.col == next_spot.col and prev_spot.col > curr_spot.col):
        dir = "right"
    elif (next_spot.row < curr_spot.row and curr_spot.col == next_spot.col and prev_spot.col < curr_spot.col):
        dir = "left"

    curr_str = f"Next: ({prev_spot.row}, {prev_spot.col}), Curr: ({curr_spot.row}, {curr_spot.col}), Prev: ({next_spot.row}, {next_spot.col}), ({dir})"
    # print(curr_str)
    return curr_str

def print_path(came_from, next_points, current):
	path_str = []
	temp = ""
	prev_spot = current
	count = 0
	max = len(next_points) - 1
	with open(create_path, 'w') as file:
		while current in next_points:
			if count >= 1:
				prev_spot = current
			
			current = came_from[current]
			try:
				next_spot = next_points[current]
			except:
				print("end")

			current.make_path()
			if count >= 1 and count < max:
				temp = create_string(prev_spot, current, next_spot)
				print(temp)
				# file.write(temp)
				if current == next_spot:
					path_str.append("(Arrived)")
				else:
					path_str.insert(0, temp)
			count += 1
			# formatted = temp
		for i in range(len(path_str)):
			format_str = f"{path_str[i]} \n"
			file.write(format_str)
			
def in_path(location, path_points):
	# actual coords
	if location in path_points:
		return True
	temp_loc = location
	# next position (0,1)
	temp_loc[0][0] = location[0][0] + 1
	if location in path_points:
		return True
	# (1,1)
	temp_loc[0][0] = location[0][0] + 1
	temp_loc[0][1] = location[0][1] + 1
	if location in path_points:
		return True
	#(0,1)
	temp_loc[0][1] = location[0][1] + 1
	if location in path_points:
		return True
	#(-1,1)
	temp_loc[0][0] = location[0][0] - 1
	temp_loc[0][1] = location[0][1] + 1
	if location in path_points:
		return True
	#(-1,0)
	temp_loc[0][0] = location[0][0] - 1
	if temp_loc in path_points:
		return True
	#(-1,-1)
	temp_loc[0][0] = location[0][0] - 1
	temp_loc[0][1] = location[0][1] - 1
	if location in path_points:
		return True
	#(0,-1)
	temp_loc[0][1] = location[0][1] - 1
	if location in path_points:
		return True
	#(1,-1)
	temp_loc[0][0] = location[0][0] + 1
	temp_loc[0][1] = location[0][1] - 1
	if location in path_points:
		return True
	
	return False

def reconstruct_path(came_from, current, draw):
	with open(file_found, 'w') as file:
		while current in came_from:	
			current = came_from[current]
			current.make_path()
			draw()
			formatted = f"{current.row} {current.col}\n"
			file.write(formatted)

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue() #open set
	open_set.put((0, count, start)) # put start node in open set
	came_from = {} # to keep track of what nodes came from where
	g_score = {spot: float("inf") for row in grid for spot in row} # keeps track of the current shortest distance to get from the start node to the current node
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row} # keeps track of the predicted distance from this node to the end node
	f_score[start] = h(start.get_pos(), end.get_pos()) # initial is the heuristic from start to end

	open_set_hash = {start} #help to see what is in the open set

	while not open_set.empty():
		# this would be replaced with the cancellation on the UI
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] #gets node associated with min f score
		open_set_hash.remove(current) # remove from open set

		if current == end:
			next_points = came_from.copy()
			next_points.popitem()
			reconstruct_path(came_from, end, draw)
			print_path(came_from, next_points, end)
			end.make_end()
			return True

		for neighbor in current.neighbors: 
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]: # if g score is better than what is found in the table
				# update
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				# add to open set
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def plot_items(grid):
	for i in range(len(item_name)):
		spot = grid[int(item_location[i][0])][int(item_location[i][1])]
		spot.make_item()

def get_location():
	#getting the location
	for i in 10:
		x = 10


def make_set_barrier(grid):
	num_shelves_x = 4
	num_shelves_y = 2
	length_x = 2
	length_y = 12
	div_rows = [7, 15, 23, 31]
	div_cols = [6, 20]

	for i in range(num_shelves_x):
		for j in range(num_shelves_y):
			for k in range(length_x):
				for l in range(length_y):
					x_coord = div_rows[i]+k
					y_coord = div_cols[j]+l
					spot = grid[x_coord][y_coord]
					spot.make_barrier()

def main(win, width):
	ROWS = 40
	grid = make_grid(ROWS, width)

	start = None
	end = None
	
	make_set_barrier(grid)
	plot_items(grid)

	run = True
	while run:
		draw(win, grid, ROWS, width)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				print(row)
				print(col)
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				# elif spot != end and spot != start:
				# 	spot.make_barrier()
				# 	print(row, " ", col)

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					returned = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					if returned:
						start = end
						start.make_start()
						end = None
						make_set_barrier(grid)
						plot_items(grid)
						

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)