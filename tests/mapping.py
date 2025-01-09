# mapping.py

import numpy as np
import config as c
import math

class OccupancyGridMap:
    def __init__(self):
        grid_size_x = c.MAP_SETTINGS["GRID_SIZE_X"]
        grid_size_y = c.MAP_SETTINGS["GRID_SIZE_Y"]
        self.grid = np.full((grid_size_x, grid_size_y), 0.5)  # Initialize all cells to 0.5 (unknown)
        self.cell_size = c.MAP_SETTINGS["CELL_SIZE"]

    def update_map(self, position, distance, heading):
        """Updates the occupancy grid based on sensor readings."""
        if distance is None or distance > 4:
            return  # Ignore readings beyond the sensor's effective range

        # Convert robot's position to grid coordinates
        grid_x = int(position[0] / self.cell_size) + self.grid.shape[0] // 2
        grid_y = int(position[1] / self.cell_size) + self.grid.shape[1] // 2

        # Convert the obstacle's position to grid coordinates
        obstacle_x = int((position[0] + distance * math.cos(math.radians(heading))) / self.cell_size) + self.grid.shape[0] // 2
        obstacle_y = int((position[1] + distance * math.sin(math.radians(heading))) / self.cell_size) + self.grid.shape[1] // 2

        # Update the cells in the grid
        if 0 <= obstacle_x < self.grid.shape[0] and 0 <= obstacle_y < self.grid.shape[1]:
            # Increase the probability of the obstacle cell
            self.grid[obstacle_x, obstacle_y] = min(1.0, self.grid[obstacle_x, obstacle_y] + 0.2)

            # Decrease the probability of cells between the robot and the obstacle
            for x, y in self.bresenham_line(grid_x, grid_y, obstacle_x, obstacle_y):
                if 0 <= x < self.grid.shape[0] and 0 <= y < self.grid.shape[1]:
                    self.grid[x, y] = max(0.0, self.grid[x, y] - 0.1)

    def bresenham_line(self, x0, y0, x1, y1):
        """Generates a sequence of points along a line using Bresenham's algorithm."""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        return points

    def display_map(self, robot_position=None):
        """Displays the map in the console, optionally with the robot's position."""
        print(" " + "-" * (self.grid.shape[1] * 2 + 1) + " ")

        for i in range(self.grid.shape[0] - 1, -1, -1):  # Iterate rows in reverse order
            line = "|"
            for j in range(self.grid.shape[1]):
                cell = self.grid[i, j]
                if robot_position and i == int(robot_position[0] / self.cell_size) + self.grid.shape[0] // 2 and j == int(robot_position[1] / self.cell_size) + self.grid.shape[1] // 2:
                    char = "R"  # Robot's position
                elif cell > c.MAP_SETTINGS["OBSTACLE_THRESHOLD"]:
                    char = "X"  # Obstacle
                elif cell < 1 - c.MAP_SETTINGS["OBSTACLE_THRESHOLD"]:
                    char = " "  # Free
                else:
                    char = "?"  # Unknown
                line += f" {char}"
            print(line + " |")
        print(" " + "-" * (self.grid.shape[1] * 2 + 1) + " ")