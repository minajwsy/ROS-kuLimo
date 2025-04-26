import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class Service_server(Node):
    pass

def main():
    rclpy.init()
    node = Service_server()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__ == "__main__":
    main()
