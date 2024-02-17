
import numpy as np

class GameArea:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=int)

    def add_object(self, obj, position):
        # Add an object to the game grid
        x, y = position
        for i in range(obj.size[0]):
            for j in range(obj.size[1]):
                self.grid[y + j][x + i] = obj.symbol


