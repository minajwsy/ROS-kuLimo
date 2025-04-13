# ros2 pkg create --build-type ament_python hello_ros2
# code ~/.bashrc
# cd colcon_ws/
# colcon build
# source install/local_setup.bash 
# ros2 run hello_ros2 hello_ros 
# ros2 pkg list | grep hello
def main():
    print("hello, ROS2 humble!! ")

if __name__== '__main__':
    main()
