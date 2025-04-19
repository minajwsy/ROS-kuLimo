#! /usr/bin/python3

import rospy
from std_msgs.msg import String


def main():
    rospy.init_node('hello', anonymous=True)
    pub = rospy.Publisher('message', String, queue_size=10)
    data = String()
    i=0
    rate = rospy.Rate(3)
    while not rospy.is_shutdown():
        data.data = f"hello, ROS! noetic {i}"
        pub.publish(data)
        print("hello, ROS1 noetic!!")
        rate.sleep()
        i += 1

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
