# Gismo Robot Configuration File

This document centralizes all hardware-related configurations for the Gismo robot, including GPIO pin assignments, PWM channels, and wiring color conventions.

## Table of Contents

- [Wiring Colour Conventions](#wiring-colour-conventions)
- [Component and GPIO Assignments](#component-and-gpio-assignments)

## Wiring Colour Conventions

These conventions provide a standardized "glyph system" for wiring, ensuring consistency and clarity during the build.

    Power: Red (+5V/3.3V) and Black (GND)

    I2C: Yellow (SDA) and Blue (SCL)

    Tilt Sensor: Green (signal)

    LEDs: Green (signal)

    Button: Green (signal)

    Grove Ultrasonic: Green (signal)

    Servos: Orange (signal)

    Buzzer and Sound Sensor: White (signal)

    Touch Sensor: Purple (signal)

    IR Receiver, Reverse Sensor, Edge Sensors: Gray (signal)

## Component and GPIO Assignments

This section maps each component to its pin assignments and power source. For components connected to the PCA9685, the Connection refers to the PWM channel number.
Pi Zero 2W

    Power: Colour: red/black, Connection: pca9685 0, Power Source: PCA2

SSD1306 Display

    SDA: Colour: White, Connection: PCA9685 SDA, Power Source: PCA out

    SCL: Colour: Blue, Connection: PCA9685 SCL, Power Source: PCA out

PCA9685

    SDA: Colour: Yellow, Connection: Pi GPIO 2, Power Source: battery

    SCL: Colour: Blue, Connection: Pi GPIO 3, Power Source: battery

MPU9250

    SDA: Colour: White, Connection: PCA9685 SDA, Power Source: PCA15

    SCL: Colour: Blue, Connection: PCA9685 SCL, Power Source: N/A

Pi Camera Rev 1.3

    Connection: Connects to the CSI port.

9G Servo (left)

    Signal: Connection: PCA9685 Channel 0, Power Source: PCA0

9G Servo (right)

    Signal: Connection: PCA9685 Channel 1, Power Source: PCA1

9G Servo (head)

    Signal: Connection: PCA9685 Channel 14, Power Source: PCA14

KY-016 RGB LED (Red)

    Signal: Colour: Red, Connection: PCA9685 Channel 13, Power Source: PCA13

KY-016 RGB LED (Green)

    Signal: Colour: Green, Connection: PCA9685 Channel 12, Power Source: N/A

KY-016 RGB LED (Blue)

    Signal: Colour: Blue, Connection: PCA9685 Channel 11, Power Source: PCA10

L298N Motor Driver

    Power: Power Source: PCA11

    Int1: Colour: Blue, Connection: PCA9685 Channel 7, Power Source: PCA11

    Int2: Colour: Green, Connection: PCA9685 Channel 8, Power Source: PCA9

    Int3: Colour: White, Connection: PCA9685 Channel 10, Power Source: PCA8

    Int4: Colour: Yellow, Connection: PCA9685 Channel 9, Power Source: PCA7

KY-033 Edge Sensor (right)

    Signal: Colour: Green, Connection: Pi GPIO 12, Power Source: PCA5

KY-033 Edge Sensor (left)

    Signal: Colour: Green, Connection: Pi GPIO 13, Power Source: PCA4

CHQ1838 IR Receiver

    Signal: Colour: Green, Connection: Pi GPIO 16, Power Source: PCA12

TTP223B Touch Sensor

    Signal: Colour: Green, Connection: Pi GPIO 17, Power Source: PCA8

KY-006 Passive Buzzer

    Signal: Colour: White, Connection: Pi GPIO 18, Power Source: PCA6

TS-YM-115 Sound Sensor

    Signal: Colour: White, Connection: Pi GPIO 21, Power Source: PCA9

HCSR04 Ultrasonic Sensor

    Echo: Colour: Green, Connection: Pi GPIO 22, Power Source: PCA7

    Trigger: Colour: Blue, Connection: Pi GPIO 23, Power Source: N/A

TP-4056 USB Charger

    Connection: Connects to LiPo 3.7V, Power Source: PCA3

Switch 999330

    Connection: Connects to LiPo 3.7V, Power Source: N/A

LiPo 3.7V 1100mAh 903042

    Connection: Connects to the TP-4056 USB Charger, Power Source: N/A
