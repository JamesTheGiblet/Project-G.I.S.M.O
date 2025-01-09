import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create a PCA9685 object.
pca = PCA9685(i2c)

# Set the PWM frequency to 60Hz.
pca.frequency = 60

# Define the PCA9685 channels for the RGB LED.
RED_CHANNEL = 13
GREEN_CHANNEL = 12
BLUE_CHANNEL = 11

# Function to set LED color.
def set_led_color(red, green, blue):
  """Sets the color of the RGB LED.

  Args:
    red: Red value (0-65535).
    green: Green value (0-65535).
    blue: Blue value (0-65535).
  """
  pca.channels[RED_CHANNEL].duty_cycle = red
  pca.channels[GREEN_CHANNEL].duty_cycle = green
  pca.channels[BLUE_CHANNEL].duty_cycle = blue

# Test the RGB LED.

# Red
set_led_color(65535, 0, 0)
time.sleep(1)

# Green
set_led_color(0, 65535, 0)
time.sleep(1)

# Blue
set_led_color(0, 0, 65535)
time.sleep(1)

# Yellow (Red + Green)
set_led_color(65535, 65535, 0)
time.sleep(1)

# Cyan (Green + Blue)
set_led_color(0, 65535, 65535)
time.sleep(1)

# Magenta (Red + Blue)
set_led_color(65535, 0, 65535)
time.sleep(1)

# White (Red + Green + Blue)
set_led_color(65535, 65535, 65535)
time.sleep(1)

# Off
set_led_color(0, 0, 0)