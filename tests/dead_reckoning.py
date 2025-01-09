import time
import board
import busio
from mpu6050 import mpu6050
import config as c
from math import radians, degrees, sin, cos

class DeadReckoning:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = mpu6050(c.MPU9250_I2C_ADDRESS) # Initialize with I2C address
        self.position = (0, 0)  # (x, y) coordinates in meters
        self.heading = 0.0  # Initial heading (degrees)
        self.last_time = time.monotonic()

    def update(self):
        """Updates the position and heading based on accelerometer and gyroscope readings."""
        dt = time.monotonic() - self.last_time
        self.last_time = time.monotonic()

        # Read accelerometer and gyroscope data
        accel_data = self.mpu.get_accel_data()
        gyro_data = self.mpu.get_gyro_data()

        accel_x = accel_data['x']  # m/s^2
        accel_y = accel_data['y']  # m/s^2
        gyro_z = gyro_data['z']  # °/s

        # Update heading (simple integration for now)
        self.heading += gyro_z * dt

        # Calculate displacement (simple integration for now)
        # Use average velocity for a slightly better estimate
        avg_vel_x = accel_x * dt  # m/s
        avg_vel_y = accel_y * dt  # m/s

        # Convert heading to radians for calculations
        heading_rad = radians(self.heading)

        # Calculate displacement based on heading
        dx = avg_vel_x * cos(heading_rad) * dt
        dy = avg_vel_y * sin(heading_rad) * dt

        # Update position
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def get_position(self):
        """Returns the current estimated position (x, y)."""
        return self.position

    def get_heading(self):
        """Returns the current estimated heading (degrees)."""
        return self.heading