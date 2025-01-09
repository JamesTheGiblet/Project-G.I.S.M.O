# rgb_led.py

import time
import config as c

class RGBLed:  # Define the class at the top level of the module
    def __init__(self, pca):
        self.pca = pca
        self.colors = {
            "RED": c.LED_COLORS["RED"],
            "GREEN": c.LED_COLORS["GREEN"],
            "BLUE": c.LED_COLORS["BLUE"],
            "YELLOW": c.LED_COLORS["YELLOW"],
            "CYAN": c.LED_COLORS["CYAN"],
            "MAGENTA": c.LED_COLORS["MAGENTA"],
            "WHITE": c.LED_COLORS["WHITE"],
            "OFF": c.LED_COLORS["OFF"]
        }

    def set_color(self, red, green, blue):
        """Sets the color of the RGB LED."""
        self.pca.channels[c.RGB_LED_PINS["RED"]].duty_cycle = red
        self.pca.channels[c.RGB_LED_PINS["GREEN"]].duty_cycle = green
        self.pca.channels[c.RGB_LED_PINS["BLUE"]].duty_cycle = blue

    def test(self):
        """Tests the RGB LED with different colors."""
        print("Testing RGB LED...")
        for color_name, color_value in self.colors.items():
            print(f"Setting LED to: {color_name}")
            self.set_color(*color_value)
            time.sleep(1)

    def set_emotion(self, emotion):
        """Sets the LED color based on a predefined emotion."""
        if emotion == "happy":
            self.set_color(*self.colors["YELLOW"])
        elif emotion == "sad":
            self.set_color(*self.colors["BLUE"])
        elif emotion == "angry":
            self.set_color(*self.colors["RED"])
        elif emotion == "surprised":
            self.set_color(*self.colors["CYAN"])
            time.sleep(0.5)
            self.set_color(*self.colors["OFF"])
            time.sleep(0.2)
            self.set_color(*self.colors["CYAN"])
            time.sleep(0.5)
            self.set_color(*self.colors["OFF"])
            time.sleep(0.2)
            self.set_color(*self.colors["CYAN"])
        elif emotion == "searching":
            self.set_color(*self.colors["GREEN"])
        elif emotion == "neutral":
            self.set_color(*self.colors["OFF"])
        else:
            print("Invalid emotion specified.")

# You don't need initialize_rgb_led() anymore, since the object is created in main.py