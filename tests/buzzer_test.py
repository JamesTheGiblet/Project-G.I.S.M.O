# buzzer_test.py
# Tests the KY-006 passive buzzer connected to GPIO 18.

import RPi.GPIO as GPIO
import time

# Define the buzzer pin
buzzer_pin = 18

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set buzzer pin as output
GPIO.setup(buzzer_pin, GPIO.OUT)

# Function to play a tone on the buzzer
def play_tone(frequency, duration):
    """Plays a tone on the buzzer for a given duration.

    Args:
        frequency: The frequency of the tone in Hz.
        duration: The duration of the tone in seconds.
    """
    pwm = GPIO.PWM(buzzer_pin, frequency)
    pwm.start(50)  # 50% duty cycle
    time.sleep(duration)
    pwm.stop()

try:
    # Play a few different tones
    play_tone(262, 1)  # Middle C
    time.sleep(0.5)
    play_tone(523, 1)  # C one octave higher
    time.sleep(0.5)
    play_tone(1046, 1)  # C two octaves higher
    time.sleep(0.5)

except KeyboardInterrupt:
    # Clean up on exit (Ctrl+C)
    GPIO.cleanup()
    print("Buzzer test stopped.")