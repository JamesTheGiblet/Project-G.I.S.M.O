import RPi.GPIO as GPIO
import time

# Define GPIO pins for line tracking sensors
left_sensor_pin = 12
#right_sensor_pin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor_pin, GPIO.IN)  # Assuming sensors output HIGH when detecting a line
#GPIO.setup(right_sensor_pin, GPIO.IN)

try:
    while True:
        left_sensor_value = GPIO.input(left_sensor_pin)
        ##right_sensor_value = GPIO.input(right_sensor_pin)

        if left_sensor_value == 0:  # Left sensor detects an edge (no line)
            print("Left edge detected!")
            # Add your code here to react to the left edge (e.g., turn right)

        #if right_sensor_value == 0:  # Right sensor detects an edge (no line)
            #print("Right edge detected!")
            # Add your code here to react to the right edge (e.g., turn left)

        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    GPIO.cleanup()