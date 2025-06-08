# touch_sensor.py

import RPi.GPIO as GPIO
import config as c

"""
touch_sensor.py

This module provides functions for interacting with a touch sensor connected to the Raspberry Pi.

Functions:
    - initialize_touch_sensor(): Initializes the touch sensor GPIO pin.
    - is_touched(): Checks if the touch sensor is currently being touched.
"""

def initialize_touch_sensor():
    """Initializes the touch sensor GPIO pin."""
    GPIO.setup(c.SENSOR_PINS["TOUCH_SENSOR"], GPIO.IN)  # Access from SENSOR_PINS

def is_touched():
    """
    Checks if the touch sensor is currently being touched.

    Returns:
        True if touched, False otherwise.
    """
    return GPIO.input(c.SENSOR_PINS["TOUCH_SENSOR"]) == GPIO.HIGH  # Access from SENSOR_PINS