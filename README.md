# Gismo the Robot

Gismo is a feature-packed robot built on a Raspberry Pi. It combines a variety of sensors, motors, and interactive components to create a responsive and engaging robotic experience.

## Features

* **Motor Control:**  Gismo can move forward, backward, and turn using two DC motors.
* **Neck Servo:** A servo motor allows Gismo to turn its "head" and scan its surroundings.
* **Obstacle Avoidance:**  Gismo uses an ultrasonic sensor to detect objects in its path and avoid collisions.
* **Edge Detection:**  Edge sensors prevent Gismo from falling off surfaces.
* **Buzzer Feedback:**  A buzzer plays melodies to indicate different events, such as object detection or edge detection.
* **RGB LED Feedback:**  An RGB LED provides visual cues, changing color based on Gismo's actions.
* **Touch Sensor Interaction:**  Gismo reacts to touch with a shaking motion.
* **IR Distance Sensor:**  An infrared distance sensor helps Gismo avoid obstacles while reversing.
* **Button Control:**  A button triggers debugging actions and sensor tests.
* **Camera Functionality:**  Gismo can take pictures when it detects an object.
* **IR Remote Control:**  Control Gismo's movements with an infrared remote.
* **Sound Sensor:** Gismo can react to sounds in its environment.
* **OLED Display:**  A small OLED screen displays a "face" that changes expression based on Gismo's status (happy or sad).
* **IMU (Inertial Measurement Unit):** An IMU (MPU9250) provides acceleration, gyroscope, and magnetometer data for advanced navigation and orientation sensing.

## Hardware Components

* Raspberry Pi (any model with 40 GPIO pins should work)
* Breadboard
* Jumper wires
* 2x DC Motors with motor driver
* Servo Motor
* Grove Ultrasonic Sensor
* 2x Edge Detection Sensors
* Buzzer
* Touch Sensor
* KY-032 IR Distance Sensor
* Button
* Camera Module (compatible with Raspberry Pi)
* IR Receiver
* RGB LED
* PCA9685 PWM Driver
* OLED Display (SSD1306)
* MPU9250 IMU Sensor
* KY-020 Tilt Sensor
* TS-YM-115 Sound Sensor

## Software Requirements

* Raspberry Pi OS
* Python 3
* RPi.GPIO library
* PIL library
* adafruit_ssd1306 library
* adafruit_pca9685 library
* evdev library
* mpu9250_jmdev library
* libcamera-still (for camera functionality)

## Installation

1. **Clone the repository:** `git clone https://github.com/your-username/gismo-robot.git`
2. **Install the required libraries:** `pip install -r requirements.txt`
3. **Connect the hardware components** according to the wiring diagram (include a diagram in your repository).
4. **Configure the IR receiver:** Find the correct eventX path for your IR receiver using `ls /dev/input/` and update the `device_path` variable in the code.
5. **Run the code:** `python gismo_v1.13.py`

## Usage

* Use the IR remote to control Gismo's movements.
* Press the button to run sensor tests.
* Gismo will automatically avoid obstacles and edges.
* Observe the RGB LED and OLED display for visual feedback.
* Listen to the buzzer for audio cues.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
