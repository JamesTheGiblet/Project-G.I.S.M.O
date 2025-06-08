# servo_control.py

import time
from adafruit_pca9685 import PCA9685
import config as c

"""
servo_control.py

This module provides functions to control the servos connected to the PCA9685 PWM driver. 
It allows for individual servo control, simultaneous control of both arm servos, 
and predefined movements like raising/lowering arms and moving the head.

Globals:
    current_angle_lhs (int): Stores the current angle of the left-hand side servo.
    current_angle_rhs (int): Stores the current angle of the right-hand side servo.
    current_angle_head (int): Stores the current angle of the head servo.

Functions:
    initialize_servos(pca): Initializes the servos to their default positions.
    set_servo_angle(pca, channel, angle): Sets the angle of a specified servo.
    waggle_arms(pca, num_waggles, waggle_delay): Makes the robot's arms waggle.
    move_servo_to_angle(pca, servo_channel, angle): Moves a servo to a specific angle.
    move_both_arms(pca, angle): Moves both arm servos to the same angle.
    raise_arms(pca): Raises both lifting arms to the up position.
    lower_arms(pca): Lowers both lifting arms to the down position.
    move_head_up(pca): Moves the head servo to the up position.
    move_head_down(pca): Moves the head servo to the down position.
    move_head_center(pca): Moves the head servo to the center position.
    test_servos(pca): Tests the servos by moving them through different positions.
"""

# Global variables to track servo angles (initialize to defaults)
current_angle_lhs = c.SERVO_ANGLES["LHS_UP"]
current_angle_rhs = c.SERVO_ANGLES["RHS_UP"]
current_angle_head = c.SERVO_ANGLES["HEAD_CENTER"]

def initialize_servos(pca):
    """Initializes the servos to their default positions."""
    global current_angle_lhs, current_angle_rhs, current_angle_head

    # Set initial positions
    set_servo_angle(pca, c.SERVO_PINS["LHS"], c.SERVO_ANGLES["LHS_UP"])
    set_servo_angle(pca, c.SERVO_PINS["RHS"], c.SERVO_ANGLES["RHS_UP"])
    set_servo_angle(pca, c.SERVO_PINS["HEAD"], c.SERVO_ANGLES["HEAD_CENTER"])

    current_angle_lhs = c.SERVO_ANGLES["LHS_UP"]
    current_angle_rhs = c.SERVO_ANGLES["RHS_UP"]
    current_angle_head = c.SERVO_ANGLES["HEAD_CENTER"]

def set_servo_angle(pca, channel, angle):
    """Sets the angle of the servo motor and updates current_angle.

    Args:
        pca: The PCA9685 object.
        channel: The PCA9685 channel connected to the servo.
        angle: The desired angle in degrees (0-180).
    """
    global current_angle_lhs, current_angle_rhs, current_angle_head

    if not 0 <= angle <= 180:
        print("Servo angle out of range (0-180)")
        return

    if channel == c.SERVO_PINS["LHS"]:
        min_pulse = c.SERVO_PULSE_WIDTHS["LHS"]["MIN"]
        max_pulse = c.SERVO_PULSE_WIDTHS["LHS"]["MAX"]
    elif channel == c.SERVO_PINS["RHS"]:
        min_pulse = c.SERVO_PULSE_WIDTHS["RHS"]["MIN"]
        max_pulse = c.SERVO_PULSE_WIDTHS["RHS"]["MAX"]
    elif channel == c.SERVO_PINS["HEAD"]:
        min_pulse = c.SERVO_PULSE_WIDTHS["HEAD"]["MIN"]
        max_pulse = c.SERVO_PULSE_WIDTHS["HEAD"]["MAX"]
    else:
        print("Invalid servo channel")
        return

    pulse = int(angle / 180 * (max_pulse - min_pulse) + min_pulse)

    # Ensure the pulse width is within the valid range
    pulse = max(min(pulse, max_pulse), min_pulse)
    pca.channels[channel].duty_cycle = int(pulse / 20000 * 65535)  # Convert pulse width to duty cycle

    # Update the current angle variable
    if channel == c.SERVO_PINS["LHS"]:
        current_angle_lhs = angle
    elif channel == c.SERVO_PINS["RHS"]:
        current_angle_rhs = angle
    elif channel == c.SERVO_PINS["HEAD"]:
        current_angle_head = angle

    print(f"Servo channel {channel} angle set to {angle} degrees (pulse width: {pulse})")

