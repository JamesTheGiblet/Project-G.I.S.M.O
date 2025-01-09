# display_test.py
# Tests the SSD1306 128x64 OLED display by drawing a confused face.

import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Define the I2C bus and display dimensions
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear the display
display.fill(0)
display.show()

# Create blank image for drawing
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)

# Draw a confused face
# Head
draw.ellipse((20, 10, 108, 54), outline=255, fill=0)
# Eyes
draw.line((35, 25, 45, 35), fill=255)  # Left eye (slanted)
draw.line((45, 25, 35, 35), fill=255)
draw.line((80, 25, 90, 35), fill=255)  # Right eye (slanted)
draw.line((90, 25, 80, 35), fill=255)
# Mouth
draw.line((40, 45, 60, 40), fill=255)  # Slightly curved line for mouth
draw.line((60, 40, 85, 45), fill=255)

# Display the image
display.image(image)
display.show()