# buzzer.py

import RPi.GPIO as GPIO
import time
import config as c

class Buzzer:
    def __init__(self, pin):
        self.buzzer_pin = pin
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        self.pwm = None

    def play_tone(self, frequency, duration):
        """Plays a tone on the buzzer for a given duration.

        Args:
            frequency: The frequency of the tone in Hz.
            duration: The duration of the tone in seconds.
        """
        if frequency > 0:  # Check if frequency is greater than 0
            if self.pwm is None:
                self.pwm = GPIO.PWM(self.buzzer_pin, frequency)
            else:
                self.pwm.ChangeFrequency(frequency)
            self.pwm.start(50)  # 50% duty cycle
        else:
            self.pwm.stop()
            self.pwm = None

        time.sleep(duration)

        if self.pwm is not None:
            self.pwm.stop()
            self.pwm = None

    def play_startup_sound(self):
        """Plays a startup sound."""
        self.play_tone(262, 0.2)  # Middle C
        time.sleep(0.1)
        self.play_tone(330, 0.2)  # E
        time.sleep(0.1)
        self.play_tone(392, 0.2)  # G

    def play_obstacle_sound(self):
        """Plays a sound for obstacle detection."""
        self.play_tone(200, 0.1)
        time.sleep(0.1)
        self.play_tone(200, 0.1)

    def play_edge_sound(self):
        """Plays a sound for edge detection."""
        self.play_tone(800, 0.1)
        time.sleep(0.1)
        self.play_tone(300, 0.2)

    def play_shutdown_sound(self):
        """Plays a shutdown sound."""
        self.play_tone(392, 0.2)  # G
        time.sleep(0.1)
        self.play_tone(330, 0.2)  # E
        time.sleep(0.1)
        self.play_tone(262, 0.2)  # Middle C

    def play_custom_tune(self, notes):
        """Plays a custom tune defined by a list of (frequency, duration) tuples.

        Args:
            notes: A list of tuples, where each tuple contains the frequency (in Hz)
                    and the duration (in seconds) of a note.
        """
        for frequency, duration in notes:
            self.play_tone(frequency, duration)
            time.sleep(0.05)  # Short pause between notes

# Example usage (you'll likely call this from your main.py):
def initialize_buzzer():
    """Initializes the buzzer."""
    global buzzer
    buzzer = Buzzer(c.BUZZER_PIN)

# Define some common musical notes (you can add more)
NOTE_C4 = 262
NOTE_D4 = 294
NOTE_E4 = 330
NOTE_E5 = 340
NOTE_F4 = 349
NOTE_F5 = 375
NOTE_G4 = 392
NOTE_A4 = 440
NOTE_B4 = 494
NOTE_C5 = 523

# Example custom tunes
TUNE_HAPPY_BIRTHDAY = [
    (NOTE_C4, 0.2), (NOTE_C4, 0.2), (NOTE_D4, 0.4), (NOTE_C4, 0.4),
    (NOTE_F4, 0.4), (NOTE_E4, 0.6), (NOTE_C4, 0.2), (NOTE_C4, 0.2),
    (NOTE_D4, 0.4), (NOTE_C4, 0.4), (NOTE_G4, 0.4), (NOTE_F4, 0.6),
    (NOTE_C4, 0.2), (NOTE_C4, 0.2), (NOTE_C5, 0.4), (NOTE_A4, 0.4),
    (NOTE_F4, 0.4), (NOTE_E4, 0.4), (NOTE_D4, 0.4), (NOTE_A4, 0.2),
    (NOTE_A4, 0.2), (NOTE_F4, 0.4), (NOTE_G4, 0.4), (NOTE_F4, 0.6)
]

TUNE_IMPERIAL_MARCH = [
    (NOTE_A4, 0.5), (NOTE_A4, 0.5), (NOTE_A4, 0.5), (NOTE_F4, 0.35),
    (NOTE_C5, 0.15), (NOTE_A4, 0.5), (NOTE_F4, 0.35), (NOTE_C5, 0.15),
    (NOTE_A4, 0.65), (NOTE_E5, 0.5), (NOTE_E5, 0.5), (NOTE_E5, 0.5),
    (NOTE_F5, 0.35), (NOTE_C5, 0.15), (NOTE_G4, 0.5), (NOTE_F4, 0.35),
    (NOTE_C5, 0.15), (NOTE_A4, 0.65)
]