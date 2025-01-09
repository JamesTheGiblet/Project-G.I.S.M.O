# robot.py

import time
import board
import busio
import RPi.GPIO as GPIO
from adafruit_pca9685 import PCA9685
import movement as m
import config as c  # Import the config module
import rgb_led as led
import buzzer as b
import touch_sensor as t
import sound_sensor as s
import display as d
import servo_control as s
import dead_reckoning as dr

# --- Initialization ---

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create a PCA9685 instance
pca = PCA9685(i2c)

# Set the PWM frequency
pca.frequency = c.PCA_FREQUENCY

# Initialize GPIO for Ultrasonic Sensor and Edge Sensors
GPIO.setmode(GPIO.BCM)

def initialize_pca():
    """Initializes the PCA9685 object."""
    global pca
    # Initialize I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create a PCA9685 object
    pca = PCA9685(i2c)

    # Set the PWM frequency to 60Hz
    pca.frequency = c.PCA_FREQUENCY

# --- Ultrasonic Sensor Function ---

def get_distance():
    """
    Measures the distance using the HC-SR04 ultrasonic sensor.

    Returns:
        The measured distance in centimeters. Returns 999.99 if measurement fails.
    """
    try:
        GPIO.setup(c.SENSOR_PINS["ULTRASONIC_TRIGGER"], GPIO.OUT)
        GPIO.setup(c.SENSOR_PINS["ULTRASONIC_ECHO"], GPIO.IN)

        GPIO.output(c.SENSOR_PINS["ULTRASONIC_TRIGGER"], GPIO.LOW)
        time.sleep(2e-6)  # 2 microseconds
        GPIO.output(c.SENSOR_PINS["ULTRASONIC_TRIGGER"], GPIO.HIGH)
        time.sleep(10e-6) # 10 microseconds
        GPIO.output(c.SENSOR_PINS["ULTRASONIC_TRIGGER"], GPIO.LOW)

        pulse_start_time = time.time()
        timeout_start_time = time.time()

        while GPIO.input(c.SENSOR_PINS["ULTRASONIC_ECHO"]) == 0:
            pulse_start_time = time.time()
            if time.time() - timeout_start_time > 0.02: # 20ms timeout for echo start
                return 999.99

        pulse_end_time = time.time()
        timeout_start_time = time.time()
        while GPIO.input(c.SENSOR_PINS["ULTRASONIC_ECHO"]) == 1:
            pulse_end_time = time.time()
            if time.time() - timeout_start_time > 0.02: # 20ms timeout for echo end
                return 999.99

        pulse_duration = pulse_end_time - pulse_start_time
        distance = pulse_duration * 17150  # Speed of sound in cm/s
        distance = round(distance, 2)

        return distance

    except Exception as e:
        print(f"Error reading distance: {e}")
        return 999.99 # Return a default large distance to indicate an error

# --- Edge Sensor Functions ---

def initialize_edge_sensors():
    """Initializes the edge sensor GPIO pins."""
    GPIO.setup(c.SENSOR_PINS["LEFT_EDGE_SENSOR"], GPIO.IN)
    GPIO.setup(c.SENSOR_PINS["RIGHT_EDGE_SENSOR"], GPIO.IN)

def read_edge_sensors():
    """
    Reads the values of the left and right edge sensors.

    Returns:
        A tuple containing the left and right sensor values (0 or 1).
        Returns (None, None) on error
    """
    try:
        left_sensor_value = GPIO.input(c.SENSOR_PINS["LEFT_EDGE_SENSOR"])
        right_sensor_value = GPIO.input(c.SENSOR_PINS["RIGHT_EDGE_SENSOR"])

        return left_sensor_value, right_sensor_value
    except Exception as e:
        print(f"Error reading edge sensors: {e}")
        return None, None

# --- Cleanup ---
def cleanup(pca, rgb_led_instance):
    """Clean up resources."""
    # Access the movement object created in main.py
    main_movement_object = globals().get('movement')

    if main_movement_object:
        main_movement_object.stop_all_motors()
    else:
        print("Warning: Movement object not found. Motors may not have stopped.")

    rgb_led_instance.set_color(*c.LED_COLORS["OFF"])
    d.clear_display()
    pca.deinit()
    GPIO.cleanup()