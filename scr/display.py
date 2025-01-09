# display.py

import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import random
import config as c

"""
display.py

This module provides functions to control an SSD1306 OLED display for the Gismo robot. 
It includes functionalities to draw various faces representing different emotional states 
and to display text on the screen. The module is designed to be used with a Raspberry Pi 
and requires the adafruit_ssd1306 library for OLED display control, along with PIL (Pillow) 
for image and text rendering.

Functions:
    - initialize_display(): Initializes the OLED display.
    - clear_display(): Clears the OLED display.
    - draw_eyes(x_offset_left, y_offset_left, x_offset_right, y_offset_right, blink): Draws a pair of eyes on the display.
    - look_around(): Simulates the eyes looking around randomly.
    - blink(): Simulates a blinking action of the eyes.
    - test_display(): Runs a test sequence displaying various eye movements and blinking.
    - draw_face_neutral(): Draws a neutral face on the display.
    - draw_face_happy(): Draws a happy face on the display.
    - draw_face_sad(): Draws a sad face on the display.
    - draw_face_angry(): Draws an angry face on the display.
    - draw_face_surprised(): Draws a surprised face on the display.
    - draw_face_searching(): Draws a searching face on the display.
    - draw_text(text): Displays text on the OLED display.

Dependencies:
    - board: Provides board-specific pin definitions.
    - busio: Provides I2C communication support.
    - PIL (Pillow): Used for image and text drawing.
    - adafruit_ssd1306: Library for SSD1306 OLED display control.
    - random: Used for generating random eye movements.
    - config: Configuration settings for the display and other parameters.
"""

# --- Eye Parameters (adjust as you like) ---
EYE_RADIUS = 10
EYE_DISTANCE = 40
IRIS_RADIUS = 4
BLINK_DURATION = 0.1
LOOK_AROUND_INTERVAL = 3  # Seconds

# --- Initialize Display ---
# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Declare display as a global variable
display = None

