# stuck_detection.py
import time
import config as c
import random
import buzzer as b


def handle_stuck_situation(pca, rgb_led_instance, movement, dead_reckoning):
    """Handles the robot's behavior when stuck."""
    global stuck_count, last_position, time_last_moved

    if movement.are_motors_commanded_to_move() and time.time() - time_last_moved > c.MOVEMENT_SETTINGS["STUCK_TIME"]:
        position = dead_reckoning.get_position()
        distance_moved = ((position[0] - last_position[0])**2 + (position[1] - last_position[1])**2)**0.5
        if distance_moved < c.MOVEMENT_SETTINGS["STUCK_DISTANCE"]:
            print("Stuck detected!")
            stuck_count += 1
            if stuck_count >= c.MOVEMENT_SETTINGS["STUCK_THRESHOLD"]:
                print("Stuck multiple times - signaling failure!")
                rgb_led_instance.set_emotion("sad")
                b.buzzer.play_tone(150, 1)  # Long, low tone
                stuck_count = 0  # Reset counter after signaling failure
            else:
                # --- Stuck Recovery Maneuver ---
                movement.stop_all_motors()
                rgb_led_instance.set_emotion("confused")
                b.buzzer.play_tone(200, 0.2)  # Short, higher tone
                movement.move_backward(speed=c.MOVEMENT_SETTINGS["FORWARD_SPEED"], duration=1.0)
                if random.choice([True, False]):
                    movement.turn_left_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"] * 2)
                else:
                    movement.turn_right_in_place(duration=c.MOVEMENT_SETTINGS["TURN_DURATION"] * 2)
                time_last_moved = time.time()  # Reset last moved time after recovery attempt
        else:
            stuck_count = 0  # Reset counter if robot moved significantly
        last_position = position