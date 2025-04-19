#! /usr/bin/python3

import rospy
from hello_ros import var_a
from std_msgs.msg import String


class Hello:
    def __init__(self):
        self.pub = rospy.Publisher('message', String, queue_size=10)
        self.data = String()
        rospy.Timer(rospy.Duration(nsecs=330_000_000), self.print_hello)
        self.i=0
        self.rate = rospy.Rate(3)

    def print_hello(self, _event):
        self.data.data = f"hello, ROS! {var_a} noetic {self.i}"
        rospy.loginfo(self.data.data)
        self.pub.publish(self.data)
        self.i += 1


def main():
    rospy.init_node('hello')
    node = Hello()
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
