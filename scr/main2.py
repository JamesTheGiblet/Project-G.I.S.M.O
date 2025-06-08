import random
import robot_commands  # Import the robot_commands module
from scr import movement
import display
import rgb_led
from scr import dead_reckoning
import time
import select
import sys
import robot  # Import the robot module for accessing necessary functions
from scr import servo_control
import stuck_detection as sd
from scr import buzzer as b
import touch_sensor as t
import sound_sensor as s
import vl53l0x_sensor as tof
from config import config as c

# --- Code Functions ---
# This program controls a robot named Gismo.
# Version 0.72 integrates dead reckoning, mapping, and a display module for enhanced functionality.
# The robot can move forward, backward, turn left, and turn right, with a ramp-up/ramp-down
# feature for smoother movements. It uses the PCA9685 PWM driver to control the L298N motor driver,
# the HC-SR04 sensor to measure distance to obstacles, and edge sensors to detect edges.
# The robot also uses an RGB LED for visual feedback, a buzzer for audio feedback,
# and implements dead reckoning for position and heading estimation using the MPU6050 library.

# --- Helper Functions ---

def react_to_sound(rgb_led_instance):
    """Makes the robot react to sound by turning, moving, and playing a tune."""
    print("Sound detected! Reacting...")
    movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"] * 2)
    movement.move_forward(speed=c.MOVEMENT_SETTINGS["FORWARD_SPEED"])
    rgb_led_instance.set_emotion("surprised")
    display.draw_face_surprised()  # Show surprised face on display
    b.buzzer.play_custom_tune(b.TUNE_IMPERIAL_MARCH)  # Play the tune
    time.sleep(0.5)
    movement.stop_all_motors()
    rgb_led_instance.set_emotion("neutral")
    display.draw_face_neutral()  # Show neutral face on display

# --- Main Program ---

if __name__ == "__main__":
    try:
        # Initialize robot components
        pca = robot.initialize_pca() 
        rgb_led_instance = rgb_led.RGBLed(pca)
        movement = movement.Movement(pca) 
        dead_reckoning = dead_reckoning.DeadReckoning()
        tof_sensor_instance = tof.initialize_tof_sensor()  # Initialize ToF sensor
        display.initialize_display()  # Initialize the display

        # Initialize other components
        b.initialize_buzzer()
        t.initialize_touch_sensor()
        s.initialize_sound_sensor()
        servo_controller = servo_control.initialize_servos(pca)  # Initialize servos
        servo_controller.initialize_servos() 
        robot.initialize_edge_sensors()  # Initialize edge sensors

        b.buzzer.play_startup_sound()
        servo_controller.test_servos() 
        rgb_led_instance.test()
        display.test_display()  # Run display test

        last_update = time.time()
        last_position = dead_reckoning.get_position()
        time_last_moved = time.time()
        stuck_count = 0
        obstacle_detected_at = None

        # Robot starts in wandering mode
        wandering = True
        print("Gismo is in wandering mode. Press Enter to start command mode.")
        display.draw_face_searching()  # Show searching face initially

        while True:
            # 1. Check for immediate obstacles and edges
            left_edge, right_edge = robot.read_edge_sensors()  # Use the robot module for edge sensor readings
            distance = tof_sensor_instance.get_distance() 

            if left_edge == 1:
                # Handle left edge
                print("Left edge detected! Turning right...")
                movement.turn_right_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                rgb_led_instance.set_emotion("angry")
                display.draw_face_angry()  # Show angry face on display
                b.buzzer.play_edge_sound()
                movement.stop_all_motors()
                time.sleep(0.5)  # Slight pause after edge correction
                continue

            elif right_edge == 1:
                # Handle right edge
                print("Right edge detected! Turning left...")
                movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                rgb_led_instance.set_emotion("angry")
                display.draw_face_angry()  # Show angry face on display
                b.buzzer.play_edge_sound()
                movement.stop_all_motors()
                time.sleep(0.5)  # Slight pause after edge correction
                continue

            if distance is not None and distance < c.MOVEMENT_SETTINGS["OBSTACLE_DISTANCE"]:
                # Handle obstacle
                print("Obstacle detected!")
                movement.stop_all_motors()

                # Record the position where the obstacle was detected
                obstacle_detected_at = (dead_reckoning.get_position(), time.time())

                servo_control.raise_arms(pca)  # Raise arms
                time.sleep(0.5)
                servo_control.move_head_up(pca)  # Move head up
                rgb_led_instance.set_emotion("surprised")
                display.draw_face_surprised()  # Show surprised face on display
                b.buzzer.play_obstacle_sound()
                time.sleep(0.5)
                servo_control.move_head_center(pca)  # Move head back to center

                # Turn to a random direction after encountering an obstacle
                if random.choice([True, False]):
                    movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                else:
                    movement.turn_right_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])

                time.sleep(0.5)  # Slight pause after obstacle avoidance

            # 2. Update robot state and check for other conditions
            dead_reckoning.update() 
            current_time = time.time() 

            # Print dead reckoning information every second
            if current_time - last_update >= 1.0:
                position = dead_reckoning.get_position()
                heading = dead_reckoning.get_heading()
                print(f"Position (X, Y): ({position[0]:.2f}, {position[1]:.2f}), Heading: {heading:.2f} degrees")
                display.draw_text(f"Pos: ({position[0]:.2f}, {position[1]:.2f}), Hdg: {heading:.2f}") 
                last_update = current_time

            # Handle stuck situation using the separate module
            sd.handle_stuck_situation(pca, rgb_led_instance, movement, dead_reckoning)
            if stuck_count >= c.MOVEMENT_SETTINGS["STUCK_THRESHOLD"]:
                wandering = False  # Exit wandering mode if stuck for too long
                movement.stop_all_motors()
                rgb_led_instance.set_emotion("neutral")
                display.draw_face_sad()  # Show sad face on display
                print("Robot got stuck. Entering command mode.")
                continue

            # Check for sound
            # if sound_detected:
            #     react_to_sound(rgb_led_instance) 
            #     sound_detected = False

            # 3. Move forward (if no obstacles or edges)
            movement.motor_right.set_speed(c.MOVEMENT_SETTINGS["FORWARD_SPEED"])
            movement.motor_left.set_speed(c.MOVEMENT_SETTINGS["FORWARD_SPEED"])
            rgb_led_instance.set_emotion("searching")
            display.draw_face_searching()  # Show searching face on display
            time_last_moved = time.time()  # Update time of last movement

            # Check for user input without blocking
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                command = sys.stdin.readline().strip()
                if command == 'exit':
                    raise KeyboardInterrupt
                elif command == 'stop':
                    wandering = False
                    movement.stop_all_motors()
                    rgb_led_instance.set_emotion("neutral")
                    display.draw_face_neutral()  # Show neutral face on display
                    print("Entering command mode. Type 'start' to resume wandering.")
                elif command == 'start':
                    wandering = True
                    rgb_led_instance.set_emotion("searching")
                    display.draw_face_searching()  # Show searching face on display
                    print("Resuming wandering...")
                else:
                    if not wandering:
                        robot_commands.handle_command(command, pca, rgb_led_instance, movement, dead_reckoning)
                    else:
                        print("Command ignored in wandering mode. Type 'stop' to enter command mode.")

    except Exception as e:
        print(f"An error occurred during initialization: {e}") 
        # Perform any necessary cleanup (e.g., stop motors, release resources)
        movement.stop_all_motors() 
        pca.cleanup() 
        exit(1)