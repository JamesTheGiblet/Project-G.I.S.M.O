# movement.py

import time
from adafruit_pca9685 import PCA9685
import config as c

class Motor:
    def __init__(self, pca, forward_channel, backward_channel, name="Unnamed Motor"):
        self.pca = pca
        self.forward_channel = forward_channel
        self.backward_channel = backward_channel
        self.current_speed = 0.0
        self.name = name

    def set_speed(self, speed, ramp_time=c.MOVEMENT_SETTINGS["RAMP_TIME"]):
        """Sets the motor speed with optional ramp-up/ramp-down."""
        if not -1.0 <= speed <= 1.0:
            raise ValueError("Speed must be between -1.0 and 1.0")

        target_speed = int(speed * 100)  # Convert to integer percentage
        current_speed = int(self.current_speed * 100)
        step = 5 if target_speed > current_speed else -5

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
    def __init__(self, pca):
        self.pca = pca
        self.motor_right = Motor(pca, c.MOTOR_DRIVER_PINS["RIGHT_FORWARD"], c.MOTOR_DRIVER_PINS["RIGHT_BACKWARD"], "Right Motor")
        self.motor_left = Motor(pca, c.MOTOR_DRIVER_PINS["LEFT_FORWARD"], c.MOTOR_DRIVER_PINS["LEFT_BACKWARD"], "Left Motor")

    def move_forward(self, duration=c.MOVEMENT_SETTINGS["MOVE_DURATION"], speed=c.MOVEMENT_SETTINGS["FORWARD_SPEED"]):
        """Moves the robot forward."""
        print(f"Moving Forward at speed {speed} for {duration} seconds")
        self.motor_right.set_speed(speed)
        self.motor_left.set_speed(speed)
        time.sleep(duration)
        self.stop_all_motors()

    def move_backward(self, duration=c.MOVEMENT_SETTINGS["MOVE_DURATION"], speed=c.MOVEMENT_SETTINGS["FORWARD_SPEED"]):
        """Moves the robot backward."""
        print(f"Moving Backward at speed {speed} for {duration} seconds")
        self.motor_right.set_speed(-speed)
        self.motor_left.set_speed(-speed)
        time.sleep(duration)
        self.stop_all_motors()

    def turn_left_in_place(self, duration=c.MOVEMENT_SETTINGS["TURN_DURATION"], speed=c.MOVEMENT_SETTINGS["TURN_SPEED"]):
        """Turns the robot left in place."""
        print(f"Turning Left in Place at speed {speed} for {duration} seconds")
        self.motor_right.set_speed(speed)
        self.motor_left.set_speed(-speed)
        time.sleep(duration)
        self.stop_all_motors()

    def turn_right_in_place(self, duration=c.MOVEMENT_SETTINGS["TURN_DURATION"], speed=c.MOVEMENT_SETTINGS["TURN_SPEED"]):
        """Turns the robot right in place."""
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