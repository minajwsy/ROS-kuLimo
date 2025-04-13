# kuLimo

---

- freshmea

limo 수업

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

## 2025-03-15

---

- 1교시
  - 교육생분들과 인사
  - 스마트 시티 설명
- 2교시
  - 시험
  - 가상환경 설치 - Vmware 22.04 설치
- 3교시
  - 리눅스 명령어 - mkdir, cd, touch, rm
  - Vscode 설치
- 4교시
  - 파이썬 수업 - type, print, fstring
- 5교시
  - 파이썬 수업 - input
  - 한글 설정
- 6교시
  - 파이썬 수업 - 제어문 if - else
  - 한글 설정
- 7교시
  - 파이썬 수업 - 반복문 for 문, range()
- 8교시
  - 파이썬 수업 - 함수, 함수에서의 인자 설명

---

## 2025-04-05

---

- 1교시
  - 파이썬 - 리스트 수업
- 2교시
  - 리스트 메소드 - 리스트 원소 추가, 삭제, 정렬
- 3교시
  - 파이썬 수업 - 딕션너리
- 4교시
  - 딕션너리 메소드 - 딕션너리 원소 추가, 삭제, 정렬
- 5교시
  - 파이썬 수업 - 클래스 설명
- 6교시
  - 파이썬 수업 - 클래스의 상속
- 7교시
  - 파이썬 수업 - 클래스 변수 및 인스턴스 변수
  - 파이썬 수업 - 클래스 메소드
- 8교시
  - 파이썬 수업 - 모듈과 패키지

---

## 2025-04-12

---

- 1교시
  - ros1 설명
  - docker 설명
- 2교시
  - docker 설치
- 3교시
  - VsCode 에서 docker 사용하기 - dev container, docker extension
  - ros1 컨테이너 만들기 - ros:noetic-desktop-full
- 4교시
  - ubuntu22.04 의 display 설정
  - xhost 설정 : x11 : x org로 실행 및 x11 권한 설정
- 5교시
  - turtlesim 설명
  - ros1 cli 설명
- 6교시
  - ros1 package 만들기 - catkin_make -> hello_ros
  - Twist 메세지 사용 터틀심 움직이기
  - ros1 cli 분석 - rospack, rosnode, rosrun, rostopic
- 7교시
  - ros2 설명
- 8교시
  - ros2 package 만들기 - colcon build -> hello_ros2
