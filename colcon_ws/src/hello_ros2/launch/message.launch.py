from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package="hello_ros2", executable="simple_pub"),
        Node(package="hello_ros2", executable="simple_sub")
        ])