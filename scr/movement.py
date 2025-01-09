# movement.py

import time
from adafruit_pca9685 import PCA9685
import config as c

class Motor:
    """
    Represents a single DC motor controlled by a motor driver connected to a PCA9685 PWM driver.

    Attributes:
        pca (PCA9685): The PCA9685 object used to control the motor.
        forward_channel (int): The PCA9685 channel connected to the forward direction pin of the motor driver.
        backward_channel (int): The PCA9685 channel connected to the backward direction pin of the motor driver.
        current_speed (float): The current speed of the motor (-1.0 to 1.0).
        name (str): A descriptive name for the motor (e.g., "Right Motor").
    """
    def __init__(self, pca, forward_channel, backward_channel, name="Unnamed Motor"):
        """
        Initializes the Motor object.

        Args:
            pca (PCA9685): The PCA9685 object used to control the motor.
            forward_channel (int): The PCA9685 channel for the forward direction.
            backward_channel (int): The PCA9685 channel for the backward direction.
            name (str, optional): A name for the motor. Defaults to "Unnamed Motor".
        """
        self.pca = pca
        self.forward_channel = forward_channel
        self.backward_channel = backward_channel
        self.current_speed = 0.0
        self.name = name

    def set_speed(self, speed, ramp_time=c.MOVEMENT_SETTINGS["RAMP_TIME"]):
        """
        Sets the motor speed with optional ramp-up/ramp-down.

        Args:
            speed (float): The desired motor speed, from -1.0 (full backward) to 1.0 (full forward).
            ramp_time (float, optional): The time (in seconds) to ramp up or down to the target speed. 
                                        Defaults to the value in config.py.
        """
        if not -1.0 <= speed <= 1.0:
            raise ValueError("Speed must be between -1.0 and 1.0")

        target_speed = int(speed * 100)  # Convert to integer percentage
        current_speed = int(self.current_speed * 100)
        step = 5 if target_speed > current_speed else -5  # Smaller step for smoother ramping

        for intermediate_speed in range(current_speed, target_speed + step, step):
            s = intermediate_speed / 100.0
            if s >= 0:
                self.pca.channels[self.forward_channel].duty_cycle = int(s * 65535)
                self.pca.channels[self.backward_channel].duty_cycle = 0
            else:
                self.pca.channels[self.forward_channel].duty_cycle = 0
                self.pca.channels[self.backward_channel].duty_cycle = int(-s * 65535)

            sleep_time = ramp_time / abs(target_speed - current_speed) * abs(step) if abs(target_speed - current_speed) > 0 else 0
            time.sleep(sleep_time)

        self.current_speed = speed

    def stop(self):
        """Stops the motor."""
        self.set_speed(0)

class Movement:
    """
    Controls the movement of the robot using two motors.

    Attributes:
        pca (PCA9685): The PCA9685 object used to control the motors.
        motor_right (Motor): The Motor object for the right motor.
        motor_left (Motor): The Motor object for the left motor.
    """
    def __init__(self, pca):
        """
        Initializes the Movement class.

        Args:
            pca (PCA9685): The PCA9685 object used to control the motors.
        """
        self.pca = pca
        self.motor_right = Motor(pca, c.MOTOR_DRIVER_PINS["RIGHT_FORWARD"], c.MOTOR_DRIVER_PINS["RIGHT_BACKWARD"], "Right Motor")
        self.motor_left = Motor(pca, c.MOTOR_DRIVER_PINS["LEFT_FORWARD"], c.MOTOR_DRIVER_PINS["LEFT_BACKWARD"], "Left Motor")

    def move_forward(self, speed=c.MOVEMENT_SETTINGS["FORWARD_SPEED"]):
        """
        Moves the robot forward indefinitely.

        Args:
            speed (float, optional): The speed at which to move forward. Defaults to the value in config.py.
        """
        print(f"Moving Forward at speed {speed}")
        self.motor_right.set_speed(speed)
        self.motor_left.set_speed(speed)

    def move_backward(self, duration=c.MOVEMENT_SETTINGS["MOVE_DURATION"], speed=c.MOVEMENT_SETTINGS["FORWARD_SPEED"]):
        """
        Moves the robot backward for a specified duration.

        Args:
            duration (float, optional): The duration of the backward movement in seconds. Defaults to the value in config.py.
            speed (float, optional): The speed at which to move backward. Defaults to the value in config.py.
        """
        print(f"Moving Backward at speed {speed} for {duration} seconds")
        self.motor_right.set_speed(-speed)
        self.motor_left.set_speed(-speed)
        time.sleep(duration)
        self.stop_all_motors()

    def turn_left_in_place(self, duration=c.MOVEMENT_SETTINGS["TURN_DURATION"], speed=c.MOVEMENT_SETTINGS["TURN_SPEED"]):
        """
        Turns the robot left in place for a specified duration.

        Args:
            duration (float, optional): The duration of the turn in seconds. Defaults to the value in config.py.
            speed (float, optional): The speed at which to turn. Defaults to the value in config.py.
        """
        print(f"Turning Left in Place at speed {speed} for {duration} seconds")
        self.motor_right.set_speed(speed)
        self.motor_left.set_speed(-speed)
        time.sleep(duration)
        self.stop_all_motors()

    def turn_right_in_place(self, duration=c.MOVEMENT_SETTINGS["TURN_DURATION"], speed=c.MOVEMENT_SETTINGS["TURN_SPEED"]):
        """
        Turns the robot right in place for a specified duration.

        Args:
            duration (float, optional): The duration of the turn in seconds. Defaults to the value in config.py.
            speed (float, optional): The speed at which to turn. Defaults to the value in config.py.
        """
        print(f"Turning Right in Place at speed {speed} for {duration} seconds")
        self.motor_right.set_speed(-speed)
        self.motor_left.set_speed(speed)
        time.sleep(duration)
        self.stop_all_motors()

    def stop_all_motors(self):
        """Stops both motors."""
        print("Stopping all motors")
        self.motor_right.stop()
        self.motor_left.stop()

    def are_motors_commanded_to_move(self):
        """
        Checks if either motor is currently commanded to move (speed is not zero).

        Returns:
            bool: True if either motor is commanded to move, False otherwise.
        """
        return self.motor_right.current_speed != 0 or self.motor_left.current_speed != 0