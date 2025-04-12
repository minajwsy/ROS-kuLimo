# cd kuLimo/catkin_ws/
# catkin_make
# source devel/setup.bash
# rosrun hello_ros moveTurtle.py
import rospy
from geometry_msgs.msg import Twist


def main():
    rospy.init_node('hello', anonymous=True)
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    data = Twist()
    data.angular.z = 1.0
    data.linear.x = 2.0

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        pub.publish(data)
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
