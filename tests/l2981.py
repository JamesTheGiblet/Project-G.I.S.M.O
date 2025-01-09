#L2981 motor_test

import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C bus and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60  # Set PWM frequency to 60Hz

# L298N Motor Driver Pin Mapping to PCA9685 Channels
INT1_CHANNEL = 7  # Motor A (Right) - Forward
INT2_CHANNEL = 6  # Motor A (Right) - Backward
INT3_CHANNEL = 8  # Motor B (Left) - Forward
INT4_CHANNEL = 10 # Motor B (Left) - Backward

# Set channels to always be off (this assumes active high logic for enable)
pca.channels[INT1_CHANNEL].duty_cycle = 0
pca.channels[INT2_CHANNEL].duty_cycle = 0
pca.channels[INT3_CHANNEL].duty_cycle = 0
pca.channels[INT4_CHANNEL].duty_cycle = 0

# --- Helper Functions ---

def set_motor_speed(pca, int1_channel, int2_channel, speed):
    """
    Sets the speed and direction of a motor.

    Args:
        pca: The PCA9685 object.
        int1_channel: PCA9685 channel for forward direction (e.g., INT1).
        int2_channel: PCA9685 channel for backward direction (e.g., INT2).
        speed: Speed from -1.0 (full backward) to 1.0 (full forward). 0 is stopped.
    """
    if speed > 0:
    # Forward
        pca.channels[int1_channel].duty_cycle = int(speed * 65535)  # Convert 0.0-1.0 to 0-65535
        pca.channels[int2_channel].duty_cycle = 0
    elif speed < 0:
    # Backward
        pca.channels[int1_channel].duty_cycle = 0
        pca.channels[int2_channel].duty_cycle = int(-speed * 65535)  # Convert 0.0-1.0 to 0-65535
    else:
    # Stop
        pca.channels[int1_channel].duty_cycle = 0
        pca.channels[int2_channel].duty_cycle = 0

def stop_all_motors(pca):
    """Stops both motors."""
    set_motor_speed(pca, INT1_CHANNEL, INT2_CHANNEL, 0)
    set_motor_speed(pca, INT3_CHANNEL, INT4_CHANNEL, 0)

# --- Test Sequences ---

def test_forward(duration=2, speed=0.5):
    """Moves the robot forward."""
    print("Moving Forward")
    set_motor_speed(pca, INT1_CHANNEL, INT2_CHANNEL, speed)  # Right motor forward
    set_motor_speed(pca, INT3_CHANNEL, INT4_CHANNEL, speed)  # Left motor forward
    time.sleep(duration)
    stop_all_motors(pca)

def test_backward(duration=2, speed=0.5):
    """Moves the robot backward."""
    print("Moving Backward")
    set_motor_speed(pca, INT1_CHANNEL, INT2_CHANNEL, -speed)  # Right motor backward
    set_motor_speed(pca, INT3_CHANNEL, INT4_CHANNEL, -speed)  # Left motor backward
    time.sleep(duration)
    stop_all_motors(pca)

def test_turn_left(duration=2, speed=0.5):
    """Turns the robot left (in place)."""
    print("Turning Left")
    set_motor_speed(pca, INT1_CHANNEL, INT2_CHANNEL, speed)  # Right motor forward
    set_motor_speed(pca, INT3_CHANNEL, INT4_CHANNEL, -speed)  # Left motor backward
    time.sleep(duration)
    stop_all_motors(pca)

def test_turn_right(duration=2, speed=0.5):
    """Turns the robot right (in place)."""
    print("Turning Right")
    set_motor_speed(pca, INT1_CHANNEL, INT2_CHANNEL, -speed)  # Right motor backward
    set_motor_speed(pca, INT3_CHANNEL, INT4_CHANNEL, speed)  # Left motor forward
    time.sleep(duration)
    stop_all_motors(pca)

# --- Main Program ---
if __name__ == "__main__":
    try:
    # Run the test sequence
        test_forward()
        time.sleep(1)  # Pause between movements

        test_backward()
        time.sleep(1)

        test_turn_left()
        time.sleep(1)

        test_turn_right()
        time.sleep(1)
    
        print("Test complete.")

    except KeyboardInterrupt:
        print("Stopping motors and exiting...")
        stop_all_motors(pca)

    finally:
    # Ensure motors are stopped when exiting
        stop_all_motors(pca)
        pca.deinit()