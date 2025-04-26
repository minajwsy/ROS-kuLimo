# sudo apt update
# sudo apt install git
# git clone https://github.com/freshmea/kuLimo.git


cmake_minimum_required(VERSION 3.0.2)
project(hello_ros)
find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
)

catkin_python_setup()

catkin_package()

catkin_install_python(PROGRAMS
  scripts/hello
  scripts/moveTurtle
  scripts/mtpub
  scripts/mtsub
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY
  launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
