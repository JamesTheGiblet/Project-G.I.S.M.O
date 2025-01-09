# main.py (Version 0.35: Removing Mapping and Loop Closure)

import time
import robot as rc
import movement as m
import config as c
import rgb_led as led
import buzzer as b
import touch_sensor as t
import sound_sensor as s
import servo_control as sc
import dead_reckoning as dr
import random

# --- Code Functions ---
# This program controls a robot named Gismo.
# Version 0.35 removes mapping and loop closure functionality, reverting to basic dead reckoning.
# The robot can move forward, backward, turn left, and turn right, with a ramp-up/ramp-down
# feature for smoother movements. It uses the PCA9685 PWM driver to control the L298N motor driver,
# the HC-SR04 sensor to measure distance to obstacles, and edge sensors to detect edges.

# --- Helper Functions ---

def react_to_sound(pca, rgb_led_instance):
    """Makes the robot react to sound by turning, moving, and playing a tune."""
    print("Sound detected! Reacting...")
    movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"] * 2)
    movement.move_forward(duration=c.MOVEMENT_SETTINGS["MOVE_DURATION"])
    rgb_led_instance.set_emotion("surprised")
    b.buzzer.play_custom_tune(b.TUNE_IMPERIAL_MARCH)  # Play the tune
    time.sleep(0.5)
    rgb_led_instance.set_emotion("neutral")

def wiggle(pca, rgb_led_instance, duration=0.5, speed=0.7):
    """Makes the robot wiggle for a short duration."""
    movement.turn_left_in_place(duration / 2)
    movement.turn_right_in_place(duration / 2)

# --- Main Program ---

if __name__ == "__main__":
    try:
        rc.initialize_pca()
        rc.initialize_edge_sensors()
        b.initialize_buzzer()
        t.initialize_touch_sensor()
        s.initialize_sound_sensor()
        sc.initialize_servos(rc.pca)
        rgb_led_instance = led.RGBLed(rc.pca)
        movement = m.Movement(rc.pca)
        dead_reckoning = dr.DeadReckoning()
        b.buzzer.play_startup_sound()
        sc.test_servos(rc.pca)
        rgb_led_instance.test()

        last_update = time.time()
        last_turn = time.time()

        while True:
            dead_reckoning.update()
            current_time = time.time()

            distance = rc.get_distance()
            left_edge, right_edge = rc.read_edge_sensors()
            touched = t.is_touched()
            sound_detected = s.is_sound_detected()

            # Print dead reckoning information every second
            if current_time - last_update >= 1.0:
                position = dead_reckoning.get_position()
                heading = dead_reckoning.get_heading()
                print(f"Position (X, Y): ({position[0]:.2f}, {position[1]:.2f}), Heading: {heading:.2f} degrees")
                last_update = current_time

            if sound_detected:
                react_to_sound(rc.pca, rgb_led_instance)
            elif touched:
                print("Touched! Wiggling...")
                wiggle(rc.pca, rgb_led_instance)
                rgb_led_instance.set_emotion("happy")
                b.buzzer.play_tone(500, 0.1)
                time.sleep(0.5)
                rgb_led_instance.set_emotion("neutral")
            elif distance < c.MOVEMENT_SETTINGS["OBSTACLE_DISTANCE"]:
                print("Obstacle detected!")
                movement.stop_all_motors()
                sc.raise_arms(rc.pca)
                time.sleep(0.5)
                sc.move_head_up(rc.pca)
                rgb_led_instance.set_emotion("surprised")
                b.buzzer.play_obstacle_sound()
                time.sleep(0.5)
                sc.move_head_center(rc.pca)
                sc.lower_arms(rc.pca)
                # Turn to a random direction after encountering an obstacle
                if random.choice([True, False]):
                    movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                else:
                    movement.turn_right_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
            elif left_edge == 1:
                print("Left edge detected! Turning right...")
                movement.turn_right_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                rgb_led_instance.set_emotion("angry")
                b.buzzer.play_edge_sound()
            elif right_edge == 1:
                print("Right edge detected! Turning left...")
                movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                rgb_led_instance.set_emotion("angry")
                b.buzzer.play_edge_sound()
            else:
                # Wander around
                if current_time - last_turn > 5:  # Turn every 5 seconds
                    if random.choice([True, False]):
                        movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                    else:
                        movement.turn_right_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"])
                    last_turn = current_time
                else:
                    movement.move_forward(duration=c.MOVEMENT_SETTINGS["MOVE_DURATION"])
                rgb_led_instance.set_emotion("searching")

            time.sleep(0.1)  # Adjust timing as needed

    except KeyboardInterrupt:
        print("Stopping motors and exiting...")
        movement.stop_all_motors()
        rgb_led_instance.set_color(*c.LED_COLORS["OFF"])
        b.buzzer.play_shutdown_sound()

    finally:
        rc.cleanup(rc.pca, rgb_led_instance)