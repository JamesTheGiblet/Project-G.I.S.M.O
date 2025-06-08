# test_on_back.py

import time
import board
import busio
from mpu6050 import mpu6050
import config as c

# Initialize I2C communication
i2c = busio.I2C(board.SCL, board.SDA)
mpu = mpu6050(c.MPU9250_I2C_ADDRESS)

# Thresholds for different orientations (adjust as needed)
ON_BACK_MIN = 4.1   # m/s^2
ON_BACK_MAX = 4.5   # m/s^2
ON_FACE_MIN = 1.2   # m/s^2
ON_FACE_MAX = 1.6   # m/s^2
UPRIGHT_MIN = 9.0   # m/s^2
UPRIGHT_MAX = 10.0  # m/s^2
ON_LHS_MIN = -1.85  # m/s^2  Values for when robot is on its left side
ON_LHS_MAX = -1.65  # m/s^2
ON_RHS_MIN = 0.4    # m/s^2   Values for when robot is on its right side
ON_RHS_MAX = 0.7    # m/s^2
UPSIDE_DOWN_MIN = -10.0 # m/s^2
UPSIDE_DOWN_MAX = -9.6  # m/s^2

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

def is_robot_on_back():
    """
    Checks if the robot is on its back based on accelerometer readings.

    Returns:
        True if on its back, False otherwise.
    """
    accel_data = mpu.get_accel_data()
    accel_z = accel_data['z']
    print(f"Accelerometer Z-axis: {accel_z:.2f} m/s^2")
    return ON_BACK_MIN <= accel_z <= ON_BACK_MAX

def is_robot_on_face():
    """
    Checks if the robot is on its face (tilted forward).

    Returns:
        True if on its face, False otherwise.
    """
    accel_data = mpu.get_accel_data()
    accel_z = accel_data['z']
    print(f"Accelerometer Z-axis: {accel_z:.2f} m/s^2")
    return ON_FACE_MIN <= accel_z <= ON_FACE_MAX

def is_robot_upright():
    """
    Checks if the robot is upright (flat on the floor).

    Returns:
        True if upright, False otherwise.
    """
    accel_data = mpu.get_accel_data()
    accel_z = accel_data['z']
    print(f"Accelerometer Z-axis: {accel_z:.2f} m/s^2")
    return UPRIGHT_MIN <= accel_z <= UPRIGHT_MAX

def is_robot_on_lhs():
    """
    Checks if the robot is on its left-hand side based on accelerometer readings.

    Returns:
        True if on its left side, False otherwise.
    """
    accel_data = mpu.get_accel_data()
    accel_x = accel_data['x']
    print(f"Accelerometer X-axis: {accel_x:.2f} m/s^2")
    return ON_LHS_MIN <= accel_x <= ON_LHS_MAX

def is_robot_on_rhs():
    """
    Checks if the robot is on its right-hand side based on accelerometer readings.

    Returns:
        True if on its right side, False otherwise.
    """
    accel_data = mpu.get_accel_data()
    accel_x = accel_data['x']
    print(f"Accelerometer X-axis: {accel_x:.2f} m/s^2")
    return ON_RHS_MIN <= accel_x <= ON_RHS_MAX

def is_robot_upside_down():
    """
    Checks if the robot is upside down.

    Returns:
        True if upside down, False otherwise.
    """
    accel_data = mpu.get_accel_data()
    accel_z = accel_data['z']
    print(f"Accelerometer Z-axis: {accel_z:.2f} m/s^2")
    return UPSIDE_DOWN_MIN <= accel_z <= UPSIDE_DOWN_MAX

if __name__ == "__main__":
    # Run calibration and print results
    gyro_biases = calibrate_gyro()
    print("\nCalibration Results:")
    print(f"  Gyro Bias (X, Y, Z): ({gyro_biases['x']:.2f}, {gyro_biases['y']:.2f}, {gyro_biases['z']:.2f})")
    print("  Update your config.py with these bias values if they seem reasonable.\n")

    input("Press Enter to start on-back/on-face/upright detection test...")

    try:
        print("Starting orientation detection test...")
        while True:
            if is_robot_on_back():
                print("Robot is on its BACK!")
            elif is_robot_on_face():
                print("Robot is on its FACE!")
            elif is_robot_upright():
                print("Robot is UPRIGHT.")
            elif is_robot_on_lhs():
                print("Robot is on its LEFT-HAND SIDE.")
            elif is_robot_on_rhs():
                print("Robot is on its RIGHT-HAND SIDE.")
            elif is_robot_upside_down():
                print("Robot is UPSIDE DOWN!")
            else:
                print("Robot orientation is UNKNOWN.")
            time.sleep(0.5)  # Adjust timing as needed

    except KeyboardInterrupt:
        print("Exiting test.")