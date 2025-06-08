# Gismo the Robot

Gismo is a feature-packed robot built on a Raspberry Pi. It combines a variety of sensors, motors, and interactive components to create a responsive and engaging robotic experience.

Building G.I.S.M.O has been an incredible experience, one that reflects my approach to problem-solving: dive in, experiment, adapt, and refine. It’s messy, exciting, and immensely rewarding—a true labor of love.

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

## **Technical Architecture**

![Diagram Placeholder](path-to-diagram-image)

The robot’s design integrates key hardware components like the Raspberry Pi, sensors, motor controllers, and a power management unit. The software uses a layered architecture for easier debugging and future enhancements.

### GPIO and Component Assignments

| Component                      | Wire/Signal | Colour   | Connection/Pin             | Power Source    |
|---------------------------------|-------------|----------|----------------------------|-----------------|
| **Raspberry Pi Zero 2W**        | power       | red/black| PCA9685 0                  | PCA2            |
| **SSD1306 Display**             | SDA         | White    | PCA9685 SDA                | PCA out         |
|                                 | SCL         | Blue     | PCA9685 SCL                | PCA out         |
| **PCA9685 PWM Driver**          | SDA         | Yellow   | Pi GPIO 2                  | battery         |
|                                 | SCL         | Blue     | Pi GPIO 3                  | battery         |
| **MPU9250 IMU**                 | SDA         | White    | PCA9685 SDA                | PCA15           |
|                                 | SCL         | Blue     | PCA9685 SCL                | -               |
| **Pi Camera Rev 1.3**           | -           | -        | CSI port                   | -               |
| **9G Servo (left)**             | -           | -        | PCA9685 Channel 0          | PCA0            |
| **9G Servo (right)**            | -           | -        | PCA9685 Channel 1          | PCA1            |
| **9G Servo (head)**             | -           | -        | PCA9685 Channel 14         | PCA14           |
| **KY-016 RGB LED (Red)**        | Red         | Red      | PCA9685 Channel 13         | PCA13           |
| **KY-016 RGB LED (Green)**      | Green       | Green    | PCA9685 Channel 12         | -               |
| **KY-016 RGB LED (Blue)**       | Blue        | Blue     | PCA9685 Channel 11         | PCA10           |
| **L298N Motor Driver (power)**  | -           | -        | -                          | PCA11           |
| **L298N Motor Driver Int1**     | Int1        | Blue     | PCA9685 Channel 7          | PCA11           |
| **L298N Motor Driver Int2**     | Int2        | Green    | PCA9685 Channel 8          | PCA9            |
| **L298N Motor Driver Int3**     | Int3        | White    | PCA9685 Channel 10         | PCA8            |
| **L298N Motor Driver Int4**     | Int4        | Yellow   | PCA9685 Channel 9          | PCA7            |
| **KY-033 Edge Sensor (right)**  | Signal      | Green    | Pi GPIO 12                 | PCA5            |
| **KY-033 Edge Sensor (left)**   | Signal      | Green    | Pi GPIO 13                 | PCA4            |
| **CHQ1838 IR Receiver**         | Signal      | Green    | Pi GPIO 16                 | PCA12           |
| **TTP223B Touch Sensor**        | Signal      | Green    | Pi GPIO 17                 | PCA8            |
| **KY-006 Passive Buzzer**       | Signal      | White    | Pi GPIO 18                 | PCA6            |
| **TS-YM-115 Sound Sensor**      | Signal      | White    | Pi GPIO 21                 | PCA9            |
| **HCSR04 Ultrasonic Echo**      | Echo        | Green    | Pi GPIO 22                 | PCA7            |
| **HCSR04 Ultrasonic Trigger**   | Trigger     | Blue     | Pi GPIO 23                 | -               |
| **TP-4056 USB Charger**         | -           | -        | LiPo 3.7V                  | PCA3            |
| **Switch 999330**               | -           | -        | LiPo 3.7V                  | -               |
| **LiPo 3.7V 1100mAh 903042**    | -           | -        | TP-4056 USB Charger        | -               |

This table summarizes the main components, their wiring, GPIO assignments, and power sources for Gismo.

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

## **Future Enhancements**  
- Integration of advanced sensors (e.g., LIDAR or ToF).  
- Machine learning for object recognition and decision-making.  
- Enhanced navigation algorithms for complex environments.  

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
