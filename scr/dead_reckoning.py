# dead_reckoning.py
 
import time
import board
import busio
from mpu6050 import mpu6050
import config as c
from math import radians, degrees, sin, cos

class DeadReckoning:
    """
    This class provides dead reckoning functionality for the robot using the MPU6050 sensor.
    It uses accelerometer and gyroscope data to estimate the robot's position and heading over time.
    """

    def __init__(self):
        """
        Initializes the DeadReckoning class.

        Sets up the I2C communication, initializes the MPU6050 sensor,
        and sets the initial position, heading, and gyroscope bias.
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = mpu6050(c.MPU9250_I2C_ADDRESS)  # Initialize with I2C address from config.py
        self.position = (0, 0)  # (x, y) coordinates in meters
        self.heading = 0.0  # Initial heading (degrees)
        self.last_time = time.monotonic()
        self.gyro_bias = 0.0  # Gyroscope bias value in degrees per second
        self.calibrate_gyro()
        self.prev_gyro_z = 0.0  # Previous gyro z reading for trapezoidal integration (not used in RK4)
        self.prev_accel_x = 0.0  # Previous accelerometer x reading for trapezoidal integration (not used in RK4)
        self.prev_accel_y = 0.0  # Previous accelerometer y reading for trapezoidal integration (not used in RK4)

    def calibrate_gyro(self, num_readings=500, delay=0.01):
        """
        Calibrates the gyroscope by taking multiple readings and averaging to find the bias.

        Args:
            num_readings: The number of readings to take for calibration.
            delay: The time delay (in seconds) between each reading.
        """
        print("Calibrating gyroscope. Please keep the robot still.")
        total_gyro_z = 0
        start_time = time.time()
        for _ in range(num_readings):
            gyro_data = self.mpu.get_gyro_data()
            total_gyro_z += gyro_data['z']
            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = 5 - elapsed_time  # Assuming calibration should take approximately 5 seconds
            print(f"Calibrating... {remaining_time:.1f} seconds remaining", end='\r')
            time.sleep(delay)
        self.gyro_bias = total_gyro_z / num_readings
        print(f"Gyroscope calibration complete. Bias: {self.gyro_bias:.2f} deg/s")

    def update(self):
        """
        Updates the position and heading based on accelerometer and gyroscope readings using RK4.
        """
        dt = time.monotonic() - self.last_time
        self.last_time = time.monotonic()

        # Read accelerometer and gyroscope data
        accel_data = self.mpu.get_accel_data()
        gyro_data = self.mpu.get_gyro_data()

        accel_x = accel_data['x']  # m/s^2
        accel_y = accel_data['y']  # m/s^2
        gyro_z = gyro_data['z'] - self.gyro_bias  # Subtract the bias

        # --- Fourth-Order Runge-Kutta (RK4) Integration ---

        # 1. Estimate state derivatives at the current time (k1)
        k1_heading = gyro_z
        k1_pos_x = accel_x * cos(radians(self.heading))
        k1_pos_y = accel_y * sin(radians(self.heading))

        # 2. Estimate state at the midpoint using k1 (k2)
        mid_heading = self.heading + k1_heading * dt / 2
        k2_heading = gyro_z  # Assuming gyro doesn't change significantly over dt
        k2_pos_x = accel_x * cos(radians(mid_heading))
        k2_pos_y = accel_y * sin(radians(mid_heading))

        # 3. Estimate state at the midpoint using k2 (k3)
        k3_heading = gyro_z  # Assuming gyro doesn't change significantly over dt
        k3_pos_x = accel_x * cos(radians(mid_heading))
        k3_pos_y = accel_y * sin(radians(mid_heading))

        # 4. Estimate state at the end using k3 (k4)
        end_heading = self.heading + k3_heading * dt
        k4_heading = gyro_z  # Assuming gyro doesn't change significantly over dt
        k4_pos_x = accel_x * cos(radians(end_heading))
        k4_pos_y = accel_y * sin(radians(end_heading))

        # Update heading and position using a weighted average of k1, k2, k3, and k4
        self.heading += (k1_heading + 2*k2_heading + 2*k3_heading + k4_heading) * dt / 6
        dx = (k1_pos_x + 2*k2_pos_x + 2*k3_pos_x + k4_pos_x) * dt * dt / 6  # Convert acceleration to displacement
        dy = (k1_pos_y + 2*k2_pos_y + 2*k3_pos_y + k4_pos_y) * dt * dt / 6

        # Update position
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def get_position(self):
        """Returns the current estimated position (x, y)."""
        return self.position

    def get_heading(self):
        """Returns the current estimated heading (degrees)."""
        return self.heading