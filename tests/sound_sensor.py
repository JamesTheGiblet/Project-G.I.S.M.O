# sound_sensor.py

import RPi.GPIO as GPIO
import config as c

def initialize_sound_sensor():
    """Initializes the sound sensor GPIO pin."""
    GPIO.setup(c.SENSOR_PINS["SOUND_SENSOR"], GPIO.IN)  # Access from SENSOR_PINS

def is_sound_detected():
    """
    Checks if the sound sensor is currently detecting sound.

    Returns:
        True if sound is detected, False otherwise.
    """
    return GPIO.input(c.SENSOR_PINS["SOUND_SENSOR"]) == GPIO.HIGH  # Access from SENSOR_PINS