def initialize_display():
    """Initializes the OLED display."""
    global display
    try:
        display = adafruit_ssd1306.SSD1306_I2C(c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"], i2c, addr=c.DISPLAY["I2C_ADDRESS"])
        # Clear the display
        display.fill(0)
        display.show()
    except ValueError:
        print("Error initializing display. Check I2C address and wiring.")
        display = None

# --- Functions ---

def clear_display():
    """Clears the OLED display."""
    if display:
        display.fill(0)
        display.show()

def draw_eyes(x_offset_left=0, y_offset_left=0, x_offset_right=0, y_offset_right=0, blink=False):
    """Draws a pair of eyes on the display."""
    if not display:
        return

    # Create a blank image
    image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
    draw = ImageDraw.Draw(image)

    # Eye positions
    left_eye_center = (c.DISPLAY["WIDTH"] // 2 - EYE_DISTANCE // 2, c.DISPLAY["HEIGHT"] // 2)
    right_eye_center = (c.DISPLAY["WIDTH"] // 2 + EYE_DISTANCE // 2, c.DISPLAY["HEIGHT"] // 2)

    if blink:
        # Draw closed eyes (lines)
        eye_top = left_eye_center[1] - EYE_RADIUS // 2
        eye_bottom = left_eye_center[1] + EYE_RADIUS // 2
        draw.line((left_eye_center[0] - EYE_RADIUS, eye_top, left_eye_center[0] + EYE_RADIUS, eye_top), fill=255)
        draw.line((left_eye_center[0] - EYE_RADIUS, eye_bottom, left_eye_center[0] + EYE_RADIUS, eye_bottom), fill=255)

        eye_top = right_eye_center[1] - EYE_RADIUS // 2
        eye_bottom = right_eye_center[1] + EYE_RADIUS // 2
        draw.line((right_eye_center[0] - EYE_RADIUS, eye_top, right_eye_center[0] + EYE_RADIUS, eye_top), fill=255)
        draw.line((right_eye_center[0] - EYE_RADIUS, eye_bottom, right_eye_center[0] + EYE_RADIUS, eye_bottom), fill=255)
    else:
        # Draw open eyes (circles)
        draw.ellipse((left_eye_center[0] - EYE_RADIUS, left_eye_center[1] - EYE_RADIUS,
                      left_eye_center[0] + EYE_RADIUS, left_eye_center[1] + EYE_RADIUS),
                     outline=255, fill=0)
        draw.ellipse((right_eye_center[0] - EYE_RADIUS, right_eye_center[1] - EYE_RADIUS,
                      right_eye_center[0] + EYE_RADIUS, right_eye_center[1] + EYE_RADIUS),
                     outline=255, fill=0)

        # Draw irises
        left_iris_center = (left_eye_center[0] + x_offset_left, left_eye_center[1] + y_offset_left)
        right_iris_center = (right_eye_center[0] + x_offset_right, right_eye_center[1] + y_offset_right)

        draw.ellipse((left_iris_center[0] - IRIS_RADIUS, left_iris_center[1] - IRIS_RADIUS,
                      left_iris_center[0] + IRIS_RADIUS, left_iris_center[1] + IRIS_RADIUS),
                     outline=255, fill=255)
        draw.ellipse((right_iris_center[0] - IRIS_RADIUS, right_iris_center[1] - IRIS_RADIUS,
                      right_iris_center[0] + IRIS_RADIUS, right_iris_center[1] + IRIS_RADIUS),
                     outline=255, fill=255)

    # Display the image
    display.image(image)
    display.show()

def look_around():
    """Makes the eyes look around randomly."""
    if display:
        for _ in range(5):
            x_offset_left = random.randint(-EYE_RADIUS, EYE_RADIUS)
            y_offset_left = random.randint(-EYE_RADIUS, EYE_RADIUS)
            x_offset_right = random.randint(-EYE_RADIUS, EYE_RADIUS)
            y_offset_right = random.randint(-EYE_RADIUS, EYE_RADIUS)
            draw_eyes(x_offset_left, y_offset_left, x_offset_right, y_offset_right)
            time.sleep(0.5)

def blink():
    """Makes the eyes blink."""
    if display:
        draw_eyes(blink=True)  # Draw closed eyes
        time.sleep(BLINK_DURATION)
        draw_eyes()  # Draw open eyes

def test_display():
    """Tests the display."""
    if display:
        try:
            draw_eyes()
            time.sleep(1)
            look_around()
            time.sleep(1)
            for _ in range(3):
                blink()
                time.sleep(0.5)
            clear_display()

        except KeyboardInterrupt:
            print("Display test stopped.")
            clear_display()
            
def draw_face_neutral():
    """Draws a neutral face on the OLED display."""
    if display:
        # Create blank image for drawing
        image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
        draw = ImageDraw.Draw(image)

        # Draw a simple neutral face
        # Head
        draw.ellipse((20, 10, 108, 54), outline=255, fill=0)
        # Eyes
        draw.ellipse((35, 20, 50, 30), outline=255, fill=0)  # Left eye
        draw.ellipse((80, 20, 95, 30), outline=255, fill=0)  # Right eye
        # Mouth
        draw.line((40, 45, 90, 45), fill=255)

        # Display the image
        display.image(image)
        display.show()

def draw_face_happy():
    """Draws a happy face on the OLED display."""
    if display:
        # Create blank image for drawing
        image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
        draw = ImageDraw.Draw(image)

        # Draw a simple happy face
        # Head
        draw.ellipse((20, 10, 108, 54), outline=255, fill=0)
        # Eyes
        draw.ellipse((35, 20, 50, 30), outline=255, fill=0)  # Left eye
        draw.ellipse((80, 20, 95, 30), outline=255, fill=0)  # Right eye
        # Mouth
        draw.arc((40, 35, 90, 50), 0, 180, fill=255)

        # Display the image
        display.image(image)
        display.show()

def draw_face_sad():
    """Draws a sad face on the OLED display."""
    if display:
        # Create blank image for drawing
        image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
        draw = ImageDraw.Draw(image)

        # Draw a simple sad face
        # Head
        draw.ellipse((20, 10, 108, 54), outline=255, fill=0)
        # Eyes
        draw.ellipse((35, 20, 50, 30), outline=255, fill=0)  # Left eye
        draw.ellipse((80, 20, 95, 30), outline=255, fill=0)  # Right eye
        # Mouth
        draw.arc((40, 35, 90, 50), 180, 0, fill=255)

        # Display the image
        display.image(image)
        display.show()

def draw_face_angry():
    """Draws an angry face on the OLED display."""
    if display:
        # Create blank image for drawing
        image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
        draw = ImageDraw.Draw(image)

        # Draw a simple angry face
        # Head
        draw.ellipse((20, 10, 108, 54), outline=255, fill=0)
        # Eyes
        draw.line((35, 20, 50, 30), fill=255)  # Left eye (slanted)
        draw.line((50, 20, 35, 30), fill=255)
        draw.line((80, 20, 95, 30), fill=255)  # Right eye (slanted)
        draw.line((95, 20, 80, 30), fill=255)
        # Mouth
        draw.line((40, 45, 90, 45), fill=255)

        # Display the image
        display.image(image)
        display.show()

def draw_face_surprised():
    """Draws a surprised face on the OLED display."""
    if display:
        # Create blank image for drawing
        image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
        draw = ImageDraw.Draw(image)

        # Draw a simple surprised face
        # Head
        draw.ellipse((20, 10, 108, 54), outline=255, fill=0)
        # Eyes
        draw.ellipse((35, 20, 50, 30), outline=255, fill=255)  # Left eye
        draw.ellipse((80, 20, 95, 30), outline=255, fill=255)  # Right eye
        # Mouth
        draw.ellipse((55, 40, 75, 50), outline=255, fill=255)

        # Display the image
        display.image(image)
        display.show()
        
def draw_face_searching():
    """Draws a searching face on the OLED display."""
    if display:
        # Create blank image for drawing
        image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
        draw = ImageDraw.Draw(image)

        # Draw a simple searching face
        # Head
        draw.ellipse((20, 10, 108, 54), outline=255, fill=0)

        # Eyes (looking to the right)
        draw.ellipse((35, 20, 50, 30), outline=255, fill=0)  # Left eye (pupil to the right)
        draw.ellipse((80, 20, 95, 30), outline=255, fill=0)  # Right eye (pupil to the right)
        draw.ellipse((45, 23, 48, 27), outline=0, fill=0)  # Left pupil
        draw.ellipse((90, 23, 93, 27), outline=0, fill=0)  # Right pupil
        
        # Mouth (neutral)
        draw.line((40, 45, 90, 45), fill=255)

        # Display the image
        display.image(image)
        display.show()

def draw_text(text):
    """Displays text on the OLED display."""
    if display:
        # Create blank image for drawing
        image = Image.new("1", (c.DISPLAY["WIDTH"], c.DISPLAY["HEIGHT"]))
        draw = ImageDraw.Draw(image)

        # Load a font (make sure you have the font file in your project directory)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        except OSError:
            print("Font not found, using default font.")
            font = ImageFont.load_default()

        # Draw the text
        draw.text((0, 0), text, font=font, fill=255)

        # Display the image
        display.image(image)
        display.show()

def clear_display():
    """Clears the OLED display."""
    if display:
        display.fill(0)
        display.show()