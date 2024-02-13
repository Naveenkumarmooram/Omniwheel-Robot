# Overview
This project focuses on simulating an omni wheel mobile robot for wall following in complex environments using ROS (Robot Operating System) and Gazebo. 

It aims to demonstrate the robot's autonomous navigation capabilities by maintaining a consistent distance from walls, handling dynamic obstacles, and adapting to changing surroundings.

# Features
Utilization of ROS and Gazebo for realistic simulation.

Implementation of a wall following algorithm for autonomous navigation.

Integration of sensor simulation for enhanced environmental interaction.

Detailed simulation of complex environments with dynamic obstacles.

# Prerequisites
ROS Noetic

Gazebo

Python 2.7 or Python 3.5+

Ubuntu 20.04 LTS

# Installation
Install ROS Noetic following the official ROS installation guide.

Install Gazebo using sudo apt-get install gazebo11.

Clone the project repository to your workspace.

# Usage
Set up your ROS environment by sourcing the ROS setup script: source /opt/ros/noetic/setup.bash.

Build the project using catkin_make from the root of your workspace.

Launch the simulation with roslaunch omni_wheel_robot_simulation simulation.launch.

# Simulation Details
The project simulates an omni wheel mobile robot equipped with sensors for wall detection and navigation.

The simulation environment is self-defined and includes various obstacles and wall configurations to test the robot's wall following algorithm.

# Acknowledgments
Guidance and support from Mr. Alunkal Ginu Paul and the Deggendorf Institute of Technology faculty.

ROS and Gazebo communities for the extensive documentation and tutorials.

# Contributing
We welcome contributions! Please submit pull requests or issues on GitHub if you have improvements or suggestions.
