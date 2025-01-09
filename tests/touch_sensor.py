# touch_sensor.py

import RPi.GPIO as GPIO
import config as c

def initialize_touch_sensor():
    """Initializes the touch sensor GPIO pin."""
    GPIO.setup(c.SENSOR_PINS["TOUCH_SENSOR"], GPIO.IN)

def is_touched():
    """
    Checks if the touch sensor is currently touched.

    Returns:
        True if touched, False otherwise.
    """
    return GPIO.input(c.SENSOR_PINS["TOUCH_SENSOR"]) == GPIO.HIGH