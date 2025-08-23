## **Project: G.I.S.M.O.**

A Build Guide for an Autonomous Robot

#### **Disclaimer: Read This First**

This is a hobby project for learning and experimentation. You are building a moving machine with electronics and batteries. If you wire something wrong, you could fry a component or worse.

**This guide is provided as-is.** I'm not responsible for any damage to your hardware, your house, or yourself. By building this, you agree that you're doing it at your own risk. Be smart, be safe, and double-check your wiring.

-----

#### **Table of Contents**

  * [The Big Idea](https://www.google.com/search?q=%23the-big-idea)
  * [What You'll Need](https://www.google.com/search?q=%23what-youll-need)
  * [What's in this Repo](https://www.google.com/search?q=%23whats-in-this-repo)
  * [The First Steps](https://www.google.com/search?q=%23the-first-steps)
  * [Want to Go Further? (The Premium Roadmap)](https://www.google.com/search?q=%23want-to-go-further-the-premium-roadmap)
  * [How to Contribute](https://www.google.com/search?q=%23how-to-contribute)

-----

### **The Big Idea**

The goal of G.I.S.M.O. is to build a simple, two-wheeled robot that can wander around on its own without bumping into things or falling off a table. It's the classic "autonomous wanderer"—a foundational project for anyone who wants to get serious about robotics. It's the physical embodiment of the "build first" philosophy.

-----

### **What You'll Need**

This is an intermediate-level project. You should be comfortable with basic Python scripting, using the command line on a Raspberry Pi, and soldering.

  * **Parts List:** You can find the complete list of components in the `pi zero 2w Components and GPIO Assignments.txt` file. The key parts are a Raspberry Pi Zero 2W, an L298N Motor Driver, an HC-SR04 ultrasonic sensor, and a couple of edge detection sensors.
  * **Tools:** You'll need a soldering iron, solder, breadboard, jumper wires, and basic hand tools.
  * **Code:** This repository contains the basic Python test scripts to get you started.

-----

### **What's in this Repo**

This repo is the **starter kit**. It gives you the foundational code and documentation to get your robot assembled and verify that each component works.

  * `config/config.py`: A central place to define your GPIO pin assignments.
  * `tests/`: A folder full of simple scripts to test individual parts like the motors, sensors, and buzzer. Run these first to make sure your wiring is correct.
  * `lib/`: Reference files, like the Raspberry Pi pinout diagram.

-----

### **The First Steps**

Getting a robot to "live" is a step-by-step process.

1.  **Make It Move:** The first goal is to get the motors calibrated and responding to commands. This involves testing the motor driver and writing a simple script to make the wheels turn.
2.  **Make It See:** Next, you'll wire up the sensors (ultrasonic for obstacles, IR sensors for edge detection) and run the test scripts to make sure it can perceive the world around it.
3.  **Make It Wander:** This is where it comes together. You'll combine the movement logic with the sensor data to create a simple "if-then" loop: "If you see a wall, turn. If you see an edge, back up." This is the core of the autonomous wanderer.

-----

### **Want to Go Further? (The Premium Roadmap)**

The free code in this repository gets you a basic wandering robot. It's a great start, but it's just the beginning.

If you want to unlock G.I.S.M.O.'s full potential and learn advanced robotics concepts, I've created a complete premium roadmap. It includes:

  * **Advanced Navigation Algorithms:** Step-by-step guides on how to implement dead reckoning and build occupancy grid maps.
  * **Complete Schematics & Code:** The full, commented source code and detailed wiring diagrams for every subsystem.
  * **In-Depth Tutorials:** Deep dives into how each component works and how to troubleshoot common problems.

**To get the full premium roadmap, visit my site:**

> **[jamesthegiblet.co.uk](https://jamesthegiblet.co.uk)**

-----

### **How to Contribute**

If you've built your own G.I.S.M.O. and added a cool new feature or improvement, I'd love to see it. Open a pull request with a clear description of what you've changed.

This is where software meets the real world. **The build is the proof.** Let's make something that moves.
