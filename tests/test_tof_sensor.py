# test_tof_sensor.py

import time
import VL53L0X # type: ignore
import config as c

def initialize_tof_sensor():
    """Initializes and returns a ToF sensor object."""
    try:
        tof_sensor = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=c.TOF_SENSOR["I2C_ADDRESS"])
        tof_sensor.open()
        print("VL53L0X ToF sensor initialized.")
        return tof_sensor
    except Exception as e:
        print(f"Error initializing VL53L0X sensor: {e}")
        return None

def get_tof_distance(tof_sensor):
    """
    Reads the distance from the ToF sensor.

    Args:
        tof_sensor: The ToF sensor object.

    Returns:
        The measured distance in centimeters, or None if an error occurred.
    """
    if tof_sensor:
        try:
            distance_mm = tof_sensor.get_distance()
            if distance_mm > 0:  # A reading of 0 usually indicates an error or out-of-range
                return distance_mm / 10.0  # Convert mm to cm
            else:
                print("VL53L0X reading out of range.")
                return None
        except Exception as e:
            print(f"Error reading ToF sensor: {e}")
            return None
    else:
        print("VL53L0X sensor not initialized.")
        return None

if __name__ == "__main__":
    tof_sensor = initialize_tof_sensor()

    if tof_sensor:
        # Configure the sensor's distance mode
        if c.TOF_SENSOR["DISTANCE_MODE"].upper() == "SHORT":
            tof_sensor.start_ranging(1)  # Short range mode
        elif c.TOF_SENSOR["DISTANCE_MODE"].upper() == "MEDIUM":
            tof_sensor.start_ranging(2)  # Medium range mode
        elif c.TOF_SENSOR["DISTANCE_MODE"].upper() == "LONG":
            tof_sensor.start_ranging(3)  # Long range mode
        else:
            print(f"Warning: Invalid distance mode '{c.TOF_SENSOR['DISTANCE_MODE']}' in config.py. Using default (medium range).")
            tof_sensor.start_ranging(2)  # Default to medium range mode

        try:
            print("Press Ctrl+C to exit.")
            while True:
                distance = get_tof_distance(tof_sensor)
                if distance is not None:
                    print(f"Distance: {distance:.2f} cm")
                time.sleep(0.5)  # Adjust timing as needed

        except KeyboardInterrupt:
            print("Exiting ToF sensor test.")

        finally:
            tof_sensor.stop_ranging()
            tof_sensor.close()
    else:
        print("Failed to initialize VL53L0X sensor. Check connections and I2C address.")