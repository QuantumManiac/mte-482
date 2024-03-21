from enum import Enum
import math
from queue import PriorityQueue
from typing import TypedDict


class Point(TypedDict):
    x: int
    y: int

file_found = './path.txt'
create_path = './path_created.txt'

item_name = []
item_location = []

product_name = ""
product_location = []
location_of_cart = []

class state(Enum):
    EMPTY = 0
    BARRIER = 1
    CLOSED = 2
    OPENED = 3
    START = 4
    END = 5

class Spot:
    def __init__(self, tile_x, tile_y, width, height, total_rows, total_cols):
        self.row = tile_x
        self.col = tile_y
        self.x = tile_x * width
        self.y = tile_y * height
        self.state = state.EMPTY
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.state == state.BARRIER

    def is_start(self):
        return self.state == state.START

    def is_end(self):
        return self.state == state.END
    
    def is_open(self):
        return self.state == state.OPENED
    
    def is_closed(self):
        return self.state == state.CLOSED

    def make_start(self):
        self.state = state.START
        
    def make_barrier(self):
        self.state = state.BARRIER

    def make_end(self):
        self.state = state.END

    def make_open(self):
        self.state = state.OPENED
    
    def make_closed(self):
        self.state = state.CLOSED

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
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
        dir = "left"
        turned = True
    elif (v1x*v2y - v1y*v2x) < 0:
        dir = "right"
        turned = True

    directions = f"{curr_spot.row},{curr_spot.col},{dir}|"
    # curr_str = f"Next: ({prev_spot.row}, {prev_spot.col}), Curr: ({curr_spot.row}, {curr_spot.col}), Prev: ({next_spot.row}, {next_spot.col}), ({dir})"
    # print(curr_str)
    return curr_spot, directions, dir, turned

def des_loc(last_point, second_last, third_last):
    v1x = second_last.row - third_last.row
    v1y = second_last.col - third_last.col
    v2x = last_point.row - second_last.row
    v2y = last_point.col - second_last.col
    direction = ""
    if (v1x*v2y - v1y*v2x) > 0:
        direction = "left"
    elif (v1x*v2y - v1y*v2x) < 0:
        direction = "right"

    return direction

def print_path(came_from, next_points, current):
    to_aisle = ""
    # count = 0
    # # chamath pls ignore how bad this is i just need to access the last three points
    # # this is also coded assuming the user isnt trying to navigate to a point right next to them ... or this wont work 
    # last_point = current
    # second_last = current
    # third_last = current
    # max = len(next_points) - 1
    # for i in came_from:
    #     if count == 0:
    #         last_point = came_from[i]
    #         second_last = next_points[i]
    #         count += 1
    #     if count == 1:
    #         third_last = next_points[i]
    #         count += 1
    
    # to_aisle = des_loc(last_point, second_last, third_last)

    path_str = ""
    path = []
    turn_dir = []
    temp = ""
    prev_spot = current
    count = 0
    dir = []
    with open(create_path, 'w') as file:
        while current in came_from:
            if count >= 1:
                prev_spot = current
            
            current = came_from[current]
            try:
                next_spot = next_points[current]
            except:
                print("end")
            if count == 0:
                    arrived = f"{current.row},{current.col},arrive_{to_aisle}"
                    arrival = [(current.row), (current.col)]
                    path.append(arrival)
                    path_str = arrived
                    turn_dir.append("Arrived!")

            # current.make_path()
            if count >= 1:
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
        path_str = f"{current.x},{current.y},start|" + path_str
        file.write(path_str)
        return path_str, path, turn_dir
    
# Set the border of the grid to be barriers
def make_border(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    for i in range(num_rows):
        for j in range(num_cols):
            if i == 0 or j == 0 or i == num_rows - 1 or j == num_cols - 1:
                spot = grid[i][j]
                spot.make_barrier()

# Make a rectangle of barriers
def make_rectangle_barrier(grid, x, y, width, height):
    for i in range(x, x + width):
        for j in range(y, y + height):
            spot = grid[i][j]
            spot.make_barrier()

def make_set_barrier(grid):
    length_x = 17
    length_y = 2
    div_rows = [2, 5, 8, 11, 14, 17]
    div_cols = [2, 20]
    # LAST_ROW = 77

    # Make the border of the grid barriers
    make_border(grid)

    # Make the rectangle barriers
    for div_row in div_rows:
        for div_col in div_cols:
            make_rectangle_barrier(grid, div_col, div_row, length_x, length_y)
					
def make_grid(length_x, length_y, tile_length_x, tile_length_y):
    grid = [[Spot(x, y, tile_length_x, tile_length_y, length_x, length_y) for y in range(length_y)] for x in range(length_x)]
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
    directions = []

    open_set_hash = {start} #help to see what is in the open set
    while not open_set.empty():
        current = open_set.get()[2] #gets node associated with min f score
        
        open_set_hash.remove(current) # remove from open set
        formatted = f"current:row {current.row}, current:col {current.col}"
        print(formatted)
        if current == end:
            print("equals")
            next_points = came_from.copy()
            # for x in came_from:
            #     formatted = f"came_from:row {x.row}, came_from:col {x.col}"
            #     print(formatted)
            next_points.popitem()
            # for x in next_points:
            #     formatted = f"next:row {x.row}, next:col {x.col}"
            #     print(formatted)
            reconstruct_path(came_from, end)
            path_str, path, directions = print_path(came_from, next_points, end)
            end.make_end()
            print("ended")
            return True, path, path_str, directions

        for neighbor in current.neighbors:
            # print("neighbours")
            temp_g_score = g_score[current] + 1
            # print(temp_g_score)

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

    return False, path, path_str, directions

# def main():
# 	grid = make_grid(39, 21, 1, 1)
# 	make_set_barrier(grid)
# 	start = grid[1][1]
# 	start.make_start()
# 	end = grid[10][6]
# 	print("go")
# 	end.make_end()
    
# 	algorithm(grid, start, end)
# 	print("done")

# main()
