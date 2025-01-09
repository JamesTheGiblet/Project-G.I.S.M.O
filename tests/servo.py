import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create a PCA9685 object.
pca = PCA9685(i2c)

# Set the PWM frequency to 60Hz (a common value for servos).
pca.frequency = 60

# Define the PCA9685 channels for the servos.
SERVO_CHANNEL_1 = 0  # Right-hand side arm
SERVO_CHANNEL_2 = 1  # Left-hand side arm (inverted)

# Servo pulse width range (obtained empirically for SERVO_CHANNEL_1).
# You might need to adjust these for SERVO_CHANNEL_2 if it's different.
MIN_PULSE = 5413
MAX_PULSE = 6124

# Variable to store the current servo angle (estimated).
current_angle_1 = 0
current_angle_2 = 0

# Function to set servo angle.
def set_servo_angle(channel, angle):
  """Sets the angle of the servo motor and updates current_angle.

  Args:
    channel: The PCA9685 channel connected to the servo.
    angle: The desired angle in degrees (0-180).
  """
  global current_angle_1, current_angle_2  # Access the global variables
  pulse = int(angle / 180 * (MAX_PULSE - MIN_PULSE) + MIN_PULSE)  # Calculate pulse width
  pca.channels[channel].duty_cycle = pulse
  if channel == SERVO_CHANNEL_1:
    current_angle_1 = angle  # Update the estimated angle for servo 1
  elif channel == SERVO_CHANNEL_2:
    current_angle_2 = angle  # Update the estimated angle for servo 2
  print(f"Servo channel {channel} angle set to {angle} degrees (pulse width: {pulse})")

# Test the servos with synchronized movement.
while True:
  # Initialize servos to their lowest point.
  set_servo_angle(SERVO_CHANNEL_1, 0)
  set_servo_angle(SERVO_CHANNEL_2, 180)  # Reversed for inverted servo

  # Move the arms up and down slowly, simultaneously.
  for angle in range(0, 180, 5):  # From 0 to 180 degrees in steps of 5
    set_servo_angle(SERVO_CHANNEL_1, angle)
    set_servo_angle(SERVO_CHANNEL_2, 180 - angle)  # Reversed direction for inverted servo
    time.sleep(0.5)  # Increased delay for slower movement

  for angle in range(180, 0, -5):  # From 180 to 0 degrees in steps of 5
    set_servo_angle(SERVO_CHANNEL_1, angle)
    set_servo_angle(SERVO_CHANNEL_2, 180 - angle)  # Reversed direction for inverted servo
    time.sleep(0.5)  # Increased delay for slower movement