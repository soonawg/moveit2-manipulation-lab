# MoveIt2 Manipulation Lab

A ROS 2 (Humble) sandbox for learning and prototyping manipulation with **MoveIt 2**, including:
- Custom URDF/Xacro robot models (e.g., `cobot.urdf.xacro`, `cube_pick_place.urdf.xacro`)  
- Launch pipelines for spawning a robot and opening RViz
- Simple Python scripts for joint motions / trajectories

This repository is intended as a **reproducible manipulation demo** for my robotics portfolio.

## Repository Structure

- `moveit2_manipulation/`
  - `launch/` : RViz / spawn / simulation launch files  
    - `rviz.launch.py` :contentReference[oaicite:3]{index=3}  
    - `spawn_robot.launch.py`, `spawn_robot_w_controller.launch.py`, `start_simulation.launch.py`6}  
  - `urdf/` : robot models (Xacro)
    - `cobot.urdf.xacro`, `cube_pick_place.urdf.xacro` 
  - `config/` : controllers / RViz config
    - `joints_controllers.yaml`, `arm.rviz`
  - `my_manipulation_robot/` : small scripts for joint motion and testing
    - `joint_move.py` and other utilities

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- MoveIt 2 + RViz2
- (If simulation is used) Gazebo / ros2_control stack

