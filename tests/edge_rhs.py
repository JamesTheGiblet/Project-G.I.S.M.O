import RPi.GPIO as GPIO
import time

# Define GPIO pin for the right-hand side (RHS) sensor
rhs_sensor_pin = 12  # Adjust if needed

GPIO.setmode(GPIO.BCM)
GPIO.setup(rhs_sensor_pin, GPIO.IN)  # Assuming sensor outputs HIGH when detecting a line

try:
    while True:
        rhs_sensor_value = GPIO.input(rhs_sensor_pin)

        if rhs_sensor_value == 0:  # RHS sensor detects an edge (no line)
            print("Right edge detected!")
        else:
            print("Line detected!")  # Or "No edge detected!"

        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    GPIO.cleanup()