import math
from queue import PriorityQueue

file_found = 'C:/UW/4B/MTE482/path.txt'
create_path = 'C:/UW/4B/MTE482/path_created.txt'

item_name = []
item_location = []

product_name = ""
product_location = []
location_of_cart = []

ROWS = 40

print(item_location)
# text = data.split('\n')
# two_d_array = [t.split() for t in text]
# print(two_d_array[1][1])

WIDTH = 600

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.barrier = False
		self.start = False
		self.end = False
		self.open = False
		self.closed = False
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_barrier(self):
		return self.barrier

	def is_start(self):
		return self.start

	def is_end(self):
		return self.end
	
	def is_open(self):
		return self.open
	
	def is_closed(self):
		return self.closed

	def make_start(self):
		self.start = True
		
	def make_barrier(self):
		self.barrier = True

	def make_end(self):
		self.end = True

	def make_open(self):
		self.open = True
	
	def make_closed(self):
		self.closed = True

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

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def pythagorean(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def create_string(prev_spot, curr_spot, next_spot):
    v1x = curr_spot.row - prev_spot.row
    v1y = curr_spot.col - prev_spot.col
    v2x = next_spot.row - curr_spot.row
    v2y = next_spot.col - curr_spot.col
    dir = ""
    turned = False
    if (v1x*v2y - v1y*v2x) > 0:
        dir = "Left"
        turned = True
    elif (v1x*v2y - v1y*v2x) < 0:
        dir = "Right"
        turned = True

    directions = f"Straight until: ({curr_spot.row}, {curr_spot.col}), Turn: {dir} "
    # curr_str = f"Next: ({prev_spot.row}, {prev_spot.col}), Curr: ({curr_spot.row}, {curr_spot.col}), Prev: ({next_spot.row}, {next_spot.col}), ({dir})"
    # print(curr_str)
    return curr_spot, directions, dir, turned

def print_path(came_from, next_points, current):
	path_str = ""
	path = []
	turn_dir = []
	temp = ""
	prev_spot = current
	count = 0
	dir = []
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
			if count == 0:
					arrived = f"({current.row}, {current.col}) Arrived!"
					arrival = [(current.row), (current.col)]
					path.append(arrival)
					path_str = arrived
					turn_dir.append("Arrived!")

			# current.make_path()
			if count >= 1 and count < max:
				temp, temp_str, dir, turned = create_string(prev_spot, current, next_spot)
				# print(temp.row)
				# print(temp.col)
				# file.write(temp)
				if turned:
					print(turned)
					temp_arr = [(temp.row), (temp.col)]
					path_str = temp_str + path_str
					path.insert(0, temp)
					turn_dir.insert(0, dir)
			count += 1
			# formatted = temp
		# for i in range(len(path_str)):
		# 	format_str = f"{path_str} \n"
		file.write(path_str)
		return path_str, path, dir

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
					
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

def reconstruct_path(came_from, current):
	with open(file_found, 'w') as file:
		while current in came_from:	
			current = came_from[current]
			# current.make_path()
			formatted = f"{current.row} {current.col}\n"
			file.write(formatted)
			
def algorithm(grid, start, end):
	for row in grid:
		for spot in row:
			spot.update_neighbors(grid)
	count = 0
	open_set = PriorityQueue() #open set
	open_set.put((0, count, start)) # put start node in open set
	came_from = {} # to keep track of what nodes came from where
	g_score = {spot: float("inf") for row in grid for spot in row} # keeps track of the current shortest distance to get from the start node to the current node
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row} # keeps track of the predicted distance from this node to the end node
	f_score[start] = h(start.get_pos(), end.get_pos()) # initial is the heuristic from start to end
	path = []
	path_str = ""
	dir = []

	open_set_hash = {start} #help to see what is in the open set

	while not open_set.empty():

		current = open_set.get()[2] #gets node associated with min f score
		open_set_hash.remove(current) # remove from open set

		if current == end:
			print("equals")
			next_points = came_from.copy()
			next_points.popitem()
			reconstruct_path(came_from, end)
			path_str, path, dir = print_path(came_from, next_points, end)
			end.make_end()
			print("ended")
			return True, path, path_str, dir

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			print(temp_g_score)

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

		if current != start:
			current.make_closed()

	return False, path, path_str, dir

# def main():
# 	grid = make_grid(40, 600)
# 	make_set_barrier(grid)
# 	start = grid[10][12]
# 	start.make_start()
# 	end = grid[27][34]
# 	print("go")
# 	end.make_end()
	
# 	algorithm(grid, start, end)
# 	print("done")

# main()