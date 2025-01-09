# Project G.I.S.M.O: A Raspberry Pi-Powered Robot

## Overview

**Gismo** is a mobile robot based on the **Raspberry Pi Zero 2 W** and programmed in **Python**. This project showcases various robotics concepts, including autonomous navigation, dead reckoning, sensor integration, and basic mapping.

G.I.S.M.O(https://github.com/user-attachments/assets/ac4136cd-969e-48b8-87b6-a39055fe23aa)
G.I.S.M.O 2(https://github.com/user-attachments/assets/3983ff73-0f72-4326-b768-f5ecdf33131d)

## Features

*   **Movement:**
    *   Continuous forward movement.
    *   Precise turns using the L298N motor driver and PCA9685 PWM controller.
    *   Smooth acceleration and deceleration (ramp-up/ramp-down).
*   **Sensors:**
    *   HC-SR04 ultrasonic sensor for obstacle avoidance.
    *   Edge sensors to prevent falls.
    *   Touch sensor for interaction.
    *   Sound sensor for reacting to sounds.
    *   MPU9250 IMU (accelerometer, gyroscope, magnetometer).
*   **Actuators:**
    *   L298N motor driver to control DC motors.
    *   PCA9685 PWM driver for motor and servo control.
    *   Servos for arm and head movement.
*   **Feedback:**
    *   RGB LED for displaying emotions/status (happy, sad, angry, surprised, searching, neutral).
    *   Buzzer for playing sounds and tunes.
    *   SSD1306 OLED display (Optional) for displaying information.
*   **Dead Reckoning:**
    *   Estimates position (X, Y) and heading using an MPU9250 IMU (accelerometer and gyroscope).
    *   Implements a complementary filter for heading correction (magnetometer integration).
    *   RK4 integration for improved accuracy.
    *   Gyroscope bias calibration.
*   **Mapping (Optional):**
    *   Basic occupancy grid mapping using ultrasonic sensor data.
*   **Wandering:**
    *   Autonomous wandering behavior with obstacle and edge avoidance.
    *   Command interface to interrupt and control the robot.
*   **Command Interface:**
    *   Allows manual control of Gismo's movements and actions through a command-line interface.
    *   `start` and `stop` commands to switch between wandering and command modes.

## Hardware Components

*   **Raspberry Pi Zero 2 W:** The main control board for the robot.
*   **PCA9685:** 16-channel PWM driver for controlling motors and servos.
*   **L298N Motor Driver:** Dual H-bridge motor driver for controlling the DC motors.
*   **MPU9250 IMU:** 9-axis IMU with accelerometer, gyroscope, and magnetometer for dead reckoning.
*   **HC-SR04 Ultrasonic Sensor:** Used for distance measurement and obstacle detection.
*   **Edge Sensors (x2):** Used to detect edges and prevent the robot from falling.
*   **Touch Sensor (TTP223B):** Allows the robot to react to touch.
*   **Sound Sensor (KY-038):** Allows the robot to react to sounds.
*   **RGB LED:** Used for displaying different colors and emotions.
*   **Passive Buzzer:** Used for playing tones and tunes.
*   **Servos (x3):**
    *   2 x 9g servos for the left and right arms.
    *   1 x 9g servo for the head.
*   **Chassis:** https://www.thingiverse.com/thing:4910801
*   **Power Supply:** LiPo battery

## Software

*   **Operating System:** Raspberry Pi OS Lite (or a similar lightweight OS)
*   **Programming Language:** Python 3.x
*   **Libraries:**
    *   `RPi.GPIO` (for GPIO access)
    *   `adafruit-pca9685` (for controlling the PCA9685)
    *   `smbus2` (for I2C communication)
    *   `mpu6050-raspberrypi`
    *   `Pillow (PIL)` (for image manipulation - if you decide to use the display)
    *   `adafruit-circuitpython-ssd1306` (for the OLED display - if you decide to use it again)
    *   `numpy` (for numerical calculations)
    *   `time`
    *   `random`

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone git@github.com:TheGiblet/Project-G.I.S.M.O.git
    cd <Project G.I.S.M.O>
    ```

2.  **Install Dependencies:**

    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Configuration:**

    *   Edit the `config/config.py` file to match your hardware setup:
        *   Set the correct pin numbers for all components.
        *   Set the I2C addresses for the PCA9685 and MPU9250.
        *   Calibrate your servos and update the pulse width ranges in `SERVO_PULSE_WIDTHS`.
        *   Calibrate your magnetometer and update the `MAGNETOMETER_OFFSETS`.
        *   Adjust the `MOVEMENT_SETTINGS` to your preference.

## Usage

1.  **Run the Main Program:**

    ```bash
    python3 src/main.py
    ```

2.  **Wandering Mode:** Gismo will start in autonomous wandering mode by default. It will move forward continuously, avoiding obstacles and edges.

3.  **Command Mode:**
    *   Press **Enter** to enter command mode and stop wandering.
    *   Type commands and press Enter to execute them.
    *   Type `help` to see a list of available commands.
    *   Type `start` to resume wandering mode.
    *   Type `exit` to quit the program.

## Calibration

*   **Gyroscope Calibration:**
    *  The gyroscope is automatically calibrated at startup. Keep the robot still during this process.

*   **Servo Calibration:**
    1.  Run `python3 utils/servo_calibration.py`.
    2.  Follow the on-screen instructions to calibrate each servo.
    3.  Update the `SERVO_PULSE_WIDTHS` values in `config.py`.

## Showcase

[Insert a link to a video of Gismo in action, if you have one]

## Future Improvements

*   **Advanced Sensor Fusion:** Implement a Kalman filter to combine accelerometer, gyroscope, and magnetometer data for more accurate dead reckoning.
*   **Mapping:** Enhance the occupancy grid mapping with more sophisticated algorithms and potentially add visualization.
*   **Path Planning:** Integrate path planning algorithms (e.g., A\*) to enable Gismo to navigate to specific goals.
*   **Enhanced Wandering:** Implement more intelligent wandering behaviors, such as wall following and exploration algorithms.
*   **Object Recognition:** Add a camera and use computer vision techniques to enable object recognition.
*   **Remote Control:** Develop a remote control interface (e.g., web interface, mobile app) for more interactive control.
*   **Voice Control:** Integrate voice recognition to control Gismo with voice commands.

## Contributing

I welcome contributions to the Gismo project! If you're interested in helping out, here are some ways you can contribute:

*   **Report Bugs:** If you find any bugs or issues, please report them on the [Issues](<link to your issues page>) page. Be sure to include as much detail as possible, such as steps to reproduce the bug, error messages, and your operating system/hardware setup.
*   **Suggest Enhancements:** Have ideas for new features or improvements? Feel free to create an issue on the [Issues](<link to your issues page>) page to discuss your suggestions.
*   **Submit Pull Requests:** If you've made code changes that you'd like to contribute, please follow these steps:

    1.  Fork the repository.
    2.  Create a new branch for your feature or bug fix: `git checkout -b feature/my-new-feature` or `git checkout -b bugfix/some-bug`.
    3.  Make your changes and commit them with clear and descriptive commit messages.
    4.  Push your branch to your forked repository: `git push origin feature/my-new-feature`.
    5.  Create a pull request (PR) from your branch to the `main` (or `master`) branch of the main repository.
    6.  Provide a detailed description of your changes in the PR, and reference any related issues.

**Contribution Guidelines:**

*   Please follow the existing code style and conventions.
*   Keep your code well-documented with docstrings and comments.
*   Write clear and concise commit messages.
*   Test your changes thoroughly before submitting a pull request.
*   Be respectful and constructive in discussions.

# Code of Conduct

## Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, sex characteristics, gender identity and expression,
level of experience, education, socio-economic status, nationality, personal
appearance, race, religion, or sexual identity and orientation.

## Our Standards

Examples of behavior that contributes to creating a positive environment
include:

*   Using welcoming and inclusive language
*   Being respectful of differing viewpoints and experiences
*   Gracefully accepting constructive criticism
*   Focusing on what is best for the community
*   Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

*   The use of sexualized language or imagery and unwelcome sexual attention or
    advances
*   Trolling, insulting/derogatory comments, and personal or political attacks
*   Public or private harassment
*   Publishing others' private information, such as a physical or electronic
    address, without explicit permission
*   Other conduct which could reasonably be considered inappropriate in a
    professional setting

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

## Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at [Your Contact Email]. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [https://www.contributor-covenant.org/version/1/4/code-of-conduct.html][v1.4]

[homepage]: https://www.contributor-covenant.org
[v1.4]: https://www.contributor-covenant.org/version/1/4/code-of-conduct.html

**Areas for Contribution:**

Here are some areas where contributions would be particularly helpful:

*   **Dead Reckoning Improvements:**
    *   Implementing sensor fusion (e.g., Kalman filter) to combine accelerometer, gyroscope, and magnetometer data.
    *   Improving the accuracy and robustness of the dead reckoning algorithm.
*   **Mapping:**
    *   Enhancing the occupancy grid mapping algorithm.
    *   Adding visualization of the map (e.g., using `matplotlib` or a web interface).
*   **Path Planning:**
    *   Implementing path planning algorithms (e.g., A\*) to allow Gismo to navigate to specific goals.
*   **Wandering Behavior:**
    *   Developing more sophisticated wandering and exploration algorithms.
    *   Improving stuck detection and recovery.
*   **Object Recognition:**
    *   Integrating a camera and implementing object recognition capabilities.
*   **Remote Control:**
    *   Creating a web interface or mobile app for remote control.
*   **Voice Control:**
    *   Adding voice recognition for voice commands.
*   **Documentation:**
    *   Improving the `README.md` file and adding more detailed documentation.
*   **Bug Fixes:**
    *   Addressing any known issues or bugs.

**Getting Help:**

If you have any questions about contributing, feel free to open an issue on the [Issues][(https://github.com/TheGiblet/Project-G.I.S.M.O/issues)) page.
I appreciate your interest in contributing to Gismo!

## License
Cozmars v2 (open cozmo)
by leodemacondo is licensed under the Creative Commons - Attribution - Non-Commercial - Share Alike license.
