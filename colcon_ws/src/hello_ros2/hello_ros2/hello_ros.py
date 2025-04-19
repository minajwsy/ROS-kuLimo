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


class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.create_timer(1, self.print_hello)
        self.count = 0

    def print_hello(self):
        print(f"hello, ROS2 humble!! {self.count}")
        self.count += 1


def main():
    rclpy.init()
    node = Hello()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
