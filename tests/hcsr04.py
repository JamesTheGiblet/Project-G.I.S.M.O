#HCSR04 Sensor test

import time
import RPi.GPIO as GPIO

# Define the GPIO pins for the HC-SR04 sensor.
ECHO_PIN = 23
TRIGGER_PIN = 22

# Function to get distance from the HC-SR04 sensor.
def get_distance(trigger_pin, echo_pin):
  GPIO.setup(trigger_pin, GPIO.OUT)
  GPIO.setup(echo_pin, GPIO.IN)

  GPIO.output(trigger_pin, GPIO.LOW)
  time.sleep(2e-6)
  GPIO.output(trigger_pin, GPIO.HIGH)
  time.sleep(10e-6)
  GPIO.output(trigger_pin, GPIO.LOW)

  while GPIO.input(echo_pin) == 0:
    pass
  pulse_start_time = time.time()

  while GPIO.input(echo_pin) == 1:
    pass
  pulse_end_time = time.time()

  pulse_duration = pulse_end_time - pulse_start_time
  distance = pulse_duration * 17150  # Speed of sound in cm/s
  distance = round(distance, 2)
  return distance

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Test the ultrasonic sensor.
while True:
  distance = get_distance(TRIGGER_PIN, ECHO_PIN)

  print(f"Distance: {distance} cm")

  time.sleep(1)  # Pause between readings