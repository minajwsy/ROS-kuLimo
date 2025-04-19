#/turtle1/cmd_vel [geometry_msgs/msg/Twist]
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Simple_pub(Node):
    def __init__(self):
        super().__init__('simple_pub') # node name
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(String, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = String()
        msg.data = f'hello, ros2 {self.count}'
        self.pub.publish(msg)
        self.count += 1


def main():
    rclpy.init()
    node = Simple_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
