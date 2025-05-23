# config.py

# --- System Configuration ---
DEBUG_MODE = True  # Enable/disable debug messages

# --- Hardware ---
# This section defines the hardware components connected to the robot and their pin/channel assignments.

# --- PCA9685 PWM Servo Driver ---
PCA_FREQUENCY = 60  # PWM frequency for the PCA9685 (common value for servos)

# --- L298N Motor Driver ---
# Pin mapping for the L298N motor driver (connected to PCA9685 channels).
MOTOR_DRIVER_PINS = {
    "RIGHT_FORWARD": 7,   # INT1
    "RIGHT_BACKWARD": 6,  # INT2
    "LEFT_FORWARD": 8,    # INT3
    "LEFT_BACKWARD": 10,  # INT4
}

# --- Sensors ---
# Pin mapping for the various sensors connected to the Raspberry Pi's GPIO pins.
SENSOR_PINS = {
    "ULTRASONIC_ECHO": 23,
    "ULTRASONIC_TRIGGER": 22,
    "LEFT_EDGE_SENSOR": 12,
    "RIGHT_EDGE_SENSOR": 13,
    "TOUCH_SENSOR": 17,
    "SOUND_SENSOR": 21,
}

# --- MPU9250 IMU ---
MPU9250_I2C_ADDRESS = 0x68  # Default I2C address (may vary depending on AD0 pin)

# --- RGB LED ---
# Pin mapping for the RGB LED (connected to PCA9685 channels).
RGB_LED_PINS = {
    "RED": 13,
    "GREEN": 12,
    "BLUE": 11,
}

# --- Buzzer ---
# Pin mapping for the buzzer (connected to a Raspberry Pi GPIO pin).
BUZZER_PIN = 18

# --- OLED Display ---
# Configuration for the OLED display.
DISPLAY = {
    "WIDTH": 128,
    "HEIGHT": 64,
    "I2C_ADDRESS": 0x3C,  # Typically 0x3C or 0x3D, check your display's address
    "CONNECTION": "PCA9685",  # Display is connected via PCA9685
}

# --- Servos ---
# Configuration for the servos connected to the PCA9685.
SERVO_PINS = {
    "LHS": 0,  # Left-hand side lifting arm
    "RHS": 1,  # Right-hand side lifting arm
    "HEAD": 2,  # Head up/down
}

# Servo pulse width limits (in microseconds, calibrated values).
SERVO_PULSE_WIDTHS = {
    "LHS": {"MIN": 2150, "MAX": 2500},
    "RHS": {"MIN": 1750, "MAX": 2050},
    "HEAD": {"MIN": 600, "MAX": 800},
}

# Servo angle settings (in degrees).
SERVO_ANGLES = {
    "LHS_UP": 0,        # Example angle - adjust as needed
    "LHS_CENTER": 45,    # Example angle - adjust as needed
    "LHS_DOWN": 90,     # Example angle - adjust as needed
    "RHS_UP": 180,      # Example angle - adjust as needed
    "RHS_CENTER": 135,  # Example angle - adjust as needed
    "RHS_DOWN": 90,     # Example angle - adjust as needed
    "HEAD_UP": 140,     # Example angle - adjust as needed
    "HEAD_CENTER": 45,  # Example angle - adjust as needed
    "HEAD_DOWN": 0,     # Example angle - adjust as needed
}

# Servo operating speed (seconds per 60 degrees at 6V).
SERVO_OPERATING_SPEED = 0.08  # Example value

# --- Robot Movement Settings ---
# Default values for robot movement.
MOVEMENT_SETTINGS = {
    "FORWARD_SPEED": 0.5,
    "TURN_SPEED": 0.5,
    "RAMP_TIME": 0.5,
    "MOVE_DURATION": 0.5,
    "TURN_DURATION": 0.2,
    "OBSTACLE_DISTANCE": 10,  # in cm
}

# --- RGB LED Colors ---
# Predefined colors for the RGB LED.
LED_COLORS = {
    "RED": (65535, 0, 0),
    "GREEN": (0, 65535, 0),
    "BLUE": (0, 0, 65535),
    "YELLOW": (65535, 65535, 0),
    "CYAN": (0, 65535, 65535),
    "MAGENTA": (65535, 0, 65535),
    "WHITE": (65535, 65535, 65535),
    "OFF": (0, 0, 0),
}