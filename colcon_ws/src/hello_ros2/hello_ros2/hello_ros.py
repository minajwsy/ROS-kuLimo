# cd ~/kuLimo/colcon_ws/src
# ros2 pkg create --build-type ament_python hello_ros2
# code ~/.bashrc
# cd colcon_ws/
# colcon build
# source install/local_setup.bash
# ros2 run hello_ros2 hello_ros
# ros2 pkg list | grep hello

import rclpy
from rclpy.node import Node


def print_hello():
    print("hello, ROS2 humble!! ")

def main():
    rclpy.init()
    node = Node('hello')
    node.create_timer(1, print_hello)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
