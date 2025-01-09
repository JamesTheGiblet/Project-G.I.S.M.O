# mapping.py

import numpy as np
import config as c
import math

class OccupancyGridMap:
    """
    Represents an occupancy grid map for the robot's environment.

    The map is stored as a 2D NumPy array (grid) where each cell holds a probability value:
      - 0.0: Definitely free
      - 1.0: Definitely occupied
      - 0.5: Unknown

    The map is updated based on dead reckoning (position, heading) and sensor readings (distance).
    """

    def __init__(self):
        """
        Initializes the OccupancyGridMap.
        """
        grid_size_x = c.MAP_SETTINGS["GRID_SIZE_X"]
        grid_size_y = c.MAP_SETTINGS["GRID_SIZE_Y"]
        self.grid = np.full((grid_size_x, grid_size_y), 0.5)  # Initialize all cells to 0.5 (unknown)
        self.cell_size = c.MAP_SETTINGS["CELL_SIZE"]  # Size of each cell in meters

    def update_map(self, position, distance, heading):
        """
        Updates the occupancy grid based on sensor readings.

        Args:
            position (tuple): The robot's current (x, y) position in meters.
            distance (float): The distance reading from the ultrasonic sensor in centimeters.
            heading (float): The robot's current heading in degrees.
        """
        if distance is None or distance > 4:
            return  # Ignore readings beyond the sensor's effective range (4 meters)

        # Convert distance from cm to meters
        distance = distance / 100

        # Convert robot's position to grid coordinates (centering the robot in the grid)
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
        """
        Generates a sequence of points along a line using Bresenham's algorithm.

        Args:
            x0 (int): The x-coordinate of the starting point.
            y0 (int): The y-coordinate of the starting point.
            x1 (int): The x-coordinate of the end point.
            y1 (int): The y-coordinate of the end point.

        Returns:
            list: A list of (x, y) tuples representing the points along the line.
        """
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
        """
        Displays the map in the console, optionally with the robot's position.

        Args:
            robot_position (tuple): The robot's current (x, y) position in meters.
        """
        print(" " + "-" * (self.grid.shape[1] * 2 + 1) + " ")

        for i in range(self.grid.shape[0] - 1, -1, -1):  # Iterate rows in reverse order
            line = "|"
            for j in range(self.grid.shape[1]):
                cell = self.grid[i, j]
                if robot_position:
                    grid_x = int(robot_position[0] / self.cell_size) + self.grid.shape[0] // 2
                    grid_y = int(robot_position[1] / self.cell_size) + self.grid.shape[1] // 2
                    if i == grid_x and j == grid_y:
                        char = "R"  # Robot's position
                    elif cell > c.MAP_SETTINGS["OBSTACLE_THRESHOLD"]:
                        char = "X"  # Obstacle
                    elif cell < (1 - c.MAP_SETTINGS["OBSTACLE_THRESHOLD"]):
                        char = " "  # Free
                    else:
                        char = "?"  # Unknown
                else:
                    if cell > c.MAP_SETTINGS["OBSTACLE_THRESHOLD"]:
                        char = "X"  # Obstacle
                    elif cell < (1 - c.MAP_SETTINGS["OBSTACLE_THRESHOLD"]):
                        char = " "  # Free
                    else:
                        char = "?"  # Unknown
                line += f" {char}"
            print(line + " |")
        print(" " + "-" * (self.grid.shape[1] * 2 + 1) + " ")