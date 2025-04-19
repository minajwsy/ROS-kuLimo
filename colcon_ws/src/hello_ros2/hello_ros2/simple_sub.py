import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Simple_sub(Node):
    def __init__(self):
        super().__init__('simple_sub')
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        print(msg.data)


def main():
    rclpy.init()
    node = Simple_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
