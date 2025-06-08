# gyro_test.py

import time
import board
import busio
from mpu6050 import mpu6050
import config as c

# Initialize I2C communication
i2c = busio.I2C(board.SCL, board.SDA)
mpu = mpu6050(c.MPU9250_I2C_ADDRESS)

def calibrate_gyro(num_readings=500, delay=0.01):
    """Calibrates the gyroscope by taking multiple readings and averaging to find the bias."""
    print("Calibrating gyroscope. Please keep the robot still.")
    total_gyro_x = 0
    total_gyro_y = 0
    total_gyro_z = 0
    start_time = time.time()

    for i in range(num_readings):
        gyro_data = mpu.get_gyro_data()
        total_gyro_x += gyro_data['x']
        total_gyro_y += gyro_data['y']
        total_gyro_z += gyro_data['z']
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = 5 - elapsed_time
        print(f"Calibrating... {remaining_time:.1f} seconds remaining", end='\r')
        time.sleep(delay)

    gyro_bias_x = total_gyro_x / num_readings
    gyro_bias_y = total_gyro_y / num_readings
    gyro_bias_z = total_gyro_z / num_readings

    print(f"Gyroscope calibration complete.")
    print(f"  Bias X: {gyro_bias_x:.2f}")
    print(f"  Bias Y: {gyro_bias_y:.2f}")
    print(f"  Bias Z: {gyro_bias_z:.2f}")

    # Return the calculated bias values as a dictionary
    return {
        "x": gyro_bias_x,
        "y": gyro_bias_y,
        "z": gyro_bias_z
    }

def print_gyro_data(gyro_biases):
    """Continuously prints gyroscope data with bias correction."""
    while True:
        try:
            gyro_data = mpu.get_gyro_data()
            gyro_x = gyro_data['x'] - gyro_biases['x']
            gyro_y = gyro_data['y'] - gyro_biases['y']
            gyro_z = gyro_data['z'] - gyro_biases['z']

            print(f"Gyroscope X (deg/s): {gyro_x:.2f}")  # Print each value on a new line
            print(f"Gyroscope Y (deg/s): {gyro_y:.2f}")
            print(f"Gyroscope Z (deg/s): {gyro_z:.2f}")
            print("-" * 20)  # Separator for clarity

            time.sleep(0.5)  # Adjust the printing rate as needed

        except KeyboardInterrupt:
            print("\nExiting gyro data printing.")
            break

if __name__ == "__main__":
    # Run calibration and print results
    gyro_biases = calibrate_gyro()
    print("\nCalibration Results:")
    print(f"  Gyro Bias (X, Y, Z): ({gyro_biases['x']:.2f}, {gyro_biases['y']:.2f}, {gyro_biases['z']:.2f})")
    print("  Update your config.py with these bias values if they seem reasonable.\n")

    input("Press Enter to start printing gyroscope data with bias correction...")
    print_gyro_data(gyro_biases)