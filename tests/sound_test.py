# sound_test.py
# This code tests the sound sensor by printing a message when sound is detected.

import time
import RPi.GPIO as GPIO

# Define GPIO pin for the sound sensor
sound_sensor_pin = 21  # Adjust if needed

GPIO.setmode(GPIO.BCM)
GPIO.setup(sound_sensor_pin, GPIO.IN)

try:
    while True:
        if GPIO.input(sound_sensor_pin) == GPIO.HIGH:
            print("Sound detected!")
        time.sleep(0.1)  # Adjust delay as needed

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO pins