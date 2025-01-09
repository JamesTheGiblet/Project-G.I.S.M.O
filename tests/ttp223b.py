#TTP23B test

import time
import RPi.GPIO as GPIO

# Define the GPIO pin for the touch sensor.
TOUCH_SENSOR_PIN = 17

# Function to detect touch.
def detect_touch(pin):
  """Detects a touch event on the specified pin.

  Args:
    pin: The GPIO pin connected to the touch sensor.

  Returns:
    True if a touch is detected, False otherwise.
  """
  GPIO.setup(pin, GPIO.IN)
  touch_detected = GPIO.input(pin)  # High signal when touched
  return touch_detected

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Test the touch sensor.
while True:
  touch_detected = detect_touch(TOUCH_SENSOR_PIN)

  if touch_detected:
    print("Touch detected!")
  else:
    print("No touch...")

  time.sleep(0.1)  # Pause between readings