# vl53l0x_sensor

import board
import busio
import adafruit_vl53l0x
from config import config as c

class VL53L0X:
    def __init__(self):
        try:
            # Initialize I2C bus and sensor
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_vl53l0x.VL53L0X(i2c, address=c.TOF_SENSOR["I2C_ADDRESS"])
            # Optionally configure the sensor
            if c.TOF_SENSOR["DISTANCE_MODE"] == 1:
                self.sensor.measurement_timing_budget = 20000  # Short range mode
            elif c.TOF_SENSOR["DISTANCE_MODE"] == 2:
                self.sensor.measurement_timing_budget = 50000  # Medium range mode
            elif c.TOF_SENSOR["DISTANCE_MODE"] == 3:
                self.sensor.measurement_timing_budget = 200000  # Long range mode
            else:
                print(f"Warning: Invalid distance mode '{c.TOF_SENSOR['DISTANCE_MODE']}' in config.py. Using default (medium range).")
                self.sensor.measurement_timing_budget = 50000  # Default to medium range mode
            print("VL53L0X ToF sensor initialized.")
        except Exception as e:
            print(f"Error initializing VL53L0X sensor: {e}")
            self.sensor = None

    def get_distance(self):
        """
        Reads the distance from the ToF sensor.

        Returns:
            The measured distance in centimeters, or None if an error occurred.
        """
        if self.sensor:
            try:
                distance = self.sensor.range / 10.0  # Convert mm to cm
                if distance > 0:
                    return distance
                else:
                    print("VL53L0X reading out of range.")
                    return None
            except Exception as e:
                print(f"Error reading ToF sensor: {e}")
                return None
        else:
            print("VL53L0X sensor not initialized.")
            return None

def initialize_tof_sensor():
    """Initializes and returns a ToF sensor object."""
    tof_sensor = VL53L0X()
    return tof_sensor