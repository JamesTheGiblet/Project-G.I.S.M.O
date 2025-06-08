# robot_commands.py

import display
from scr import buzzer, dead_reckoning, movement, servo_control


def handle_command(command, pca, rgb_led_instance, movement):
    """Handles commands entered by the user."""
    command = command.lower()
    if command == "forward":
        movement.move_forward()
        display.draw_face_searching()  # Show searching face while moving forward
    elif command == "backward":
        movement.move_backward()
        display.draw_face_sad()  # Show sad face while moving backward
    elif command == "left":
        movement.turn_left_in_place()
        display.draw_face_neutral()  # Show neutral face during turns
    elif command == "right":
        movement.turn_right_in_place()
        display.draw_face_neutral()  # Show neutral face during turns
    elif command == "stop":
        movement.stop_all_motors()
        display.draw_face_neutral()  # Show neutral face when stopped
    elif command == "wiggle":
        # Assuming the wiggle function is defined elsewhere (e.g., in robot_actions.py)
        # You'll need to import it here if that's the case
        wiggle()  # Call the wiggle function
    elif command == "happy":
        rgb_led_instance.set_emotion("happy")
        display.draw_face_happy()
    elif command == "sad":
        rgb_led_instance.set_emotion("sad")
        display.draw_face_sad()
    elif command == "angry":
        rgb_led_instance.set_emotion("angry")
        display.draw_face_angry()
    elif command == "surprised":
        rgb_led_instance.set_emotion("surprised")
        display.draw_face_surprised()
    elif command == "searching":
        rgb_led_instance.set_emotion("searching")
        display.draw_face_searching()
    elif command == "neutral":
        rgb_led_instance.set_emotion("neutral")
        display.draw_face_neutral()
    elif command == "arms up":
        servo_control.raise_arms(pca)
    elif command == "arms down":
        servo_control.lower_arms(pca)
    elif command == "head up":
        servo_control.move_head_up(pca)
    elif command == "head down":
        servo_control.move_head_down(pca)
    elif command == "head center":
        servo_control.move_head_center(pca)
    elif command == "play tune":
        buzzer.play_custom_tune(buzzer.TUNE_IMPERIAL_MARCH)
    elif command == "get position":
        position = dead_reckoning.get_position()
        heading = dead_reckoning.get_heading()
        print(f"Position (X, Y): ({position[0]:.2f}, {position[1]:.2f}), Heading: {heading:.2f} degrees")
        display.draw_text(f"Pos: ({position[0]:.2f}, {position[1]:.2f}), Hdg: {heading:.2f}")
    elif command == "help":
        print("Available commands: forward, backward, left, right, stop, wiggle, happy, sad, angry, surprised, searching, neutral, arms up, arms down, head up, head down, head center, play tune, get position, help, exit, start, stop")
    elif command == "exit":
        raise KeyboardInterrupt
    else:
        print("Invalid command.")


def wiggle(duration=0.5):
    """Makes the robot wiggle for a short duration (assuming this function is defined here)."""
    movement.turn_left_in_place(duration / 2)
    display.draw_face_angry()  # Show angry face while turning left
    movement.turn_right_in_place(duration / 2)
    display.draw_face_neutral()  # Return to neutral face