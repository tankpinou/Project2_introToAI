# -*- coding: utf-8 -*-
"""Project2(bot1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qtqCTExLvi7pqVJXGSYEIwsVzlFazWwk
"""

import random

class Bot1:
    def __init__(self, grid,open_cells):
        self.grid = grid
        self.leak_detected = False
        self.leak_location = None
        self.total_actions = 0
        self.bot_location = self.initialize_bot()
        #self.may_contain_leak = self.initialize_possible_leaks()
        self.may_contain_leak = open_cells

    def initialize_bot(self):
        # Place the Bot
        row = random.randint(0, len(self.grid)-1)
        col = random.randint(0, len(self.grid[0])-1)
        self.grid[row][col] = 'bot'
        return (row, col)

    def initialize_possible_leaks(self):
        # Initialize MAY_CONTAIN_LEAK = all open cells in the ship that aren't where the bot is
        self.may_contain_leak = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 'open' and (row,col) != self.bot_location:
                    self.may_contain_leak.append((row, col))

    def get_detection_square(self, location):
        # Get the detection square around the given location
        row, col = location
        detection_square = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                r = row + i
                c = col + j
                if self.is_valid_cell(r, c):
                    detection_square.append((r, c))
        return detection_square

    def is_valid_cell(self, row, col):
        # Check if the given cell is a valid cell in the grid
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])

    def get_closest_possible_leak(self):
        # Get the closest possible leak location to the current bot location
        closest_distance = float('inf')
        closest_location = None
        for location in self.may_contain_leak:
            distance = self.manhattan_distance(self.bot_location, location)
            if distance < closest_distance:
                closest_distance = distance
                closest_location = location
        return closest_location

    def manhattan_distance(self, location1, location2):
        # Calculate the Manhattan distance between two locations
        row1, col1 = location1
        row2, col2 = location2
        return abs(row1 - row2) + abs(col1 - col2)

    def run(self):
        while not self.leak_detected:
            self.sense()
            self.update_possible_leaks()
            self.move()

    def sense(self):
        # Run detection square on bot location
        detection_square = self.get_detection_square(self.bot_location)
        for row, col in detection_square:
            if self.grid[row][col] == 'leak':
                self.leak_detected = True
                self.leak_location = (row, col)
                break
        self.total_actions += 1

    def update_possible_leaks(self):
        # Update possible leak locations based on sensing
        if self.leak_detected:
            self.may_contain_leak = list(set(self.may_contain_leak) & set(self.get_detection_square(self.bot_location)))
        else:
            self.may_contain_leak = list(set(self.may_contain_leak) - set(self.get_detection_square(self.bot_location)))

    def move(self):
        # Move to closest possible leak location
        closest = self.get_closest_possible_leak()
        self.total_actions += self.manhattan_distance(self.bot_location, closest)
        self.bot_location = closest

def generate_ship_layout(D):
    grid = [['blocked'] * D for _ in range(D)]
    open_cells = set()

    # Choose a random cell for the leak
    button_row = random.randint(1, D-2)
    button_col = random.randint(1, D-2)
    grid[button_row][button_col] = 'leak'
    open_cells.add((button_row, button_col))

    while True:
        blocked_cells = set()
        for row in range(1, D-1):
            for col in range(1, D-1):
                if grid[row][col] == 'blocked':
                    neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
                    open_neighbors = 0
                    for neighbor_row, neighbor_col in neighbors:
                        if grid[neighbor_row][neighbor_col] == 'open':
                            open_neighbors += 1
                    if open_neighbors == 1:
                        blocked_cells.add((row, col))

        if not blocked_cells:
            break

        random_cell = random.choice(list(blocked_cells))
        grid[random_cell[0]][random_cell[1]] = 'open'
        open_cells.add(random_cell)

    # Identify dead ends and open random closed neighbors for half of them
    dead_ends = set()
    for row in range(1, D-1):
        for col in range(1, D-1):
            if grid[row][col] == 'open':
                neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
                open_neighbors = 0
                for neighbor_row, neighbor_col in neighbors:
                    if grid[neighbor_row][neighbor_col] == 'open':
                        open_neighbors += 1
                if open_neighbors == 1:
                    dead_ends.add((row, col))

    num_cells_to_open = len(dead_ends) // 2
    for _ in range(num_cells_to_open):
        dead_end = random.choice(list(dead_ends))
        neighbors = [(dead_end[0]-1, dead_end[1]), (dead_end[0]+1, dead_end[1]),
                     (dead_end[0], dead_end[1]-1), (dead_end[0], dead_end[1]+1)]
        closed_neighbors = []
        for neighbor_row, neighbor_col in neighbors:
            if grid[neighbor_row][neighbor_col] == 'blocked':
                closed_neighbors.append((neighbor_row, neighbor_col))
        if len(closed_neighbors)!=0:
          random_neighbor = random.choice(closed_neighbors)
          grid[random_neighbor[0]][random_neighbor[1]] = 'open'
          open_cells.add(random_neighbor)

    return grid, open_cells

# Generate ship layout
D = 50  # Size of the ship grid
grid, open_cells = generate_ship_layout(D)

# Randomly select a starting position for bot1
#start_row, start_col = random.choice(list(open_cells))
#grid[start_row][start_col] = 'bot'

# Create bot1 instance
bot1 = Bot1(grid,open_cells)

# Run the simulation
bot1.run()

# Leak found
print("Leak location:", bot1.leak_location)
print("Total actions:", bot1.total_actions)

