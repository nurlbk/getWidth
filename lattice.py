class lattice:
    def __init__(self):
        self.grid = []
        self.grid_horizontal_size = 0  # в будущем можно будет убрать эти элементы
        self.grid_vertical_size = 0
        self.min_max_point = []
        self.cell_size = 0

    def set_grid(self, min_point, max_point, cell_size):
        self.grid_horizontal_size = int((max_point[0] - min_point[0]) / cell_size) + 3
        self.grid_vertical_size = int((max_point[1] - min_point[1]) / cell_size) + 3
        self.cell_size = cell_size
        self.min_max_point = [min_point, max_point]

        for _ in range(0, self.grid_horizontal_size):
            self.grid.append([[] for _ in range(0, self.grid_vertical_size)])

    def get_grid(self, grid_points):
        return self.grid[grid_points[0]][grid_points[1]]

    def set_grid_horizontal_size(self, grid_horizontal_size):
        self.grid_horizontal_size = grid_horizontal_size

    def get_grid_horizontal_size(self):
        return self.grid_horizontal_size

    def set_grid_vertical_size(self, grid_vertical_size):
        self.grid_vertical_size = grid_vertical_size

    def get_grid_vertical_size(self):
        return self.grid_vertical_size

    def get_min_point(self):
        return self.min_max_point[0]

    def get_max_point(self):
        return self.min_max_point[1]

    def set_cell_size(self, cell_size):
        self.cell_size = cell_size

    def get_cell_size(self):
        return self.cell_size