def waggle_arms(pca, num_waggles=2, waggle_delay=0.1):
    """Waggles the robot's arms back and forth.

    Args:
        pca: The PCA9685 object.
        num_waggles: The number of times to waggle the arms.
        waggle_delay: The delay (in seconds) between each waggle movement.
    """
    global current_angle_lhs, current_angle_rhs  # Access global angle variables

    print("Waggling arms...")

    for _ in range(num_waggles):
        # Move arms to opposite positions
        set_servo_angle(pca, c.SERVO_PINS["LHS"], c.SERVO_ANGLES["LHS_UP"])
        set_servo_angle(pca, c.SERVO_PINS["RHS"], c.SERVO_ANGLES["RHS_DOWN"])
        time.sleep(waggle_delay)

        # Move arms to opposite positions
        set_servo_angle(pca, c.SERVO_PINS["LHS"], c.SERVO_ANGLES["LHS_DOWN"])
        set_servo_angle(pca, c.SERVO_PINS["RHS"], c.SERVO_ANGLES["RHS_UP"])
        time.sleep(waggle_delay)

    # Return arms to their initial positions after waggling
    set_servo_angle(pca, c.SERVO_PINS["LHS"], current_angle_lhs)
    set_servo_angle(pca, c.SERVO_PINS["RHS"], current_angle_rhs)

def move_servo_to_angle(pca, servo_channel, angle):
    """Moves the specified servo to the given angle."""
    set_servo_angle(pca, servo_channel, angle)

def move_both_arms(pca, angle):
    """Moves both LHS and RHS servos to the specified angle."""
    set_servo_angle(pca, c.SERVO_PINS["LHS"], angle)
    set_servo_angle(pca, c.SERVO_PINS["RHS"], angle)

def raise_arms(pca):
    """Raises both lifting arms."""
    move_both_arms(pca, c.SERVO_ANGLES["LHS_UP"])

def lower_arms(pca):
    """Lowers both lifting arms."""
    move_both_arms(pca, c.SERVO_ANGLES["LHS_DOWN"])

def move_head_up(pca):
    """Moves the head servo to the up position."""
    set_servo_angle(pca, c.SERVO_PINS["HEAD"], c.SERVO_ANGLES["HEAD_UP"])

def move_head_down(pca):
    """Moves the head servo to the down position."""
    set_servo_angle(pca, c.SERVO_PINS["HEAD"], c.SERVO_ANGLES["HEAD_DOWN"])

def move_head_center(pca):
    """Moves the head servo to the center position."""
    set_servo_angle(pca, c.SERVO_PINS["HEAD"], c.SERVO_ANGLES["HEAD_CENTER"])

def test_servos(pca):
    """Tests the servos by moving them through different positions."""
    print("Testing Servos...")

    # Move both arms together
    print("Moving both arms up...")
    raise_arms(pca)
    time.sleep(1)
    print("Moving both arms down...")
    lower_arms(pca)
    time.sleep(1)

    # Test head movement
    print("Moving head up...")
    move_head_up(pca)
    time.sleep(1)
    print("Moving head to center...")
    move_head_center(pca)
    time.sleep(1)
    print("Moving head down...")
    move_head_down(pca)
    time.sleep(1)
    print("Moving head to center...")
    move_head_center(pca)
    time.sleep(1)

    print("Servo Test Complete")