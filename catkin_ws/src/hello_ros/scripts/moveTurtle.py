#! /usr/bin/python3

import rospy
from geometry_msgs.msg import Twist


def main():
    rospy.init_node('hello', anonymous=True)
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    data = Twist()
    data.angular.z = 3.0
    velocity = 0.0

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        data.linear.x = velocity
        velocity += 0.1
        if velocity > 10:
            velocity = 0
        pub.publish(data)
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
