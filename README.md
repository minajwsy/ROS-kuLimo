# kuLimo

---

- limo 수업
  - 1조: 박인규, 정명재, 구찬형, 이현성, 박윤국
  - 2조: 박정우, 차경민, 김학민, 장대진, 이경용
  - 3조: 손건희, 최근호, 양정아, 김지숙, 이승원
  - 4조: 윤형정, 최용규, 이한솔, 맹진수, 정용태

- 파일 다운로드
[링크](https://drive.google.com/file/d/1twlHYAgrWeLSQRO_vHy68lJxr-n1qIWl/view?usp=sharing)

- vscode deb 파일
[링크](https://drive.google.com/file/d/1We4ILpw1NTzpspkflSpvdZikvyApTxn0/view?usp=sharing)

- noetic ros1 컨테이너 만들기
  - docker run -it -d --name ros1_noetic --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --net=host osrf/ros:noetic-desktop-full

```bash
source /opt/ros/noetic/setup.bash # ros를 초기화.
export XDG_RUNTIME_DIR=/run/user/$(id -u)
mkdir -p /run/user/$(id -u)
chmod 700 /run/user/$(id -u)
# rosrun turtlesim turtlesim_node
# rosrun turtlesim turtle_teleop_key
# rqt
# rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]'
```

---

## 파이썬 수업

---

- 수업 일정 (2일)
  - 2025-03-15, 2025-04-05
- 수업 목표
  - VMware 를 이용한 가상환경 운용
  - 리눅스 명령어
  - 파이썬 기초 문법
- [과정 진행 사항](doc/python.md)

---

## ROS1, ROS2 수업

---

- 수업 목표
  - ROS1, ROS2 기초 문법
  - ROS1, ROS2 패키지 만들기
  - ROS1, ROS2 패키지 사용하기
- [과정 진행 사항](doc/ros.md)
