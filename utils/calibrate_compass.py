# calibrate_compass.py

import time
import board
import busio
import smbus2  # Import the smbus2 library
import config as c

# I2C bus configuration
i2c_bus = 1  # Use I2C bus 1 (adjust if needed)
bus = smbus2.SMBus(i2c_bus)

# MPU9250 I2C address
mpu_addr = c.MPU9250_I2C_ADDRESS

# Register addresses for magnetometer
mag_asa_x = 0x10  # Magnetometer X-axis sensitivity adjustment
mag_asa_y = 0x11  # Magnetometer Y-axis sensitivity adjustment
mag_asa_z = 0x12  # Magnetometer Z-axis sensitivity adjustment

def read_magnetometer_data():
    """Reads magnetometer data from the MPU9250."""
    # AK8963 magnetometer I2C address
    ak8963_addr = 0x0C

    # Read status and make sure data is ready
    status = bus.read_byte_data(ak8963_addr, 0x02)
    if not (status & 0x01):
        # print("Magnetometer data not ready.")
        return None  # Data not ready

    # Read magnetometer data (6 bytes for x, y, z)
    data = bus.read_i2c_block_data(ak8963_addr, 0x03, 7)  # Reading 7 bytes to include status

    # Check for data overflow
    if status & 0x08:
        print("Magnetometer data overflow.")
        return None  # Data overflow

    # Extract raw magnetometer data (x, y, z)
    mag_x_raw = twos_complement(data[1], data[0])
    mag_y_raw = twos_complement(data[3], data[2])
    mag_z_raw = twos_complement(data[5], data[4])

    # Read the sensitivity adjustment values from the magnetometer's fuse ROM
    asa_x = bus.read_byte_data(ak8963_addr, mag_asa_x)
    asa_y = bus.read_byte_data(ak8963_addr, mag_asa_y)
    asa_z = bus.read_byte_data(ak8963_addr, mag_asa_z)

    # Apply sensitivity adjustments (as described in the MPU9250 datasheet)
    mag_x = mag_x_raw * ((asa_x - 128) * 0.5 / 128 + 1)
    mag_y = mag_y_raw * ((asa_y - 128) * 0.5 / 128 + 1)
    mag_z = mag_z_raw * ((asa_z - 128) * 0.5 / 128 + 1)

    return {'x': mag_x, 'y': mag_y, 'z': mag_z}

def twos_complement(high_byte, low_byte):
    """Converts two's complement data to signed integer."""
    value = (high_byte << 8) + low_byte
    if value >= 0x8000:
        return -((0xFFFF - value) + 1)
    return value

def calibrate_magnetometer():
    """
    Calibrates the magnetometer by finding the minimum and maximum values for each axis.
    """
    print("Starting magnetometer calibration...")
    print("Please rotate the robot in all directions (like making a figure-8) for 30 seconds.")

    start_time = time.time()
    min_values = [float('inf')] * 3
    max_values = [float('-inf')] * 3

    while time.time() - start_time < 30:
        mag_data = read_magnetometer_data()

        if mag_data is not None:
            mag_x = mag_data['x']
            mag_y = mag_data['y']
            mag_z = mag_data['z']

            min_values[0] = min(min_values[0], mag_x)
            min_values[1] = min(min_values[1], mag_y)
            min_values[2] = min(min_values[2], mag_z)

            max_values[0] = max(max_values[0], mag_x)
            max_values[1] = max(max_values[1], mag_y)
            max_values[2] = max(max_values[2], mag_z)

            print(f"Current Min: {min_values}, Current Max: {max_values}")
            time.sleep(0.1)
        else:
            print("Failed to read magnetometer data.")
            time.sleep(0.5) # Wait a bit longer before retrying

    print("Calibration complete.")

    # Calculate offsets (average of min and max)
    offsets = [(min_val + max_val) / 2 for min_val, max_val in zip(min_values, max_values)]

    print("Calibration Results:")
    print(f"  Minimum values: {min_values}")
    print(f"  Maximum values: {max_values}")
    print(f"  Offsets: {offsets}")
    print("  Paste these offsets into your config.py file.")

if __name__ == "__main__":
    calibrate_magnetometer()