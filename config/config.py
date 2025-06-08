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
    "FORWARD_SPEED": 0.7,  # Increased from 0.5
    "TURN_SPEED": 0.6,     # Increased from 0.5
    "RAMP_TIME": 0.5,
    "MOVE_DURATION": 2.0, # Increased from 0.5
    "TURN_DURATION": 0.3,  # Increased from 0.2
    "OBSTACLE_DISTANCE": 20, # in cm, increased from 10
    "STUCK_TIME": 5,  # Seconds before considered stuck
    "STUCK_DISTANCE": 0.05, # Distance in meters to consider movement significant
    "AVOIDANCE_ZONE_RADIUS": 0.2, # Radius around obstacle to avoid (in meters)
    "OBSTACLE_MEMORY_TIME": 30, # Time to remember obstacle (in seconds)
    "STUCK_THRESHOLD": 3  # Number of times to be stuck before exiting wandering
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

# --- Mapping ---
MAP_SETTINGS = {
    "GRID_SIZE_X": 50,   # Number of cells in the X dimension
    "GRID_SIZE_Y": 50,   # Number of cells in the Y dimension
    "CELL_SIZE": 0.1,    # Size of one cell in meters (10 cm)
    "OBSTACLE_THRESHOLD": 0.8,   # Probability above which a cell is considered occupied
    "FREE_THRESHOLD": 0.2,     # Probability below which a cell is considered free
    "UPDATE_INTERVAL": 2,     # Update map every 2 seconds
    "DISPLAY_MAP": True,        # Set to False if you don't want to display the map on the terminal
    "MAP_DISPLAY_INTERVAL": 10,  # Display map every 10 seconds 
    "LOOP_CLOSURE_DISTANCE": 0.5, # For more flexibility in loop closure detection
}

# --- VL53L0X Time-of-Flight Sensor ---
TOF_SENSOR = {
    "I2C_ADDRESS": 0x29,  # Default I2C address
    "XSHUT_PIN": None,   # (Optional) GPIO pin for XSHUT or PCA channel
    "DISTANCE_MODE": 2, # 1 = Short, 2 = Medium, 3 = Long
}