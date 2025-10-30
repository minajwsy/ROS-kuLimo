# 코드 해설 및 실습 방법 설명
_Exported on 2025. 10. 30. at 15시 25분 4초 GMT+9 from Cursor (1.4.5)_

---

**User**

[Code해설] 이 디렉토리는 실제 진행되었던 수업 내용에 대한 기록이야. 이를 분석해서 hello_ros2 폴더의 코드 내용을 해설하고, 실습하는 방법까지 같이 이해하기 쉽게 설명해줘. 수업내용을 제대로 이해하지 못해서  그래

---

**Cursor**

안녕하세요! hello_ros2 폴더의 코드 내용을 자세히 분석해드리겠습니다. 먼저 전체 구조를 파악해보겠습니다.

이제 주요 파일들을 살펴보겠습니다.

좋습니다! **hello_ros2** 패키지의 전체 내용을 체계적으로 설명드리겠습니다. 이 패키지는 ROS2의 핵심 개념들을 단계별로 학습하도록 구성되어 있습니다.

---

# 📚 hello_ros2 패키지 완전 해설

## 🏗️ 1. 패키지 구조

```
hello_ros2/
├── hello_ros2/          # 실제 Python 코드들
├── launch/              # 여러 노드를 함께 실행하는 런치 파일
├── param/               # 파라미터 설정 파일
├── package.xml          # 패키지 메타데이터
└── setup.py             # 패키지 설치 설정
```

---

## 📝 2. ROS2 학습 단계별 코드 해설

### **1단계: 기본 노드 생성** 🎯

#### `hello_ros.py` - 가장 기본적인 ROS2 노드

```python:1:34:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/hello_ros.py
# cd ~/kuLimo/colcon_ws/src
# ros2 pkg create --build-type ament_python hello_ros2
# code ~/.bashrc
# cd colcon_ws/
# colcon build
# source install/local_setup.bash
# ros2 run hello_ros2 hello_ros
# ros2 pkg list | grep hello

import rclpy
from rclpy.node import Node


class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.create_timer(1, self.print_hello)
        self.count = 0

    def print_hello(self):
        print(f"hello, ROS2 humble!! {self.count}")
        self.count += 1


def main():
    rclpy.init()
    node = Hello()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
```

**설명:**
- **Node 클래스 상속**: ROS2의 모든 노드는 `Node` 클래스를 상속받습니다
- **create_timer**: 1초마다 `print_hello` 함수를 호출
- **rclpy.spin**: 노드를 계속 실행시켜 콜백 함수들이 동작하도록 함

**실습 방법:**
```bash
# 패키지 빌드
cd ~/kuLimo/colcon_ws
colcon build --packages-select hello_ros2

# 환경 설정
source install/setup.bash

# 노드 실행
ros2 run hello_ros2 hello_ros
```

---

### **2단계: 토픽 통신 (Publisher/Subscriber)** 📡

#### `simple_pub.py` - 메시지 발행자

```python:1:31:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/simple_pub.py
#/turtle1/cmd_vel [geometry_msgs/msg/Twist]
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Simple_pub(Node):
    def __init__(self):
        super().__init__('simple_pub') # node name
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(String, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = String()
        msg.data = f'hello, ros2 {self.count}'
        self.pub.publish(msg)
        self.count += 1


def main():
    rclpy.init()
    node = Simple_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
```

**설명:**
- **create_publisher(메시지타입, 토픽이름, 큐크기)**: Publisher 생성
- 0.1초마다 "/message" 토픽으로 문자열 메시지 발행

#### `simple_sub.py` - 메시지 구독자

```python:1:25:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/simple_sub.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Simple_sub(Node):
    def __init__(self):
        super().__init__('simple_sub')
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        self.get_logger().info(msg.data)


def main():
    rclpy.init()
    node = Simple_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
```

**설명:**
- **create_subscription(메시지타입, 토픽이름, 콜백함수, 큐크기)**: Subscriber 생성
- 메시지가 도착할 때마다 `sub_callback` 함수가 자동 호출됨

**실습 방법:**
```bash
# 터미널 1: Publisher 실행
ros2 run hello_ros2 simple_pub

# 터미널 2: Subscriber 실행
ros2 run hello_ros2 simple_sub

# 터미널 3: 토픽 확인
ros2 topic list
ros2 topic echo /message
```

---

### **3단계: 서비스 통신 (Client/Server)** 🤝

#### `simple_service_server.py` - 서비스 서버

```python:1:43:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/simple_service_server.py
import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class Service_server(Node):
    def __init__(self):
        super().__init__("service_server")  # 노드 이름
        self.create_service(SetBool, "setBool", self.setBool_callback)
        self.bool = False
        self.cnt = 0

    def setBool_callback(self, request: SetBool.Request, response: SetBool.Response):
        # 서버의 작동 알고리즘...
        self.get_logger().info(f"{self.cnt}번째 요청 처리")
        self.get_logger().info(f"현재 bool 정보 {self.bool}")
        self.get_logger().info(f"변경 요청 값 {request.data}")
        if request.data != self.bool:
            self.bool = not self.bool  # 실제 데이터 변경
            response.success = True
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 성공"
        else:
            response.success = False
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 실패"
        time.sleep(5)
        self.cnt += 1
        return response


def main():
    rclpy.init()
    node = Service_server()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**설명:**
- **create_service(서비스타입, 서비스이름, 콜백함수)**: 서비스 서버 생성
- 클라이언트 요청이 오면 콜백 함수가 실행되고 응답(response)을 리턴
- 5초간 처리 시간이 걸리는 것을 시뮬레이션

#### `simple_service_client.py` - 서비스 클라이언트

```python:13:53:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/simple_service_client.py
class Service_client(Node):
    def __init__(self):
        super().__init__("service_client")  # 노드 이름
        self.client = self.create_client(SetBool, "setBool")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        self.create_timer(1, self.update)
        self.create_timer(2, self.send_request)
        self.bool = False
        self.cnt = 0
        self.request = SetBool.Request()
        self.future = Future()

    def update(self):
        self.get_logger().info("main Thread is running!!")

    def send_request(self):
        self.get_logger().info(f"{self.cnt} 번째 요청")
        self.request.data = not self.request.data
        self.future = self.client.call_async(self.request)  # ros1 대기
        self.future.add_done_callback(self.done_callback)
        self.cnt += 1

    def done_callback(self, future):
        response: SetBool.Response = future.result()
        self.get_logger().info(f"처리 상태: {response.success}")
        self.get_logger().info(f"서버에서 온 메세지: {response.message}")


def main():
    rclpy.init()
    node = Service_client()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**설명:**
- **call_async**: 비동기 방식으로 서비스 호출 (ROS2의 중요한 특징!)
- **add_done_callback**: 응답이 도착하면 콜백 함수 실행
- 메인 스레드가 블로킹되지 않아서 `update` 함수가 계속 실행됨

**실습 방법:**
```bash
# 터미널 1: 서비스 서버 실행
ros2 run hello_ros2 simple_service_server

# 터미널 2: 서비스 클라이언트 실행
ros2 run hello_ros2 simple_service_client

# 터미널 3: 서비스 확인
ros2 service list
ros2 service call /setBool std_srvs/srv/SetBool "{data: true}"
```

---

### **4단계: 액션 (Action)** ⏱️

#### `action_server.py` - 액션 서버

```python:15:59:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/action_server.py
class Action_server(Node):
    def __init__(self):
        super().__init__("fibonacci_server")  # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.action_server = ActionServer(
            self, Fibonacci, "fibonacci", execute_callback=self.execute_callback
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        # goal 을 받았을 때...
        request: Fibonacci.Goal = goal_handle.request
        self.get_logger().info(f"{request.step}")
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [0, 1]
        result = Fibonacci.Result()

        # feedback
        for i in range(1, request.step):
            feedback.temp_seq.append(feedback.temp_seq[i] + feedback.temp_seq[i - 1])
            goal_handle.publish_feedback(feedback)  # 피드백 보내기
            time.sleep(1)

        # result 보내기
        print(type(goal_handle))
        goal_handle.succeed()  # 완료 status 보내기
        # goal_handle.abort()  # aborted 상태로 보내기
        result.seq = feedback.temp_seq
        return result  # action 종료


def main():
    rclpy.init()
    node = Action_server()
    executor = MultiThreadedExecutor(num_threads=5)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**설명:**
- **Action**: 장시간 실행되는 작업에 사용 (서비스 + 피드백)
- **goal**: 목표 (피보나치 수열의 단계 수)
- **feedback**: 진행 상황을 주기적으로 보냄
- **result**: 최종 결과 반환
- **MultiThreadedExecutor**: 멀티스레드로 실행해야 피드백이 제대로 전송됨

#### `action_client.py` - 액션 클라이언트

```python:17:75:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/action_client.py
class Action_client(Node):
    def __init__(self):
        super().__init__("fibonacci_client")  # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.action_client = ActionClient(self, Fibonacci, "fibonacci")
        self.future = Future()  # 메세지가 담길 오브젝트 future
        self.get_result_future = Future()  # 초기화
        # 서버 접속
        while not self.action_client.wait_for_server(
            timeout_sec=1
        ):  # 서버 응답 대기 멈춤!
            self.get_logger().info("피보나치 서버 접속중 ...")
        self.send_goal()

    def send_goal(self):
        goal = Fibonacci.Goal()
        goal.step = 8
        self.future: Future = self.action_client.send_goal_async(
            goal, feedback_callback=self.feedback_callback
        )
        self.future.add_done_callback(self.goal_response_callback)

    # ros1 에 없는 체크 포인트( goal 이 접수 될 때)
    def goal_response_callback(self, future: Future):
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        self.get_result_future: Future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        feedback: Fibonacci.Feedback = msg.feedback
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.temp_seq}")

    # result 를 처리하는 콜백 함수
    def done_callback(self, future: Future):
        result: Fibonacci_GetResult_Response = future.result()  # type : ignore
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f"result: {result.result.seq} 성공!!")
        if result.status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    rclpy.init()
    node = Action_client()
    executor = MultiThreadedExecutor(num_threads=5)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**설명:**
- **send_goal_async**: goal 전송
- **feedback_callback**: 피드백을 받을 때마다 실행
- **goal_response_callback**: goal이 서버에 접수되었는지 확인
- **done_callback**: 최종 결과 처리

**실습 방법:**
```bash
# 터미널 1: 액션 서버 실행
ros2 run hello_ros2 action_server

# 터미널 2: 액션 클라이언트 실행
ros2 run hello_ros2 action_client

# 터미널 3: 액션 확인
ros2 action list
ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 10}"
```

---

### **5단계: 파라미터 (Parameter)** ⚙️

#### `simple_parameter.py` - 파라미터 사용

```python:12:44:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/simple_parameter.py
class Simple_parameter(Node):
    def __init__(self):
        super().__init__("simple_parameter")
        self.create_timer(1, self.update)
        self.declare_parameter("para1", 0)
        self.para1 = self.get_parameter("para1").get_parameter_value().integer_value

        self.add_on_set_parameters_callback(self.parameter_callback)

    def update(self):
        self.get_logger().info(f"parameter : {self.para1}")
        self.para1 += 1
        self.set_parameters([Parameter("para1", Parameter.Type.INTEGER, self.para1)])

    def parameter_callback(self, parameters: list[Parameter]):
        for parameter in parameters:
            if parameter.name == "para1":
                self.para1 = int(parameter.value)  # type: ignore
        return SetParametersResult(successful=True)


def main():
    rclpy.init()
    node = Simple_parameter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**설명:**
- **declare_parameter**: 파라미터 선언 및 기본값 설정
- **get_parameter**: 파라미터 값 가져오기
- **set_parameters**: 파라미터 값 변경
- **add_on_set_parameters_callback**: 외부에서 파라미터 변경 시 콜백 실행

**실습 방법:**
```bash
# 터미널 1: 노드 실행 (초기값 설정)
ros2 run hello_ros2 simple_parameter --ros-args -p para1:=100

# 터미널 2: 파라미터 확인 및 변경
ros2 param list
ros2 param get /simple_parameter para1
ros2 param set /simple_parameter para1 500
```

---

### **6단계: 실전 응용 - Turtlesim 제어** 🐢

#### `move_turtle.py` - 터틀심 움직이기

```python:10:49:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/move_turtle.py
class Move_turtle(Node):
    def __init__(self):
        super().__init__("move_turtle")  # node name
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.declare_parameter("vel", 0.0)
        self.declare_parameter("angle_vel", 1.2)
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        for parameter in parameters:
            if parameter.name == "vel":
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                self.angle_vel = float(parameter.value)  # type: ignore
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        msg = Twist()
        msg.angular.z = self.angle_vel  # python type 캐스팅이 자유롭다.
        msg.linear.x = self.vel  # 하지만 DDS 로 넘길 때는 type check 가 되어야 한다.
        self.pub.publish(msg)
        self.vel += 0.01  # type: ignore


def main():
    rclpy.init()
    node = Move_turtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**설명:**
- **Twist 메시지**: 로봇의 선속도(linear)와 각속도(angular) 제어
- **linear.x**: 전진/후진 속도
- **angular.z**: 회전 속도
- 파라미터로 속도를 실시간 조정 가능

**실습 방법:**
```bash
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: 제어 노드 실행
ros2 run hello_ros2 move_turtle

# 터미널 3: 속도 변경
ros2 param set /move_turtle vel 2.0
ros2 param set /move_turtle angle_vel 3.0
```

---

### **7단계: TF (Transform) - 좌표계 변환** 🌐

#### `follow_turtlesim.py` - 터틀 따라가기

이 코드는 두 개의 거북이를 생성하고, turtle2가 turtle1을 따라가도록 합니다.

**주요 개념:**
- **TF (Transform)**: 로봇의 다양한 좌표계 간의 관계를 표현
- **TransformBroadcaster**: TF 정보 발행
- **TransformListener**: TF 정보 수신
- **lookup_transform**: 두 좌표계 간의 변환 정보 조회

**실습 방법:**
```bash
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: 따라가기 노드 실행
ros2 run hello_ros2 follow_turtlesim

# 터미널 3: turtle1을 키보드로 조종
ros2 run turtlesim turtle_teleop_key

# 터미널 4: TF 트리 확인
ros2 run tf2_tools view_frames

# RViz로 TF 시각화
rviz2
```

---

### **8단계: Launch 파일** 🚀

#### `message.launch.py` - 간단한 런치 파일

```python:1:9:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/launch/message.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package="hello_ros2", executable="simple_pub"),
        Node(package="hello_ros2", executable="simple_sub")
        ])
```

**설명:**
- 여러 노드를 동시에 실행
- Publisher와 Subscriber를 한 번에 시작

#### `moveTurtle.launch.py` - 파라미터 파일 사용

```python:16:39:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/launch/moveTurtle.launch.py
def generate_launch_description():
    param_dir = LaunchConfiguration(
        "param_dir",
        default=os.path.join(
            get_package_share_directory("hello_ros2"), "param", "turtlesim.yaml"
        ),
    )
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "param_dir",
                default_value=param_dir,
                description="turtlesim paramdter dump file",
            ),
            Node(
                package="turtlesim", executable="turtlesim_node", parameters=[param_dir]
            ),
            Node(
                package="hello_ros2", executable="move_turtle", parameters=[param_dir]
            ),
            Node(package="hello_ros2", executable="change_color_client"),
        ]
    )
```

**실습 방법:**
```bash
# 간단한 런치 파일 실행
ros2 launch hello_ros2 message.launch.py

# 파라미터 파일과 함께 실행
ros2 launch hello_ros2 moveTurtle.launch.py

# 다른 파라미터 파일 지정
ros2 launch hello_ros2 moveTurtle.launch.py param_dir:=/path/to/your/params.yaml
```

---

### **9단계: 파라미터 파일** 📋

#### `turtlesim.yaml` - YAML 파라미터 파일

```yaml:1:19:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/param/turtlesim.yaml
/turtlesim:
  ros__parameters:
    background_b: 200
    background_g: 16
    background_r: 10
    qos_overrides:
      /parameter_events:
        publisher:
          depth: 1000
          durability: volatile
          history: keep_last
          reliability: reliable
    use_sim_time: false

/move_turtle:
  ros__parameters:
    vel: 1.0
    angle_vel: 3.0
```

**설명:**
- 여러 노드의 파라미터를 파일로 관리
- `/turtlesim`: turtlesim 배경색 설정
- `/move_turtle`: 속도 파라미터 설정

---

### **10단계: 커스텀 메시지** ✉️

#### `my_topic_pub.py` - 사용자 정의 메시지 사용

```python:8:36:/Users/minajwsy/Documents/kuLimo-PythonC++교육/colcon_ws/src/hello_ros2/hello_ros2/my_topic_pub.py
class Simple_pub(Node):
    def __init__(self):
        super().__init__("myTopicPub")  # node name
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(MyTopic, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = MyTopic()
        msg.a = 10
        msg.b = 20
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f"내가 만든 토픽 입니다.{self.count}"
        self.pub.publish(msg)
        self.count += 1


def main():
    rclpy.init()
    node = Simple_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**MyTopic.msg 정의:**
```msg
std_msgs/Header header
int32 a
int32 b
```

**실습 방법:**
```bash
# user_interface 패키지 먼저 빌드
cd ~/kuLimo/colcon_ws
colcon build --packages-select user_interface

# hello_ros2 패키지 빌드
colcon build --packages-select hello_ros2

# 실행
ros2 run hello_ros2 my_topic_pub
ros2 topic echo /message
```

---

## 🎓 전체 학습 로드맵

1. **기본 노드** → 2. **토픽** → 3. **서비스** → 4. **액션** → 5. **파라미터**
6. **실전 응용 (Turtlesim)** → 7. **TF** → 8. **Launch** → 9. **커스텀 메시지**

---

## 🛠️ 패키지 빌드 및 실행 전체 흐름

```bash
# 1. 작업공간으로 이동
cd ~/kuLimo/colcon_ws

# 2. 패키지 빌드
colcon build --packages-select hello_ros2

# 또는 전체 빌드
colcon build

# 3. 환경 설정 (매번 새 터미널에서 실행 필요)
source install/setup.bash

# 4. 노드 실행
ros2 run hello_ros2 <executable_name>

# 5. Launch 파일 실행
ros2 launch hello_ros2 <launch_file_name>
```

---

## 📌 주요 ROS2 명령어 정리

```bash
# 노드 관련
ros2 node list                    # 실행 중인 노드 목록
ros2 node info /node_name         # 노드 정보 확인

# 토픽 관련
ros2 topic list                   # 토픽 목록
ros2 topic echo /topic_name       # 토픽 메시지 확인
ros2 topic info /topic_name       # 토픽 정보

# 서비스 관련
ros2 service list                 # 서비스 목록
ros2 service call /service_name   # 서비스 호출

# 액션 관련
ros2 action list                  # 액션 목록
ros2 action send_goal /action_name # 액션 goal 전송

# 파라미터 관련
ros2 param list                   # 파라미터 목록
ros2 param get /node_name param   # 파라미터 값 확인
ros2 param set /node_name param value # 파라미터 설정

# TF 관련
ros2 run tf2_tools view_frames    # TF 트리 시각화
ros2 run tf2_ros tf2_echo frame1 frame2 # TF 변환 확인
```

---

## 💡 중요 포인트

1. **ROS1 vs ROS2의 차이**
   - ROS2는 비동기 방식 (call_async, add_done_callback)
   - 멀티스레드 실행기(MultiThreadedExecutor) 사용

2. **콜백 기반 프로그래밍**
   - Timer, Subscription, Service 등은 모두 콜백 함수 사용
   - `rclpy.spin()`으로 콜백 함수들이 실행되도록 유지

3. **파라미터 활용**
   - 런타임에 동적으로 값 변경 가능
   - YAML 파일로 관리하면 편리

4. **Launch 파일의 중요성**
   - 여러 노드를 한 번에 실행
   - 파라미터 파일 로드
   - 복잡한 시스템 구성 간편화

이해가 안 되는 부분이나 더 자세히 알고 싶은 내용이 있으면 말씀해주세요! 😊

```plaintext
hello_ros2/
├── hello_ros2/          # 실제 Python 코드들
├── launch/              # 여러 노드를 함께 실행하는 런치 파일
├── param/               # 파라미터 설정 파일
├── package.xml          # 패키지 메타데이터
└── setup.py             # 패키지 설치 설정
```

```plaintext
# cd ~/kuLimo/colcon_ws/src
# ros2 pkg create --build-type ament_python hello_ros2
# code ~/.bashrc
# cd colcon_ws/
# colcon build
# source install/local_setup.bash
# ros2 run hello_ros2 hello_ros
# ros2 pkg list | grep hello

import rclpy
from rclpy.node import Node


class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.create_timer(1, self.print_hello)
        self.count = 0

    def print_hello(self):
        print(f"hello, ROS2 humble!! {self.count}")
        self.count += 1


def main():
    rclpy.init()
    node = Hello()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
```

```shellscript
# 패키지 빌드
cd ~/kuLimo/colcon_ws
colcon build --packages-select hello_ros2

# 환경 설정
source install/setup.bash

# 노드 실행
ros2 run hello_ros2 hello_ros
```

```plaintext
#/turtle1/cmd_vel [geometry_msgs/msg/Twist]
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Simple_pub(Node):
    def __init__(self):
        super().__init__('simple_pub') # node name
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(String, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = String()
        msg.data = f'hello, ros2 {self.count}'
        self.pub.publish(msg)
        self.count += 1


def main():
    rclpy.init()
    node = Simple_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
```

```plaintext
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Simple_sub(Node):
    def __init__(self):
        super().__init__('simple_sub')
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        self.get_logger().info(msg.data)


def main():
    rclpy.init()
    node = Simple_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__== '__main__':
    main()
```

```shellscript
# 터미널 1: Publisher 실행
ros2 run hello_ros2 simple_pub

# 터미널 2: Subscriber 실행
ros2 run hello_ros2 simple_sub

# 터미널 3: 토픽 확인
ros2 topic list
ros2 topic echo /message
```

```plaintext
import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class Service_server(Node):
    def __init__(self):
        super().__init__("service_server")  # 노드 이름
        self.create_service(SetBool, "setBool", self.setBool_callback)
        self.bool = False
        self.cnt = 0

    def setBool_callback(self, request: SetBool.Request, response: SetBool.Response):
        # 서버의 작동 알고리즘...
        self.get_logger().info(f"{self.cnt}번째 요청 처리")
        self.get_logger().info(f"현재 bool 정보 {self.bool}")
        self.get_logger().info(f"변경 요청 값 {request.data}")
        if request.data != self.bool:
            self.bool = not self.bool  # 실제 데이터 변경
            response.success = True
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 성공"
        else:
            response.success = False
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 실패"
        time.sleep(5)
        self.cnt += 1
        return response


def main():
    rclpy.init()
    node = Service_server()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```plaintext
class Service_client(Node):
    def __init__(self):
        super().__init__("service_client")  # 노드 이름
        self.client = self.create_client(SetBool, "setBool")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        self.create_timer(1, self.update)
        self.create_timer(2, self.send_request)
        self.bool = False
        self.cnt = 0
        self.request = SetBool.Request()
        self.future = Future()

    def update(self):
        self.get_logger().info("main Thread is running!!")

    def send_request(self):
        self.get_logger().info(f"{self.cnt} 번째 요청")
        self.request.data = not self.request.data
        self.future = self.client.call_async(self.request)  # ros1 대기
        self.future.add_done_callback(self.done_callback)
        self.cnt += 1

    def done_callback(self, future):
        response: SetBool.Response = future.result()
        self.get_logger().info(f"처리 상태: {response.success}")
        self.get_logger().info(f"서버에서 온 메세지: {response.message}")


def main():
    rclpy.init()
    node = Service_client()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: 서비스 서버 실행
ros2 run hello_ros2 simple_service_server

# 터미널 2: 서비스 클라이언트 실행
ros2 run hello_ros2 simple_service_client

# 터미널 3: 서비스 확인
ros2 service list
ros2 service call /setBool std_srvs/srv/SetBool "{data: true}"
```

```plaintext
class Action_server(Node):
    def __init__(self):
        super().__init__("fibonacci_server")  # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.action_server = ActionServer(
            self, Fibonacci, "fibonacci", execute_callback=self.execute_callback
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        # goal 을 받았을 때...
        request: Fibonacci.Goal = goal_handle.request
        self.get_logger().info(f"{request.step}")
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [0, 1]
        result = Fibonacci.Result()

        # feedback
        for i in range(1, request.step):
            feedback.temp_seq.append(feedback.temp_seq[i] + feedback.temp_seq[i - 1])
            goal_handle.publish_feedback(feedback)  # 피드백 보내기
            time.sleep(1)

        # result 보내기
        print(type(goal_handle))
        goal_handle.succeed()  # 완료 status 보내기
        # goal_handle.abort()  # aborted 상태로 보내기
        result.seq = feedback.temp_seq
        return result  # action 종료


def main():
    rclpy.init()
    node = Action_server()
    executor = MultiThreadedExecutor(num_threads=5)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```plaintext
class Action_client(Node):
    def __init__(self):
        super().__init__("fibonacci_client")  # 노드 이름
        self.callback_group = ReentrantCallbackGroup()
        self.action_client = ActionClient(self, Fibonacci, "fibonacci")
        self.future = Future()  # 메세지가 담길 오브젝트 future
        self.get_result_future = Future()  # 초기화
        # 서버 접속
        while not self.action_client.wait_for_server(
            timeout_sec=1
        ):  # 서버 응답 대기 멈춤!
            self.get_logger().info("피보나치 서버 접속중 ...")
        self.send_goal()

    def send_goal(self):
        goal = Fibonacci.Goal()
        goal.step = 8
        self.future: Future = self.action_client.send_goal_async(
            goal, feedback_callback=self.feedback_callback
        )
        self.future.add_done_callback(self.goal_response_callback)

    # ros1 에 없는 체크 포인트( goal 이 접수 될 때)
    def goal_response_callback(self, future: Future):
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        self.get_result_future: Future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        feedback: Fibonacci.Feedback = msg.feedback
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.temp_seq}")

    # result 를 처리하는 콜백 함수
    def done_callback(self, future: Future):
        result: Fibonacci_GetResult_Response = future.result()  # type : ignore
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f"result: {result.result.seq} 성공!!")
        if result.status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    rclpy.init()
    node = Action_client()
    executor = MultiThreadedExecutor(num_threads=5)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: 액션 서버 실행
ros2 run hello_ros2 action_server

# 터미널 2: 액션 클라이언트 실행
ros2 run hello_ros2 action_client

# 터미널 3: 액션 확인
ros2 action list
ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 10}"
```

```plaintext
class Simple_parameter(Node):
    def __init__(self):
        super().__init__("simple_parameter")
        self.create_timer(1, self.update)
        self.declare_parameter("para1", 0)
        self.para1 = self.get_parameter("para1").get_parameter_value().integer_value

        self.add_on_set_parameters_callback(self.parameter_callback)

    def update(self):
        self.get_logger().info(f"parameter : {self.para1}")
        self.para1 += 1
        self.set_parameters([Parameter("para1", Parameter.Type.INTEGER, self.para1)])

    def parameter_callback(self, parameters: list[Parameter]):
        for parameter in parameters:
            if parameter.name == "para1":
                self.para1 = int(parameter.value)  # type: ignore
        return SetParametersResult(successful=True)


def main():
    rclpy.init()
    node = Simple_parameter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: 노드 실행 (초기값 설정)
ros2 run hello_ros2 simple_parameter --ros-args -p para1:=100

# 터미널 2: 파라미터 확인 및 변경
ros2 param list
ros2 param get /simple_parameter para1
ros2 param set /simple_parameter para1 500
```

```plaintext
class Move_turtle(Node):
    def __init__(self):
        super().__init__("move_turtle")  # node name
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.declare_parameter("vel", 0.0)
        self.declare_parameter("angle_vel", 1.2)
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        for parameter in parameters:
            if parameter.name == "vel":
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                self.angle_vel = float(parameter.value)  # type: ignore
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        msg = Twist()
        msg.angular.z = self.angle_vel  # python type 캐스팅이 자유롭다.
        msg.linear.x = self.vel  # 하지만 DDS 로 넘길 때는 type check 가 되어야 한다.
        self.pub.publish(msg)
        self.vel += 0.01  # type: ignore


def main():
    rclpy.init()
    node = Move_turtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: 제어 노드 실행
ros2 run hello_ros2 move_turtle

# 터미널 3: 속도 변경
ros2 param set /move_turtle vel 2.0
ros2 param set /move_turtle angle_vel 3.0
```

```shellscript
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: 따라가기 노드 실행
ros2 run hello_ros2 follow_turtlesim

# 터미널 3: turtle1을 키보드로 조종
ros2 run turtlesim turtle_teleop_key

# 터미널 4: TF 트리 확인
ros2 run tf2_tools view_frames

# RViz로 TF 시각화
rviz2
```

```plaintext
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package="hello_ros2", executable="simple_pub"),
        Node(package="hello_ros2", executable="simple_sub")
        ])
```

```plaintext
def generate_launch_description():
    param_dir = LaunchConfiguration(
        "param_dir",
        default=os.path.join(
            get_package_share_directory("hello_ros2"), "param", "turtlesim.yaml"
        ),
    )
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "param_dir",
                default_value=param_dir,
                description="turtlesim paramdter dump file",
            ),
            Node(
                package="turtlesim", executable="turtlesim_node", parameters=[param_dir]
            ),
            Node(
                package="hello_ros2", executable="move_turtle", parameters=[param_dir]
            ),
            Node(package="hello_ros2", executable="change_color_client"),
        ]
    )
```

```shellscript
# 간단한 런치 파일 실행
ros2 launch hello_ros2 message.launch.py

# 파라미터 파일과 함께 실행
ros2 launch hello_ros2 moveTurtle.launch.py

# 다른 파라미터 파일 지정
ros2 launch hello_ros2 moveTurtle.launch.py param_dir:=/path/to/your/params.yaml
```

```plaintext
/turtlesim:
  ros__parameters:
    background_b: 200
    background_g: 16
    background_r: 10
    qos_overrides:
      /parameter_events:
        publisher:
          depth: 1000
          durability: volatile
          history: keep_last
          reliability: reliable
    use_sim_time: false

/move_turtle:
  ros__parameters:
    vel: 1.0
    angle_vel: 3.0
```

```plaintext
class Simple_pub(Node):
    def __init__(self):
        super().__init__("myTopicPub")  # node name
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(MyTopic, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = MyTopic()
        msg.a = 10
        msg.b = 20
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f"내가 만든 토픽 입니다.{self.count}"
        self.pub.publish(msg)
        self.count += 1


def main():
    rclpy.init()
    node = Simple_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```plaintext
std_msgs/Header header
int32 a
int32 b
```

```shellscript
# user_interface 패키지 먼저 빌드
cd ~/kuLimo/colcon_ws
colcon build --packages-select user_interface

# hello_ros2 패키지 빌드
colcon build --packages-select hello_ros2

# 실행
ros2 run hello_ros2 my_topic_pub
ros2 topic echo /message
```

```shellscript
# 1. 작업공간으로 이동
cd ~/kuLimo/colcon_ws

# 2. 패키지 빌드
colcon build --packages-select hello_ros2

# 또는 전체 빌드
colcon build

# 3. 환경 설정 (매번 새 터미널에서 실행 필요)
source install/setup.bash

# 4. 노드 실행
ros2 run hello_ros2 <executable_name>

# 5. Launch 파일 실행
ros2 launch hello_ros2 <launch_file_name>
```

```shellscript
# 노드 관련
ros2 node list                    # 실행 중인 노드 목록
ros2 node info /node_name         # 노드 정보 확인

# 토픽 관련
ros2 topic list                   # 토픽 목록
ros2 topic echo /topic_name       # 토픽 메시지 확인
ros2 topic info /topic_name       # 토픽 정보

# 서비스 관련
ros2 service list                 # 서비스 목록
ros2 service call /service_name   # 서비스 호출

# 액션 관련
ros2 action list                  # 액션 목록
ros2 action send_goal /action_name # 액션 goal 전송

# 파라미터 관련
ros2 param list                   # 파라미터 목록
ros2 param get /node_name param   # 파라미터 값 확인
ros2 param set /node_name param value # 파라미터 설정

# TF 관련
ros2 run tf2_tools view_frames    # TF 트리 시각화
ros2 run tf2_ros tf2_echo frame1 frame2 # TF 변환 확인
```

---

**User**

hello_ros2 폴더의 모든 코드에 이해하기 쉽게 주석을 달아줘

---

**Cursor**

hello_ros2 폴더의 모든 코드 파일에 상세한 주석을 달아드리겠습니다. 먼저 나머지 파일들을 확인하고 모든 파일에 주석을 추가해드리겠습니다.

현재 ask mode이므로 파일을 직접 수정할 수 없습니다. 아래에 모든 파일의 주석이 추가된 버전을 제공해드리겠습니다. 복사해서 사용하시면 됩니다.

---

## 📄 1. hello_ros.py (가장 기본적인 노드)

```python
"""
ROS2 기본 노드 예제
- ROS2 노드의 가장 기본적인 구조를 보여줌
- Timer를 사용한 주기적인 함수 실행
"""

# 패키지 생성 및 실행 방법:
# cd ~/kuLimo/colcon_ws/src
# ros2 pkg create --build-type ament_python hello_ros2
# code ~/.bashrc
# cd colcon_ws/
# colcon build
# source install/local_setup.bash
# ros2 run hello_ros2 hello_ros
# ros2 pkg list | grep hello

import rclpy
from rclpy.node import Node


class Hello(Node):
    """
    가장 기본적인 ROS2 노드 클래스
    1초마다 "hello, ROS2 humble!!" 메시지를 출력
    """
    
    def __init__(self):
        """노드 초기화 함수"""
        # Node 클래스를 상속받아 'hello'라는 이름의 노드 생성
        super().__init__('hello')
        
        # Timer 생성: 1초(1.0)마다 print_hello 함수를 호출
        # 첫 번째 인자: 주기(초 단위)
        # 두 번째 인자: 실행할 콜백 함수
        self.create_timer(1, self.print_hello)
        
        # 카운터 변수 초기화
        self.count = 0

    def print_hello(self):
        """
        Timer에 의해 주기적으로 호출되는 함수
        현재 카운트 값과 함께 hello 메시지 출력
        """
        print(f"hello, ROS2 humble!! {self.count}")
        self.count += 1  # 카운터 증가


def main():
    """
    노드의 메인 함수
    ROS2 초기화, 노드 생성, 실행
    """
    # ROS2 Python 클라이언트 라이브러리 초기화
    rclpy.init()
    
    # Hello 노드 인스턴스 생성
    node = Hello()
    
    try:
        # 노드 실행 (콜백 함수들이 실행되도록 유지)
        # spin()은 노드가 종료될 때까지 계속 실행됨
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Ctrl+C로 종료 시 노드 정리
        node.destroy_node()


if __name__== '__main__':
    main()
```

---

## 📄 2. simple_pub.py (Publisher - 메시지 발행자)

```python
"""
ROS2 Publisher 예제
- 토픽을 통해 메시지를 발행하는 방법
- String 타입의 메시지를 /message 토픽으로 전송
"""

# /turtle1/cmd_vel [geometry_msgs/msg/Twist]
import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 표준 문자열 메시지 타입


class Simple_pub(Node):
    """
    간단한 Publisher 노드
    0.1초마다 /message 토픽으로 문자열 메시지 발행
    """
    
    def __init__(self):
        """Publisher 노드 초기화"""
        # 'simple_pub'이라는 이름의 노드 생성
        super().__init__('simple_pub')
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # 첫 번째 인자: 메시지 타입 (String)
        # 두 번째 인자: 토픽 이름 ("/message")
        # 세 번째 인자: 큐 크기 (10) - 메시지가 밀릴 때 버퍼 크기
        self.pub = self.create_publisher(String, "/message", 10)
        
        # 카운터 초기화
        self.count = 0

    def pub_turtle(self):
        """
        주기적으로 호출되어 메시지를 발행하는 함수
        """
        # String 메시지 객체 생성
        msg = String()
        
        # 메시지 데이터 설정 (f-string으로 카운트 포함)
        msg.data = f'hello, ros2 {self.count}'
        
        # 메시지 발행 (토픽으로 전송)
        self.pub.publish(msg)
        
        # 카운터 증가
        self.count += 1


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Publisher 노드 생성
    node = Simple_pub()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__== '__main__':
    main()
```

---

## 📄 3. simple_sub.py (Subscriber - 메시지 구독자)

```python
"""
ROS2 Subscriber 예제
- 토픽을 통해 메시지를 수신하는 방법
- /message 토픽의 메시지를 구독하여 출력
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 표준 문자열 메시지 타입


class Simple_sub(Node):
    """
    간단한 Subscriber 노드
    /message 토픽에서 메시지를 수신하여 로그로 출력
    """
    
    def __init__(self):
        """Subscriber 노드 초기화"""
        # 'simple_sub'이라는 이름의 노드 생성
        super().__init__('simple_sub')
        
        # Subscriber 생성
        # 첫 번째 인자: 메시지 타입 (String)
        # 두 번째 인자: 토픽 이름 ('message')
        # 세 번째 인자: 콜백 함수 (메시지 수신 시 실행될 함수)
        # 네 번째 인자: 큐 크기 (10)
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        """
        메시지가 도착할 때마다 자동으로 호출되는 콜백 함수
        
        Args:
            msg (String): 수신된 메시지 객체
        """
        # 로거를 통해 수신된 메시지 내용 출력
        # get_logger()는 ROS2의 로깅 시스템 사용
        self.get_logger().info(msg.data)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Subscriber 노드 생성
    node = Simple_sub()
    
    try:
        # 노드 실행 (메시지 수신 대기)
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__== '__main__':
    main()
```

---

## 📄 4. simple_service_server.py (Service Server)

```python
"""
ROS2 Service Server 예제
- 클라이언트의 요청을 받아 처리하고 응답을 반환
- SetBool 서비스를 사용하여 bool 값 변경
"""

import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool  # 표준 Bool 설정 서비스


class Service_server(Node):
    """
    간단한 Service Server 노드
    SetBool 서비스를 제공하여 bool 값을 변경
    """
    
    def __init__(self):
        """Service Server 초기화"""
        # "service_server"라는 이름의 노드 생성
        super().__init__("service_server")
        
        # Service Server 생성
        # 첫 번째 인자: 서비스 타입 (SetBool)
        # 두 번째 인자: 서비스 이름 ("setBool")
        # 세 번째 인자: 콜백 함수 (요청 처리 함수)
        self.create_service(SetBool, "setBool", self.setBool_callback)
        
        # 내부 bool 상태 변수
        self.bool = False
        
        # 요청 카운터
        self.cnt = 0

    def setBool_callback(self, request: SetBool.Request, response: SetBool.Response):
        """
        서비스 요청을 처리하는 콜백 함수
        
        Args:
            request: 클라이언트로부터 받은 요청 (data: bool)
            response: 클라이언트에게 보낼 응답 (success: bool, message: string)
            
        Returns:
            response: 처리 결과가 담긴 응답 객체
        """
        # 서버의 작동 알고리즘
        
        # 로그 출력: 몇 번째 요청인지
        self.get_logger().info(f"{self.cnt}번째 요청 처리")
        
        # 로그 출력: 현재 bool 상태
        self.get_logger().info(f"현재 bool 정보 {self.bool}")
        
        # 로그 출력: 클라이언트가 요청한 값
        self.get_logger().info(f"변경 요청 값 {request.data}")
        
        # 요청 값과 현재 값이 다른 경우 (변경이 필요한 경우)
        if request.data != self.bool:
            self.bool = not self.bool  # 실제 데이터 변경
            response.success = True  # 성공 플래그 설정
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 성공"
        else:
            # 요청 값과 현재 값이 같은 경우 (변경 불필요)
            response.success = False  # 실패 플래그 설정
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 실패"
        
        # 처리 시간 시뮬레이션 (5초 대기)
        time.sleep(5)
        
        # 카운터 증가
        self.cnt += 1
        
        # 응답 반환
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Service Server 노드 생성
    node = Service_server()
    
    try:
        # 노드 실행 (서비스 요청 대기)
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

---

## 📄 5. simple_service_client.py (Service Client)

```python
"""
ROS2 Service Client 예제 (비동기 방식)
- 서비스에 요청을 보내고 비동기로 응답을 받음
- ROS2의 중요한 특징: 비동기 처리로 메인 스레드가 블로킹되지 않음
"""

# 실행 및 비교 방법:
# ros2 run hello_ros2 simple_service_client
# ros2 run hello_ros2 simple_service_server2
# ros2 run hello_ros2 simple_service_server
# 화면의 결과를 비교해 보세요.

from asyncio import Future

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class Service_client(Node):
    """
    비동기 방식의 Service Client 노드
    서비스 요청을 보내는 동안에도 메인 스레드가 계속 실행됨
    """
    
    def __init__(self):
        """Service Client 초기화"""
        # "service_client"라는 이름의 노드 생성
        super().__init__("service_client")
        
        # Service Client 생성
        # 첫 번째 인자: 서비스 타입 (SetBool)
        # 두 번째 인자: 서비스 이름 ("setBool")
        self.client = self.create_client(SetBool, "setBool")
        
        # 서비스 서버가 준비될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        
        # Timer 1: 1초마다 update 함수 실행 (메인 스레드 동작 확인용)
        self.create_timer(1, self.update)
        
        # Timer 2: 2초마다 send_request 함수 실행 (서비스 요청)
        self.create_timer(2, self.send_request)
        
        # 내부 bool 값
        self.bool = False
        
        # 요청 카운터
        self.cnt = 0
        
        # 서비스 요청 객체 생성
        self.request = SetBool.Request()
        
        # Future 객체 (비동기 응답을 받을 객체)
        self.future = Future()

    def update(self):
        """
        메인 스레드가 정상 동작하는지 확인하는 함수
        서비스 요청 중에도 계속 실행되어야 함 (비동기의 장점)
        """
        self.get_logger().info("main Thread is running!!")

    def send_request(self):
        """
        서비스에 요청을 보내는 함수
        비동기 방식으로 요청하므로 응답을 기다리지 않고 즉시 리턴
        """
        self.get_logger().info(f"{self.cnt} 번째 요청")
        
        # 요청 데이터 설정 (bool 값 토글)
        self.request.data = not self.request.data
        
        # 비동기 서비스 호출
        # ROS1에서는 이 부분에서 응답이 올 때까지 대기(블로킹)했음
        # ROS2에서는 call_async로 비동기 처리
        self.future = self.client.call_async(self.request)
        
        # 응답이 도착하면 done_callback 함수가 자동 호출되도록 설정
        self.future.add_done_callback(self.done_callback)
        
        # 카운터 증가
        self.cnt += 1

    def done_callback(self, future):
        """
        서비스 응답이 도착했을 때 자동으로 호출되는 콜백 함수
        
        Args:
            future: 응답이 담긴 Future 객체
        """
        # Future 객체에서 실제 응답 데이터 추출
        response: SetBool.Response = future.result()
        
        # 처리 결과 로그 출력
        self.get_logger().info(f"처리 상태: {response.success}")
        self.get_logger().info(f"서버에서 온 메세지: {response.message}")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Service Client 노드 생성
    node = Service_client()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

---

## 📄 6. simple_service_server2.py (멀티스레드 Service Server)

```python
"""
ROS2 Service Server 예제 (멀티스레드 버전)
- ReentrantCallbackGroup을 사용하여 여러 요청을 동시에 처리 가능
- MultiThreadedExecutor로 멀티스레드 실행
"""

import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup  # 재진입 가능한 콜백 그룹
from rclpy.executors import MultiThreadedExecutor  # 멀티스레드 실행기
from rclpy.node import Node
from std_srvs.srv import SetBool


class Service_server(Node):
    """
    멀티스레드 방식의 Service Server
    여러 클라이언트의 요청을 동시에 처리할 수 있음
    """
    
    def __init__(self):
        """Service Server 초기화"""
        # "service_server"라는 이름의 노드 생성
        super().__init__("service_server")
        
        # ReentrantCallbackGroup 생성
        # 이 그룹의 콜백들은 동시에 실행될 수 있음
        self.callback_group = ReentrantCallbackGroup()
        
        # Service Server 생성 (callback_group 지정)
        self.create_service(
            SetBool,  # 서비스 타입
            "setBool",  # 서비스 이름
            self.setBool_callback,  # 콜백 함수
            callback_group=self.callback_group,  # 콜백 그룹 지정
        )
        
        # 내부 bool 상태
        self.bool = False
        
        # 요청 카운터
        self.cnt = 0

    def setBool_callback(self, request: SetBool.Request, response: SetBool.Response):
        """
        서비스 요청 처리 콜백 (멀티스레드로 동시 실행 가능)
        
        Args:
            request: 클라이언트 요청
            response: 서버 응답
            
        Returns:
            response: 처리된 응답
        """
        # 요청 정보 로그
        self.get_logger().info(f"{self.cnt}번째 요청 처리")
        self.get_logger().info(f"현재 bool 정보 {self.bool}")
        self.get_logger().info(f"변경 요청 값 {request.data}")
        
        # 요청 값과 현재 값 비교
        if request.data != self.bool:
            self.bool = not self.bool  # bool 값 변경
            response.success = True
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 성공"
        else:
            response.success = False
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 실패"
        
        # 처리 시간 시뮬레이션 (5초)
        # 멀티스레드이므로 다른 요청도 동시에 처리 가능
        time.sleep(5)
        
        # 카운터 증가
        self.cnt += 1
        
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Service Server 노드 생성
    node = Service_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    # 최대 5개의 요청을 동시에 처리 가능
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 Executor와 노드 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

---

## 📄 7. action_server.py (Action Server)

```python
"""
ROS2 Action Server 예제
- 장시간 실행되는 작업에 사용 (Service + Feedback)
- 피보나치 수열을 계산하며 중간 과정(feedback)을 전송
"""

# 명령줄로 액션 테스트:
# ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 15 }"

import time

import rclpy
from rclpy.action import ActionServer  # Action Server 클래스
from rclpy.action.server import ServerGoalHandle  # Goal 핸들러
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sympy import fibonacci  # 피보나치 수 계산 (사용되지 않음)
from user_interface.action import Fibonacci  # 커스텀 액션 타입


class Action_server(Node):
    """
    Fibonacci Action Server
    피보나치 수열을 계산하며 진행 상황을 피드백으로 전송
    """
    
    def __init__(self):
        """Action Server 초기화"""
        # "fibonacci_server"라는 이름의 노드 생성
        super().__init__("fibonacci_server")
        
        # ReentrantCallbackGroup 생성 (멀티스레드 처리용)
        self.callback_group = ReentrantCallbackGroup()
        
        # Action Server 생성
        # self: 노드 인스턴스
        # Fibonacci: 액션 타입
        # "fibonacci": 액션 이름
        # execute_callback: goal을 처리하는 함수
        self.action_server = ActionServer(
            self, 
            Fibonacci, 
            "fibonacci", 
            execute_callback=self.execute_callback
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        """
        Action goal을 처리하는 콜백 함수
        
        Args:
            goal_handle: goal 처리를 위한 핸들 객체
            
        Returns:
            result: 최종 결과 (피보나치 수열)
        """
        # goal에서 요청 데이터 추출
        request: Fibonacci.Goal = goal_handle.request
        self.get_logger().info(f"{request.step}")
        
        # Feedback 객체 생성 (중간 진행 상황 전송용)
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [0, 1]  # 피보나치 초기값
        
        # Result 객체 생성 (최종 결과 전송용)
        result = Fibonacci.Result()

        # 피보나치 수열 계산 (feedback 전송)
        for i in range(1, request.step):
            # 다음 피보나치 수 계산
            feedback.temp_seq.append(
                feedback.temp_seq[i] + feedback.temp_seq[i - 1]
            )
            
            # 피드백 발행 (클라이언트에게 중간 결과 전송)
            goal_handle.publish_feedback(feedback)
            
            # 1초 대기 (진행 상황 시뮬레이션)
            time.sleep(1)

        # 작업 완료 상태 설정
        print(type(goal_handle))
        goal_handle.succeed()  # 완료 status 보내기
        # goal_handle.abort()  # aborted 상태로 보내기 (실패 시)
        
        # 최종 결과 설정
        result.seq = feedback.temp_seq
        
        # result 반환 (action 종료)
        return result


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Action Server 노드 생성
    node = Action_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    # 피드백을 보내면서 다른 작업도 처리할 수 있도록
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

---

## 📄 8. action_client.py (Action Client)

```python
"""
ROS2 Action Client 예제
- Action 서버에 goal을 전송하고 피드백과 결과를 받음
- 피보나치 수열 계산을 요청
"""

# 명령줄로 액션 테스트:
# ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 15 }"

import time

import rclpy
from action_msgs.msg import GoalStatus  # Goal 상태 (성공, 실패 등)
from rclpy.action import ActionClient  # Action Client 클래스
from rclpy.action.client import ClientGoalHandle  # Client Goal 핸들러
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.task import Future  # 비동기 작업용 Future
from user_interface.action import Fibonacci  # 커스텀 액션 타입
from user_interface.action._fibonacci import Fibonacci_GetResult_Response


class Action_client(Node):
    """
    Fibonacci Action Client
    피보나치 계산을 요청하고 피드백과 결과를 받음
    """
    
    def __init__(self):
        """Action Client 초기화"""
        # "fibonacci_client"라는 이름의 노드 생성
        super().__init__("fibonacci_client")
        
        # ReentrantCallbackGroup 생성
        self.callback_group = ReentrantCallbackGroup()
        
        # Action Client 생성
        # self: 노드 인스턴스
        # Fibonacci: 액션 타입
        # "fibonacci": 액션 이름
        self.action_client = ActionClient(self, Fibonacci, "fibonacci")
        
        # Future 객체들 초기화
        self.future = Future()  # goal 전송용
        self.get_result_future = Future()  # 결과 수신용
        
        # 서버 접속 대기
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("피보나치 서버 접속중 ...")
        
        # goal 전송
        self.send_goal()

    def send_goal(self):
        """
        Action 서버에 goal을 전송하는 함수
        """
        # Goal 객체 생성
        goal = Fibonacci.Goal()
        goal.step = 8  # 피보나치 8단계 요청
        
        # 비동기로 goal 전송
        # feedback_callback: 피드백 수신 시 호출될 함수
        self.future: Future = self.action_client.send_goal_async(
            goal, 
            feedback_callback=self.feedback_callback
        )
        
        # goal 응답이 도착하면 goal_response_callback 호출
        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future):
        """
        goal이 서버에 접수되었는지 확인하는 콜백
        (ROS1에는 없던 체크 포인트)
        
        Args:
            future: goal 전송 결과가 담긴 Future
        """
        # goal 핸들 추출
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        
        # goal이 거부된 경우
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        
        # goal이 접수된 경우, 결과를 비동기로 요청
        self.get_result_future: Future = goal_handle.get_result_async()
        
        # 결과가 도착하면 done_callback 호출
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        """
        Action 실행 중 피드백이 도착할 때마다 호출되는 콜백
        
        Args:
            msg: 피드백 메시지
        """
        # 피드백에서 데이터 추출
        feedback: Fibonacci.Feedback = msg.feedback
        
        # 지금까지의 계산 결과 출력
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.temp_seq}")

    def done_callback(self, future: Future):
        """
        Action이 완료되었을 때 호출되는 콜백
        최종 결과를 처리
        
        Args:
            future: 결과가 담긴 Future
        """
        # 결과 추출
        result: Fibonacci_GetResult_Response = future.result()  # type : ignore
        
        # 성공 여부에 따라 처리
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            # 성공한 경우
            self.get_logger().info(f"result: {result.result.seq} 성공!!")
        if result.status == GoalStatus.STATUS_ABORTED:
            # 중단된 경우
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Action Client 노드 생성
    node = Action_client()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

---

## 📄 9. simple_parameter.py (Parameter 사용)

```python
"""
ROS2 Parameter 예제
- 런타임에 동적으로 변경 가능한 파라미터 사용
- 외부에서 파라미터 값을 설정하고 변경 가능
"""

# 실행 방법:
# ros2 run hello_ros2 simple_parameter --ros-args -p para1:=True
# ros2 run hello_ros2 simple_parameter
# ros2 param set simple_parameter para1 1000
# ros2 param get simple_parameter para1

import rclpy
from rcl_interfaces.msg import SetParametersResult  # 파라미터 설정 결과
from rclpy.node import Node
from rclpy.parameter import Parameter  # 파라미터 클래스


class Simple_parameter(Node):
    """
    파라미터를 사용하는 간단한 노드
    para1 파라미터를 주기적으로 증가시키며 외부에서도 변경 가능
    """
    
    def __init__(self):
        """파라미터 노드 초기화"""
        # "simple_parameter"라는 이름의 노드 생성
        super().__init__("simple_parameter")
        
        # Timer 생성: 1초마다 update 함수 호출
        self.create_timer(1, self.update)
        
        # 파라미터 선언
        # 첫 번째 인자: 파라미터 이름 ("para1")
        # 두 번째 인자: 기본값 (0)
        self.declare_parameter("para1", 0)
        
        # 파라미터 값 가져오기
        self.para1 = self.get_parameter("para1").get_parameter_value().integer_value

        # 파라미터 변경 콜백 등록
        # 외부에서 파라미터가 변경될 때 호출됨
        self.add_on_set_parameters_callback(self.parameter_callback)

    def update(self):
        """
        주기적으로 호출되는 업데이트 함수
        파라미터 값을 1씩 증가시킴
        """
        # 현재 파라미터 값 출력
        self.get_logger().info(f"parameter : {self.para1}")
        
        # 파라미터 값 증가
        self.para1 += 1
        
        # 변경된 파라미터 값 설정
        # Parameter 객체 생성: (이름, 타입, 값)
        self.set_parameters([
            Parameter("para1", Parameter.Type.INTEGER, self.para1)
        ])

    def parameter_callback(self, parameters: list[Parameter]):
        """
        파라미터가 외부에서 변경될 때 호출되는 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 파라미터 변경 성공 여부
        """
        # 변경된 파라미터들을 순회
        for parameter in parameters:
            # para1 파라미터가 변경된 경우
            if parameter.name == "para1":
                # 내부 변수에 새 값 저장
                self.para1 = int(parameter.value)  # type: ignore
        
        # 변경 성공 반환
        return SetParametersResult(successful=True)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # 파라미터 노드 생성
    node = Simple_parameter()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

---

계속해서 나머지 파일들의 주석을 달아드리겠습니다. 다음 응답에서 계속하겠습니다!

```python
"""
ROS2 기본 노드 예제
- ROS2 노드의 가장 기본적인 구조를 보여줌
- Timer를 사용한 주기적인 함수 실행
"""

# 패키지 생성 및 실행 방법:
# cd ~/kuLimo/colcon_ws/src
# ros2 pkg create --build-type ament_python hello_ros2
# code ~/.bashrc
# cd colcon_ws/
# colcon build
# source install/local_setup.bash
# ros2 run hello_ros2 hello_ros
# ros2 pkg list | grep hello

import rclpy
from rclpy.node import Node


class Hello(Node):
    """
    가장 기본적인 ROS2 노드 클래스
    1초마다 "hello, ROS2 humble!!" 메시지를 출력
    """
    
    def __init__(self):
        """노드 초기화 함수"""
        # Node 클래스를 상속받아 'hello'라는 이름의 노드 생성
        super().__init__('hello')
        
        # Timer 생성: 1초(1.0)마다 print_hello 함수를 호출
        # 첫 번째 인자: 주기(초 단위)
        # 두 번째 인자: 실행할 콜백 함수
        self.create_timer(1, self.print_hello)
        
        # 카운터 변수 초기화
        self.count = 0

    def print_hello(self):
        """
        Timer에 의해 주기적으로 호출되는 함수
        현재 카운트 값과 함께 hello 메시지 출력
        """
        print(f"hello, ROS2 humble!! {self.count}")
        self.count += 1  # 카운터 증가


def main():
    """
    노드의 메인 함수
    ROS2 초기화, 노드 생성, 실행
    """
    # ROS2 Python 클라이언트 라이브러리 초기화
    rclpy.init()
    
    # Hello 노드 인스턴스 생성
    node = Hello()
    
    try:
        # 노드 실행 (콜백 함수들이 실행되도록 유지)
        # spin()은 노드가 종료될 때까지 계속 실행됨
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Ctrl+C로 종료 시 노드 정리
        node.destroy_node()


if __name__== '__main__':
    main()
```

```python
"""
ROS2 Publisher 예제
- 토픽을 통해 메시지를 발행하는 방법
- String 타입의 메시지를 /message 토픽으로 전송
"""

# /turtle1/cmd_vel [geometry_msgs/msg/Twist]
import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 표준 문자열 메시지 타입


class Simple_pub(Node):
    """
    간단한 Publisher 노드
    0.1초마다 /message 토픽으로 문자열 메시지 발행
    """
    
    def __init__(self):
        """Publisher 노드 초기화"""
        # 'simple_pub'이라는 이름의 노드 생성
        super().__init__('simple_pub')
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # 첫 번째 인자: 메시지 타입 (String)
        # 두 번째 인자: 토픽 이름 ("/message")
        # 세 번째 인자: 큐 크기 (10) - 메시지가 밀릴 때 버퍼 크기
        self.pub = self.create_publisher(String, "/message", 10)
        
        # 카운터 초기화
        self.count = 0

    def pub_turtle(self):
        """
        주기적으로 호출되어 메시지를 발행하는 함수
        """
        # String 메시지 객체 생성
        msg = String()
        
        # 메시지 데이터 설정 (f-string으로 카운트 포함)
        msg.data = f'hello, ros2 {self.count}'
        
        # 메시지 발행 (토픽으로 전송)
        self.pub.publish(msg)
        
        # 카운터 증가
        self.count += 1


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Publisher 노드 생성
    node = Simple_pub()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__== '__main__':
    main()
```

```python
"""
ROS2 Subscriber 예제
- 토픽을 통해 메시지를 수신하는 방법
- /message 토픽의 메시지를 구독하여 출력
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 표준 문자열 메시지 타입


class Simple_sub(Node):
    """
    간단한 Subscriber 노드
    /message 토픽에서 메시지를 수신하여 로그로 출력
    """
    
    def __init__(self):
        """Subscriber 노드 초기화"""
        # 'simple_sub'이라는 이름의 노드 생성
        super().__init__('simple_sub')
        
        # Subscriber 생성
        # 첫 번째 인자: 메시지 타입 (String)
        # 두 번째 인자: 토픽 이름 ('message')
        # 세 번째 인자: 콜백 함수 (메시지 수신 시 실행될 함수)
        # 네 번째 인자: 큐 크기 (10)
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        """
        메시지가 도착할 때마다 자동으로 호출되는 콜백 함수
        
        Args:
            msg (String): 수신된 메시지 객체
        """
        # 로거를 통해 수신된 메시지 내용 출력
        # get_logger()는 ROS2의 로깅 시스템 사용
        self.get_logger().info(msg.data)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Subscriber 노드 생성
    node = Simple_sub()
    
    try:
        # 노드 실행 (메시지 수신 대기)
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__== '__main__':
    main()
```

```python
"""
ROS2 Service Server 예제
- 클라이언트의 요청을 받아 처리하고 응답을 반환
- SetBool 서비스를 사용하여 bool 값 변경
"""

import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool  # 표준 Bool 설정 서비스


class Service_server(Node):
    """
    간단한 Service Server 노드
    SetBool 서비스를 제공하여 bool 값을 변경
    """
    
    def __init__(self):
        """Service Server 초기화"""
        # "service_server"라는 이름의 노드 생성
        super().__init__("service_server")
        
        # Service Server 생성
        # 첫 번째 인자: 서비스 타입 (SetBool)
        # 두 번째 인자: 서비스 이름 ("setBool")
        # 세 번째 인자: 콜백 함수 (요청 처리 함수)
        self.create_service(SetBool, "setBool", self.setBool_callback)
        
        # 내부 bool 상태 변수
        self.bool = False
        
        # 요청 카운터
        self.cnt = 0

    def setBool_callback(self, request: SetBool.Request, response: SetBool.Response):
        """
        서비스 요청을 처리하는 콜백 함수
        
        Args:
            request: 클라이언트로부터 받은 요청 (data: bool)
            response: 클라이언트에게 보낼 응답 (success: bool, message: string)
            
        Returns:
            response: 처리 결과가 담긴 응답 객체
        """
        # 서버의 작동 알고리즘
        
        # 로그 출력: 몇 번째 요청인지
        self.get_logger().info(f"{self.cnt}번째 요청 처리")
        
        # 로그 출력: 현재 bool 상태
        self.get_logger().info(f"현재 bool 정보 {self.bool}")
        
        # 로그 출력: 클라이언트가 요청한 값
        self.get_logger().info(f"변경 요청 값 {request.data}")
        
        # 요청 값과 현재 값이 다른 경우 (변경이 필요한 경우)
        if request.data != self.bool:
            self.bool = not self.bool  # 실제 데이터 변경
            response.success = True  # 성공 플래그 설정
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 성공"
        else:
            # 요청 값과 현재 값이 같은 경우 (변경 불필요)
            response.success = False  # 실패 플래그 설정
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 실패"
        
        # 처리 시간 시뮬레이션 (5초 대기)
        time.sleep(5)
        
        # 카운터 증가
        self.cnt += 1
        
        # 응답 반환
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Service Server 노드 생성
    node = Service_server()
    
    try:
        # 노드 실행 (서비스 요청 대기)
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```python
"""
ROS2 Service Client 예제 (비동기 방식)
- 서비스에 요청을 보내고 비동기로 응답을 받음
- ROS2의 중요한 특징: 비동기 처리로 메인 스레드가 블로킹되지 않음
"""

# 실행 및 비교 방법:
# ros2 run hello_ros2 simple_service_client
# ros2 run hello_ros2 simple_service_server2
# ros2 run hello_ros2 simple_service_server
# 화면의 결과를 비교해 보세요.

from asyncio import Future

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class Service_client(Node):
    """
    비동기 방식의 Service Client 노드
    서비스 요청을 보내는 동안에도 메인 스레드가 계속 실행됨
    """
    
    def __init__(self):
        """Service Client 초기화"""
        # "service_client"라는 이름의 노드 생성
        super().__init__("service_client")
        
        # Service Client 생성
        # 첫 번째 인자: 서비스 타입 (SetBool)
        # 두 번째 인자: 서비스 이름 ("setBool")
        self.client = self.create_client(SetBool, "setBool")
        
        # 서비스 서버가 준비될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        
        # Timer 1: 1초마다 update 함수 실행 (메인 스레드 동작 확인용)
        self.create_timer(1, self.update)
        
        # Timer 2: 2초마다 send_request 함수 실행 (서비스 요청)
        self.create_timer(2, self.send_request)
        
        # 내부 bool 값
        self.bool = False
        
        # 요청 카운터
        self.cnt = 0
        
        # 서비스 요청 객체 생성
        self.request = SetBool.Request()
        
        # Future 객체 (비동기 응답을 받을 객체)
        self.future = Future()

    def update(self):
        """
        메인 스레드가 정상 동작하는지 확인하는 함수
        서비스 요청 중에도 계속 실행되어야 함 (비동기의 장점)
        """
        self.get_logger().info("main Thread is running!!")

    def send_request(self):
        """
        서비스에 요청을 보내는 함수
        비동기 방식으로 요청하므로 응답을 기다리지 않고 즉시 리턴
        """
        self.get_logger().info(f"{self.cnt} 번째 요청")
        
        # 요청 데이터 설정 (bool 값 토글)
        self.request.data = not self.request.data
        
        # 비동기 서비스 호출
        # ROS1에서는 이 부분에서 응답이 올 때까지 대기(블로킹)했음
        # ROS2에서는 call_async로 비동기 처리
        self.future = self.client.call_async(self.request)
        
        # 응답이 도착하면 done_callback 함수가 자동 호출되도록 설정
        self.future.add_done_callback(self.done_callback)
        
        # 카운터 증가
        self.cnt += 1

    def done_callback(self, future):
        """
        서비스 응답이 도착했을 때 자동으로 호출되는 콜백 함수
        
        Args:
            future: 응답이 담긴 Future 객체
        """
        # Future 객체에서 실제 응답 데이터 추출
        response: SetBool.Response = future.result()
        
        # 처리 결과 로그 출력
        self.get_logger().info(f"처리 상태: {response.success}")
        self.get_logger().info(f"서버에서 온 메세지: {response.message}")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Service Client 노드 생성
    node = Service_client()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```python
"""
ROS2 Service Server 예제 (멀티스레드 버전)
- ReentrantCallbackGroup을 사용하여 여러 요청을 동시에 처리 가능
- MultiThreadedExecutor로 멀티스레드 실행
"""

import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup  # 재진입 가능한 콜백 그룹
from rclpy.executors import MultiThreadedExecutor  # 멀티스레드 실행기
from rclpy.node import Node
from std_srvs.srv import SetBool


class Service_server(Node):
    """
    멀티스레드 방식의 Service Server
    여러 클라이언트의 요청을 동시에 처리할 수 있음
    """
    
    def __init__(self):
        """Service Server 초기화"""
        # "service_server"라는 이름의 노드 생성
        super().__init__("service_server")
        
        # ReentrantCallbackGroup 생성
        # 이 그룹의 콜백들은 동시에 실행될 수 있음
        self.callback_group = ReentrantCallbackGroup()
        
        # Service Server 생성 (callback_group 지정)
        self.create_service(
            SetBool,  # 서비스 타입
            "setBool",  # 서비스 이름
            self.setBool_callback,  # 콜백 함수
            callback_group=self.callback_group,  # 콜백 그룹 지정
        )
        
        # 내부 bool 상태
        self.bool = False
        
        # 요청 카운터
        self.cnt = 0

    def setBool_callback(self, request: SetBool.Request, response: SetBool.Response):
        """
        서비스 요청 처리 콜백 (멀티스레드로 동시 실행 가능)
        
        Args:
            request: 클라이언트 요청
            response: 서버 응답
            
        Returns:
            response: 처리된 응답
        """
        # 요청 정보 로그
        self.get_logger().info(f"{self.cnt}번째 요청 처리")
        self.get_logger().info(f"현재 bool 정보 {self.bool}")
        self.get_logger().info(f"변경 요청 값 {request.data}")
        
        # 요청 값과 현재 값 비교
        if request.data != self.bool:
            self.bool = not self.bool  # bool 값 변경
            response.success = True
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 성공"
        else:
            response.success = False
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 실패"
        
        # 처리 시간 시뮬레이션 (5초)
        # 멀티스레드이므로 다른 요청도 동시에 처리 가능
        time.sleep(5)
        
        # 카운터 증가
        self.cnt += 1
        
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Service Server 노드 생성
    node = Service_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    # 최대 5개의 요청을 동시에 처리 가능
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 Executor와 노드 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```python
"""
ROS2 Action Server 예제
- 장시간 실행되는 작업에 사용 (Service + Feedback)
- 피보나치 수열을 계산하며 중간 과정(feedback)을 전송
"""

# 명령줄로 액션 테스트:
# ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 15 }"

import time

import rclpy
from rclpy.action import ActionServer  # Action Server 클래스
from rclpy.action.server import ServerGoalHandle  # Goal 핸들러
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sympy import fibonacci  # 피보나치 수 계산 (사용되지 않음)
from user_interface.action import Fibonacci  # 커스텀 액션 타입


class Action_server(Node):
    """
    Fibonacci Action Server
    피보나치 수열을 계산하며 진행 상황을 피드백으로 전송
    """
    
    def __init__(self):
        """Action Server 초기화"""
        # "fibonacci_server"라는 이름의 노드 생성
        super().__init__("fibonacci_server")
        
        # ReentrantCallbackGroup 생성 (멀티스레드 처리용)
        self.callback_group = ReentrantCallbackGroup()
        
        # Action Server 생성
        # self: 노드 인스턴스
        # Fibonacci: 액션 타입
        # "fibonacci": 액션 이름
        # execute_callback: goal을 처리하는 함수
        self.action_server = ActionServer(
            self, 
            Fibonacci, 
            "fibonacci", 
            execute_callback=self.execute_callback
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        """
        Action goal을 처리하는 콜백 함수
        
        Args:
            goal_handle: goal 처리를 위한 핸들 객체
            
        Returns:
            result: 최종 결과 (피보나치 수열)
        """
        # goal에서 요청 데이터 추출
        request: Fibonacci.Goal = goal_handle.request
        self.get_logger().info(f"{request.step}")
        
        # Feedback 객체 생성 (중간 진행 상황 전송용)
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [0, 1]  # 피보나치 초기값
        
        # Result 객체 생성 (최종 결과 전송용)
        result = Fibonacci.Result()

        # 피보나치 수열 계산 (feedback 전송)
        for i in range(1, request.step):
            # 다음 피보나치 수 계산
            feedback.temp_seq.append(
                feedback.temp_seq[i] + feedback.temp_seq[i - 1]
            )
            
            # 피드백 발행 (클라이언트에게 중간 결과 전송)
            goal_handle.publish_feedback(feedback)
            
            # 1초 대기 (진행 상황 시뮬레이션)
            time.sleep(1)

        # 작업 완료 상태 설정
        print(type(goal_handle))
        goal_handle.succeed()  # 완료 status 보내기
        # goal_handle.abort()  # aborted 상태로 보내기 (실패 시)
        
        # 최종 결과 설정
        result.seq = feedback.temp_seq
        
        # result 반환 (action 종료)
        return result


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Action Server 노드 생성
    node = Action_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    # 피드백을 보내면서 다른 작업도 처리할 수 있도록
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```python
"""
ROS2 Action Client 예제
- Action 서버에 goal을 전송하고 피드백과 결과를 받음
- 피보나치 수열 계산을 요청
"""

# 명령줄로 액션 테스트:
# ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 15 }"

import time

import rclpy
from action_msgs.msg import GoalStatus  # Goal 상태 (성공, 실패 등)
from rclpy.action import ActionClient  # Action Client 클래스
from rclpy.action.client import ClientGoalHandle  # Client Goal 핸들러
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.task import Future  # 비동기 작업용 Future
from user_interface.action import Fibonacci  # 커스텀 액션 타입
from user_interface.action._fibonacci import Fibonacci_GetResult_Response


class Action_client(Node):
    """
    Fibonacci Action Client
    피보나치 계산을 요청하고 피드백과 결과를 받음
    """
    
    def __init__(self):
        """Action Client 초기화"""
        # "fibonacci_client"라는 이름의 노드 생성
        super().__init__("fibonacci_client")
        
        # ReentrantCallbackGroup 생성
        self.callback_group = ReentrantCallbackGroup()
        
        # Action Client 생성
        # self: 노드 인스턴스
        # Fibonacci: 액션 타입
        # "fibonacci": 액션 이름
        self.action_client = ActionClient(self, Fibonacci, "fibonacci")
        
        # Future 객체들 초기화
        self.future = Future()  # goal 전송용
        self.get_result_future = Future()  # 결과 수신용
        
        # 서버 접속 대기
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("피보나치 서버 접속중 ...")
        
        # goal 전송
        self.send_goal()

    def send_goal(self):
        """
        Action 서버에 goal을 전송하는 함수
        """
        # Goal 객체 생성
        goal = Fibonacci.Goal()
        goal.step = 8  # 피보나치 8단계 요청
        
        # 비동기로 goal 전송
        # feedback_callback: 피드백 수신 시 호출될 함수
        self.future: Future = self.action_client.send_goal_async(
            goal, 
            feedback_callback=self.feedback_callback
        )
        
        # goal 응답이 도착하면 goal_response_callback 호출
        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future):
        """
        goal이 서버에 접수되었는지 확인하는 콜백
        (ROS1에는 없던 체크 포인트)
        
        Args:
            future: goal 전송 결과가 담긴 Future
        """
        # goal 핸들 추출
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        
        # goal이 거부된 경우
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        
        # goal이 접수된 경우, 결과를 비동기로 요청
        self.get_result_future: Future = goal_handle.get_result_async()
        
        # 결과가 도착하면 done_callback 호출
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        """
        Action 실행 중 피드백이 도착할 때마다 호출되는 콜백
        
        Args:
            msg: 피드백 메시지
        """
        # 피드백에서 데이터 추출
        feedback: Fibonacci.Feedback = msg.feedback
        
        # 지금까지의 계산 결과 출력
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.temp_seq}")

    def done_callback(self, future: Future):
        """
        Action이 완료되었을 때 호출되는 콜백
        최종 결과를 처리
        
        Args:
            future: 결과가 담긴 Future
        """
        # 결과 추출
        result: Fibonacci_GetResult_Response = future.result()  # type : ignore
        
        # 성공 여부에 따라 처리
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            # 성공한 경우
            self.get_logger().info(f"result: {result.result.seq} 성공!!")
        if result.status == GoalStatus.STATUS_ABORTED:
            # 중단된 경우
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Action Client 노드 생성
    node = Action_client()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```python
"""
ROS2 Parameter 예제
- 런타임에 동적으로 변경 가능한 파라미터 사용
- 외부에서 파라미터 값을 설정하고 변경 가능
"""

# 실행 방법:
# ros2 run hello_ros2 simple_parameter --ros-args -p para1:=True
# ros2 run hello_ros2 simple_parameter
# ros2 param set simple_parameter para1 1000
# ros2 param get simple_parameter para1

import rclpy
from rcl_interfaces.msg import SetParametersResult  # 파라미터 설정 결과
from rclpy.node import Node
from rclpy.parameter import Parameter  # 파라미터 클래스


class Simple_parameter(Node):
    """
    파라미터를 사용하는 간단한 노드
    para1 파라미터를 주기적으로 증가시키며 외부에서도 변경 가능
    """
    
    def __init__(self):
        """파라미터 노드 초기화"""
        # "simple_parameter"라는 이름의 노드 생성
        super().__init__("simple_parameter")
        
        # Timer 생성: 1초마다 update 함수 호출
        self.create_timer(1, self.update)
        
        # 파라미터 선언
        # 첫 번째 인자: 파라미터 이름 ("para1")
        # 두 번째 인자: 기본값 (0)
        self.declare_parameter("para1", 0)
        
        # 파라미터 값 가져오기
        self.para1 = self.get_parameter("para1").get_parameter_value().integer_value

        # 파라미터 변경 콜백 등록
        # 외부에서 파라미터가 변경될 때 호출됨
        self.add_on_set_parameters_callback(self.parameter_callback)

    def update(self):
        """
        주기적으로 호출되는 업데이트 함수
        파라미터 값을 1씩 증가시킴
        """
        # 현재 파라미터 값 출력
        self.get_logger().info(f"parameter : {self.para1}")
        
        # 파라미터 값 증가
        self.para1 += 1
        
        # 변경된 파라미터 값 설정
        # Parameter 객체 생성: (이름, 타입, 값)
        self.set_parameters([
            Parameter("para1", Parameter.Type.INTEGER, self.para1)
        ])

    def parameter_callback(self, parameters: list[Parameter]):
        """
        파라미터가 외부에서 변경될 때 호출되는 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 파라미터 변경 성공 여부
        """
        # 변경된 파라미터들을 순회
        for parameter in parameters:
            # para1 파라미터가 변경된 경우
            if parameter.name == "para1":
                # 내부 변수에 새 값 저장
                self.para1 = int(parameter.value)  # type: ignore
        
        # 변경 성공 반환
        return SetParametersResult(successful=True)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # 파라미터 노드 생성
    node = Simple_parameter()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

---

**User**

계속해

---

**Cursor**

계속해서 나머지 파일들의 주석을 달아드리겠습니다!

---

## 📄 10. move_turtle.py (Turtlesim 제어)

```python
"""
ROS2 Turtlesim 제어 예제
- Twist 메시지를 발행하여 터틀을 움직임
- 파라미터로 속도를 동적으로 조정 가능
"""

# /turtle1/cmd_vel [geometry_msgs/msg/Twist]

import rclpy
from geometry_msgs.msg import Twist  # 로봇 속도 명령 메시지
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter


class Move_turtle(Node):
    """
    Turtlesim을 제어하는 노드
    선속도와 각속도를 파라미터로 제어 가능
    """
    
    def __init__(self):
        """Turtlesim 제어 노드 초기화"""
        # "move_turtle"이라는 이름의 노드 생성
        super().__init__("move_turtle")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출 (10Hz)
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # Twist 메시지를 "/turtle1/cmd_vel" 토픽으로 발행
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        
        # 파라미터 선언
        # vel: 선속도 (전진/후진 속도)
        self.declare_parameter("vel", 0.0)
        # angle_vel: 각속도 (회전 속도)
        self.declare_parameter("angle_vel", 1.2)
        
        # 파라미터 값 가져오기
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        # 파라미터 변경 콜백 등록
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        """
        파라미터가 외부에서 변경될 때 호출되는 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 변경 성공 여부
        """
        # 변경된 파라미터들을 순회
        for parameter in parameters:
            if parameter.name == "vel":
                # 선속도 파라미터 업데이트
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                # 각속도 파라미터 업데이트
                self.angle_vel = float(parameter.value)  # type: ignore
        
        # 변경 성공 반환
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        """
        주기적으로 호출되어 터틀에게 속도 명령을 보내는 함수
        """
        # Twist 메시지 생성
        msg = Twist()
        
        # 각속도 설정 (z축 회전 = 평면에서의 회전)
        # python은 type 캐스팅이 자유롭다.
        msg.angular.z = self.angle_vel
        
        # 선속도 설정 (x축 = 전진/후진)
        # 하지만 DDS로 넘길 때는 type check가 되어야 한다.
        msg.linear.x = self.vel
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 선속도를 점진적으로 증가 (가속)
        self.vel += 0.01  # type: ignore


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Turtlesim 제어 노드 생성
    node = Move_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: 제어 노드 실행
ros2 run hello_ros2 move_turtle

# 터미널 3: 파라미터 실시간 변경
ros2 param set /move_turtle vel 2.0
ros2 param set /move_turtle angle_vel 3.0
```

---

## 📄 11. move_limo.py (Limo 로봇 제어)

```python
"""
ROS2 Limo 로봇 제어 예제
- Gazebo 시뮬레이션에서 Limo 로봇을 제어
- move_turtle.py와 유사하지만 /cmd_vel 토픽 사용
"""

# /cmd_vel [geometry_msgs/msg/Twist]
# ros2 launch limo_description gazebo_models_diff.launch.py
# ros2 run hello_ros2 move_limo

import rclpy
from geometry_msgs.msg import Twist  # 로봇 속도 명령 메시지
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter


class Move_turtle(Node):
    """
    Limo 로봇을 제어하는 노드
    실제 로봇이나 Gazebo 시뮬레이션에서 사용
    """
    
    def __init__(self):
        """Limo 제어 노드 초기화"""
        # "move_limo"라는 이름의 노드 생성
        super().__init__("move_limo")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # "/cmd_vel" 토픽으로 Twist 메시지 발행
        # (turtlesim은 /turtle1/cmd_vel, 실제 로봇은 /cmd_vel)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        
        # 파라미터 선언 (기본값 지정)
        self.declare_parameter("vel", 1.0)  # 기본 선속도: 1.0 m/s
        self.declare_parameter("angle_vel", 1.2)  # 기본 각속도: 1.2 rad/s
        
        # 파라미터 값 가져오기
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        # 파라미터 변경 콜백 등록
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        """
        파라미터 변경 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 변경 성공 여부
        """
        for parameter in parameters:
            if parameter.name == "vel":
                # 선속도 업데이트
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                # 각속도 업데이트
                self.angle_vel = float(parameter.value)  # type: ignore
        
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        """
        로봇에게 속도 명령을 보내는 함수
        """
        # Twist 메시지 생성
        msg = Twist()
        
        # 각속도 설정 (회전 속도)
        # python은 type 캐스팅이 자유롭다.
        msg.angular.z = self.angle_vel
        
        # 선속도 설정 (전진/후진 속도)
        # 하지만 DDS로 넘길 때는 type check가 되어야 한다.
        msg.linear.x = self.vel
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 주석 처리됨: 속도를 점진적으로 증가시키지 않음
        # self.vel += 0.01  # type: ignore


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Limo 제어 노드 생성
    node = Move_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: Limo Gazebo 시뮬레이션 실행
ros2 launch limo_description gazebo_models_diff.launch.py

# 터미널 2: Limo 제어 노드 실행
ros2 run hello_ros2 move_limo

# 터미널 3: 속도 조정
ros2 param set /move_limo vel 0.5
ros2 param set /move_limo angle_vel 0.8
```

---

## 📄 12. change_color_client.py (Turtlesim 색상 변경)

```python
"""
ROS2 Service Client 예제 - Turtlesim 펜 색상 변경
- SetPen 서비스를 사용하여 터틀의 궤적 색상을 무작위로 변경
- moveTurtle.launch.py에서 함께 실행됨
"""

# service client를 만드세요. /turtle1/set_pen [turtlesim/srv/SetPen]
# service 이름 타입(turtlesim_node color 변경) 실시간으로 다양한 색상
# launch 파일에 노드 추가 moveTurtle.launch.py

# move_turtle.py -> 파라미터를 설정 각속도 움직임을 외부에서 변화!
# 위 파라미터도 yaml에 넣어서 작동!

import random  # 무작위 색상 생성용
from asyncio import Future

import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen  # Turtlesim 펜 설정 서비스


class Color_client(Node):
    """
    Turtlesim의 펜 색상을 무작위로 변경하는 Service Client
    0.3초마다 RGB 값을 무작위로 생성하여 변경
    """
    
    def __init__(self):
        """Color Client 초기화"""
        # "color_client"라는 이름의 노드 생성
        super().__init__("color_client")
        
        # Service Client 생성
        # SetPen 서비스: 터틀의 펜 설정 (색상, 두께 등)
        # "turtle1/set_pen": 서비스 이름
        self.client = self.create_client(SetPen, "turtle1/set_pen")
        
        # 서비스 서버가 준비될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        
        # Timer 생성: 0.3초마다 update 함수 호출
        # 색상이 빠르게 변경됨
        self.create_timer(0.3, self.update)
        
        # 서비스 요청 객체 생성
        self.request = SetPen.Request()
        
        # Future 객체 (비동기 응답용)
        self.future = Future()

    def update(self):
        """
        주기적으로 호출되어 무작위 RGB 색상을 생성하는 함수
        """
        # RGB 각 채널에 대해 0~255 사이의 무작위 값 생성
        self.request.b = random.randint(0, 255)  # Blue
        self.request.g = random.randint(0, 255)  # Green
        self.request.r = random.randint(0, 255)  # Red
        
        # 서비스 요청 전송
        self.send_request()

    def send_request(self):
        """
        서비스에 색상 변경 요청을 보내는 함수
        """
        # 요청할 RGB 값 로그 출력
        self.get_logger().info(
            f"{self.request.r} {self.request.g} {self.request.b} :RGB 요청"
        )
        
        # 비동기 서비스 호출
        self.future = self.client.call_async(self.request)
        
        # 응답이 도착하면 done_callback 호출
        self.future.add_done_callback(self.done_callback)

    def done_callback(self, future):
        """
        서비스 응답을 처리하는 콜백
        
        Args:
            future: 응답이 담긴 Future 객체
        """
        # 응답 받기 (SetPen 서비스는 빈 응답 반환)
        _ = future.result()
        
        # 처리 완료 로그
        self.get_logger().info("처리 완료!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Color Client 노드 생성
    node = Color_client()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: move_turtle 실행 (터틀을 움직여야 색상 변화를 볼 수 있음)
ros2 run hello_ros2 move_turtle

# 터미널 3: 색상 변경 클라이언트 실행
ros2 run hello_ros2 change_color_client
```

---

## 📄 13. add_server.py (커스텀 서비스 서버)

```python
"""
ROS2 커스텀 Service Server 예제
- user_interface 패키지의 AddTwoInts 서비스 사용
- 두 정수를 더하는 서비스 제공
- 멀티스레드로 동작
"""

import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from user_interface.srv import AddTwoInts  # 커스텀 서비스 타입


class Service_server(Node):
    """
    두 정수를 더하는 서비스를 제공하는 서버
    요청에 포함된 a와 b를 더한 결과를 반환
    """
    
    def __init__(self):
        """Add Service Server 초기화"""
        # "add_service_server"라는 이름의 노드 생성
        super().__init__("add_service_server")
        
        # ReentrantCallbackGroup 생성 (동시 요청 처리용)
        self.callback_group = ReentrantCallbackGroup()
        
        # Service Server 생성
        self.create_service(
            AddTwoInts,  # 서비스 타입
            "add_ints",  # 서비스 이름
            self.setBool_callback,  # 콜백 함수
            callback_group=self.callback_group,  # 콜백 그룹
        )

    def setBool_callback(
        self, request: AddTwoInts.Request, response: AddTwoInts.Response
    ):
        """
        덧셈 서비스 요청을 처리하는 콜백
        
        Args:
            request: 요청 (header, a, b, op)
            response: 응답 (success, result, message)
            
        Returns:
            response: 처리된 응답
        """
        # 서버의 작동 알고리즘
        
        # 요청 시간 로그 출력
        self.get_logger().info(f"{request.header.stamp} 시간")
        
        # 요청 값 로그 출력
        self.get_logger().info(f"a : {request.a}")
        self.get_logger().info(f"b : {request.b}")
        
        # 덧셈 수행
        response.result = request.a + request.b
        
        # 성공 플래그 설정
        response.success = True
        
        # 응답 메시지 설정
        response.message = "a 와 b 의 값을 더해서 반환 했다!"
        
        # 처리 시간 시뮬레이션 (5초 대기)
        time.sleep(5)
        
        # 응답 반환
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Add Service Server 노드 생성
    node = Service_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: 서비스 서버 실행
ros2 run hello_ros2 add_server

# 터미널 2: 서비스 호출 (명령줄)
ros2 service call /add_ints user_interface/srv/AddTwoInts "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''}, a: 10, b: 20, op: '+'}"
```

---

## 📄 14. dynamic_tf.py (동적 TF 브로드캐스터)

```python
"""
ROS2 Dynamic TF Broadcaster 예제
- 동적으로 변화하는 좌표계 변환(Transform) 정보를 발행
- world -> map -> joint 계층 구조 생성
- map 프레임이 world 기준으로 회전
"""

# 사전 설치 필요:
# sudo apt install ros-humble-tf-transformations

import rclpy
import rclpy.logging
from geometry_msgs.msg import TransformStamped  # 좌표 변환 메시지
from rclpy.node import Node
from tf2_ros.transform_broadcaster import TransformBroadcaster  # TF 브로드캐스터
from tf_transformations import quaternion_from_euler  # 오일러각 -> 쿼터니언 변환


class DynamicFramePublisher(Node):
    """
    동적으로 변화하는 TF를 발행하는 노드
    world -> map (회전) -> joint (고정) 구조
    """
    
    def __init__(self):
        """Dynamic TF Publisher 초기화"""
        # "dynamic_tf2_broadcaster"라는 이름의 노드 생성
        super().__init__("dynamic_tf2_broadcaster")
        
        # Timer 생성: 1/30초(약 33ms)마다 pub_cb 호출 (30Hz)
        self.create_timer(1 / 30, self.pub_cb)
        
        # TransformBroadcaster 생성 (TF 발행용)
        self.tf_br = TransformBroadcaster(self)
        
        # 회전 각도 변수 (시간에 따라 증가)
        self.t = 0.0

    def pub_cb(self):
        """
        주기적으로 호출되어 TF를 발행하는 함수
        """
        # === 첫 번째 Transform: world -> map (회전) ===
        t = TransformStamped()
        
        # 헤더 정보 설정
        t.header.stamp = self.get_clock().now().to_msg()  # 현재 시간
        t.header.frame_id = "world"  # 부모 프레임
        t.child_frame_id = "map"  # 자식 프레임
        
        # 위치 설정 (translation)
        t.transform.translation.x = 1.0  # x축으로 1m 이동
        t.transform.translation.y = 1.0  # y축으로 1m 이동
        t.transform.translation.z = 0.0  # z축 이동 없음
        
        # 회전 설정 (rotation)
        # 오일러각(roll, pitch, yaw)을 쿼터니언으로 변환
        quat = quaternion_from_euler(0, 0, self.t)  # z축(yaw) 회전
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        # === 두 번째 Transform: map -> joint (고정) ===
        t2 = TransformStamped()
        
        # 헤더 정보
        t2.header.stamp = self.get_clock().now().to_msg()
        t2.header.frame_id = "map"  # 부모 프레임
        t2.child_frame_id = "joint"  # 자식 프레임
        
        # 위치 설정
        t2.transform.translation.x = 3.0  # x축으로 3m 이동
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = 0.0
        
        # 회전 없음 (identity quaternion)
        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        t2.transform.rotation.w = 1.0

        # 회전 각도 증가 (1/60 라디안씩)
        self.t += 1 / 60
        print(self.t)

        # TF 발행
        self.tf_br.sendTransform(t)  # world -> map
        self.tf_br.sendTransform(t2)  # map -> joint


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Dynamic TF Publisher 노드 생성
    node = DynamicFramePublisher()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: TF 브로드캐스터 실행
ros2 run hello_ros2 dynamic_tf

# 터미널 2: RViz로 TF 시각화
rviz2
# RViz에서 Fixed Frame을 "world"로 설정
# Add -> TF 추가

# 터미널 3: TF 확인
ros2 run tf2_ros tf2_echo world map
ros2 run tf2_ros tf2_echo world joint
```

---

## 📄 15. tf_listener.py (TF 리스너)

```python
"""
ROS2 TF Listener 예제
- TF 정보를 수신하여 좌표계 간의 변환 정보를 확인
- joint 프레임과 world 프레임 간의 상대 위치를 계산
"""

# 사전 설치 필요:
# sudo apt install ros-humble-tf-transformations

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy import time
from rclpy.node import Node
from tf2_ros.buffer import Buffer  # TF 정보를 저장하는 버퍼
from tf2_ros.transform_listener import TransformListener  # TF 수신용

# from tf2_ros import TransformException


class FrameListener(Node):
    """
    TF를 수신하여 좌표 변환 정보를 출력하는 노드
    """
    
    def __init__(self):
        """TF Listener 초기화"""
        # "tf2_listener"라는 이름의 노드 생성
        super().__init__("tf2_listener")
        
        # TF Buffer 생성 (TF 정보를 저장)
        self.tf_buffer = Buffer()
        
        # TransformListener 생성 (TF 수신)
        # tf_buffer에 수신한 TF 정보가 자동으로 저장됨
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Timer 생성: 0.1초마다 on_timer 호출 (10Hz)
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        """
        주기적으로 호출되어 TF 조회를 수행하는 함수
        """
        try:
            # TF 조회 (lookup_transform)
            # 첫 번째 인자: 목표 프레임 (target frame)
            # 두 번째 인자: 소스 프레임 (source frame)
            # 세 번째 인자: 시간 (Time()는 최신 정보)
            # 의미: "world 기준으로 joint의 위치는?"
            t = self.tf_buffer.lookup_transform("joint", "world", time.Time())
        except Exception:
            # TF 조회 실패 시 (아직 TF가 발행되지 않았거나 연결 안 됨)
            self.get_logger().info("lookup 실패!!")
            return
        
        # TF 조회 성공: 위치 정보 출력
        self.get_logger().info(f"{t.transform.translation.x}")
        self.get_logger().info(f"{t.transform.translation.y}")
        self.get_logger().info(f"{t.transform.translation.z}")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # TF Listener 노드 생성
    node = FrameListener()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: TF 브로드캐스터 실행 (TF 정보 발행)
ros2 run hello_ros2 dynamic_tf

# 터미널 2: TF 리스너 실행 (TF 정보 수신)
ros2 run hello_ros2 tf_listener
```

---

계속해서 나머지 파일들도 작성하겠습니다. 다음 응답에서 계속!

```python
"""
ROS2 Turtlesim 제어 예제
- Twist 메시지를 발행하여 터틀을 움직임
- 파라미터로 속도를 동적으로 조정 가능
"""

# /turtle1/cmd_vel [geometry_msgs/msg/Twist]

import rclpy
from geometry_msgs.msg import Twist  # 로봇 속도 명령 메시지
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter


class Move_turtle(Node):
    """
    Turtlesim을 제어하는 노드
    선속도와 각속도를 파라미터로 제어 가능
    """
    
    def __init__(self):
        """Turtlesim 제어 노드 초기화"""
        # "move_turtle"이라는 이름의 노드 생성
        super().__init__("move_turtle")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출 (10Hz)
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # Twist 메시지를 "/turtle1/cmd_vel" 토픽으로 발행
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        
        # 파라미터 선언
        # vel: 선속도 (전진/후진 속도)
        self.declare_parameter("vel", 0.0)
        # angle_vel: 각속도 (회전 속도)
        self.declare_parameter("angle_vel", 1.2)
        
        # 파라미터 값 가져오기
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        # 파라미터 변경 콜백 등록
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        """
        파라미터가 외부에서 변경될 때 호출되는 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 변경 성공 여부
        """
        # 변경된 파라미터들을 순회
        for parameter in parameters:
            if parameter.name == "vel":
                # 선속도 파라미터 업데이트
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                # 각속도 파라미터 업데이트
                self.angle_vel = float(parameter.value)  # type: ignore
        
        # 변경 성공 반환
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        """
        주기적으로 호출되어 터틀에게 속도 명령을 보내는 함수
        """
        # Twist 메시지 생성
        msg = Twist()
        
        # 각속도 설정 (z축 회전 = 평면에서의 회전)
        # python은 type 캐스팅이 자유롭다.
        msg.angular.z = self.angle_vel
        
        # 선속도 설정 (x축 = 전진/후진)
        # 하지만 DDS로 넘길 때는 type check가 되어야 한다.
        msg.linear.x = self.vel
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 선속도를 점진적으로 증가 (가속)
        self.vel += 0.01  # type: ignore


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Turtlesim 제어 노드 생성
    node = Move_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: 제어 노드 실행
ros2 run hello_ros2 move_turtle

# 터미널 3: 파라미터 실시간 변경
ros2 param set /move_turtle vel 2.0
ros2 param set /move_turtle angle_vel 3.0
```

```python
"""
ROS2 Limo 로봇 제어 예제
- Gazebo 시뮬레이션에서 Limo 로봇을 제어
- move_turtle.py와 유사하지만 /cmd_vel 토픽 사용
"""

# /cmd_vel [geometry_msgs/msg/Twist]
# ros2 launch limo_description gazebo_models_diff.launch.py
# ros2 run hello_ros2 move_limo

import rclpy
from geometry_msgs.msg import Twist  # 로봇 속도 명령 메시지
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter


class Move_turtle(Node):
    """
    Limo 로봇을 제어하는 노드
    실제 로봇이나 Gazebo 시뮬레이션에서 사용
    """
    
    def __init__(self):
        """Limo 제어 노드 초기화"""
        # "move_limo"라는 이름의 노드 생성
        super().__init__("move_limo")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # "/cmd_vel" 토픽으로 Twist 메시지 발행
        # (turtlesim은 /turtle1/cmd_vel, 실제 로봇은 /cmd_vel)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        
        # 파라미터 선언 (기본값 지정)
        self.declare_parameter("vel", 1.0)  # 기본 선속도: 1.0 m/s
        self.declare_parameter("angle_vel", 1.2)  # 기본 각속도: 1.2 rad/s
        
        # 파라미터 값 가져오기
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        # 파라미터 변경 콜백 등록
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        """
        파라미터 변경 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 변경 성공 여부
        """
        for parameter in parameters:
            if parameter.name == "vel":
                # 선속도 업데이트
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                # 각속도 업데이트
                self.angle_vel = float(parameter.value)  # type: ignore
        
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        """
        로봇에게 속도 명령을 보내는 함수
        """
        # Twist 메시지 생성
        msg = Twist()
        
        # 각속도 설정 (회전 속도)
        # python은 type 캐스팅이 자유롭다.
        msg.angular.z = self.angle_vel
        
        # 선속도 설정 (전진/후진 속도)
        # 하지만 DDS로 넘길 때는 type check가 되어야 한다.
        msg.linear.x = self.vel
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 주석 처리됨: 속도를 점진적으로 증가시키지 않음
        # self.vel += 0.01  # type: ignore


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Limo 제어 노드 생성
    node = Move_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: Limo Gazebo 시뮬레이션 실행
ros2 launch limo_description gazebo_models_diff.launch.py

# 터미널 2: Limo 제어 노드 실행
ros2 run hello_ros2 move_limo

# 터미널 3: 속도 조정
ros2 param set /move_limo vel 0.5
ros2 param set /move_limo angle_vel 0.8
```

```python
"""
ROS2 Service Client 예제 - Turtlesim 펜 색상 변경
- SetPen 서비스를 사용하여 터틀의 궤적 색상을 무작위로 변경
- moveTurtle.launch.py에서 함께 실행됨
"""

# service client를 만드세요. /turtle1/set_pen [turtlesim/srv/SetPen]
# service 이름 타입(turtlesim_node color 변경) 실시간으로 다양한 색상
# launch 파일에 노드 추가 moveTurtle.launch.py

# move_turtle.py -> 파라미터를 설정 각속도 움직임을 외부에서 변화!
# 위 파라미터도 yaml에 넣어서 작동!

import random  # 무작위 색상 생성용
from asyncio import Future

import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen  # Turtlesim 펜 설정 서비스


class Color_client(Node):
    """
    Turtlesim의 펜 색상을 무작위로 변경하는 Service Client
    0.3초마다 RGB 값을 무작위로 생성하여 변경
    """
    
    def __init__(self):
        """Color Client 초기화"""
        # "color_client"라는 이름의 노드 생성
        super().__init__("color_client")
        
        # Service Client 생성
        # SetPen 서비스: 터틀의 펜 설정 (색상, 두께 등)
        # "turtle1/set_pen": 서비스 이름
        self.client = self.create_client(SetPen, "turtle1/set_pen")
        
        # 서비스 서버가 준비될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        
        # Timer 생성: 0.3초마다 update 함수 호출
        # 색상이 빠르게 변경됨
        self.create_timer(0.3, self.update)
        
        # 서비스 요청 객체 생성
        self.request = SetPen.Request()
        
        # Future 객체 (비동기 응답용)
        self.future = Future()

    def update(self):
        """
        주기적으로 호출되어 무작위 RGB 색상을 생성하는 함수
        """
        # RGB 각 채널에 대해 0~255 사이의 무작위 값 생성
        self.request.b = random.randint(0, 255)  # Blue
        self.request.g = random.randint(0, 255)  # Green
        self.request.r = random.randint(0, 255)  # Red
        
        # 서비스 요청 전송
        self.send_request()

    def send_request(self):
        """
        서비스에 색상 변경 요청을 보내는 함수
        """
        # 요청할 RGB 값 로그 출력
        self.get_logger().info(
            f"{self.request.r} {self.request.g} {self.request.b} :RGB 요청"
        )
        
        # 비동기 서비스 호출
        self.future = self.client.call_async(self.request)
        
        # 응답이 도착하면 done_callback 호출
        self.future.add_done_callback(self.done_callback)

    def done_callback(self, future):
        """
        서비스 응답을 처리하는 콜백
        
        Args:
            future: 응답이 담긴 Future 객체
        """
        # 응답 받기 (SetPen 서비스는 빈 응답 반환)
        _ = future.result()
        
        # 처리 완료 로그
        self.get_logger().info("처리 완료!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Color Client 노드 생성
    node = Color_client()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: move_turtle 실행 (터틀을 움직여야 색상 변화를 볼 수 있음)
ros2 run hello_ros2 move_turtle

# 터미널 3: 색상 변경 클라이언트 실행
ros2 run hello_ros2 change_color_client
```

```python
"""
ROS2 커스텀 Service Server 예제
- user_interface 패키지의 AddTwoInts 서비스 사용
- 두 정수를 더하는 서비스 제공
- 멀티스레드로 동작
"""

import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from user_interface.srv import AddTwoInts  # 커스텀 서비스 타입


class Service_server(Node):
    """
    두 정수를 더하는 서비스를 제공하는 서버
    요청에 포함된 a와 b를 더한 결과를 반환
    """
    
    def __init__(self):
        """Add Service Server 초기화"""
        # "add_service_server"라는 이름의 노드 생성
        super().__init__("add_service_server")
        
        # ReentrantCallbackGroup 생성 (동시 요청 처리용)
        self.callback_group = ReentrantCallbackGroup()
        
        # Service Server 생성
        self.create_service(
            AddTwoInts,  # 서비스 타입
            "add_ints",  # 서비스 이름
            self.setBool_callback,  # 콜백 함수
            callback_group=self.callback_group,  # 콜백 그룹
        )

    def setBool_callback(
        self, request: AddTwoInts.Request, response: AddTwoInts.Response
    ):
        """
        덧셈 서비스 요청을 처리하는 콜백
        
        Args:
            request: 요청 (header, a, b, op)
            response: 응답 (success, result, message)
            
        Returns:
            response: 처리된 응답
        """
        # 서버의 작동 알고리즘
        
        # 요청 시간 로그 출력
        self.get_logger().info(f"{request.header.stamp} 시간")
        
        # 요청 값 로그 출력
        self.get_logger().info(f"a : {request.a}")
        self.get_logger().info(f"b : {request.b}")
        
        # 덧셈 수행
        response.result = request.a + request.b
        
        # 성공 플래그 설정
        response.success = True
        
        # 응답 메시지 설정
        response.message = "a 와 b 의 값을 더해서 반환 했다!"
        
        # 처리 시간 시뮬레이션 (5초 대기)
        time.sleep(5)
        
        # 응답 반환
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Add Service Server 노드 생성
    node = Service_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: 서비스 서버 실행
ros2 run hello_ros2 add_server

# 터미널 2: 서비스 호출 (명령줄)
ros2 service call /add_ints user_interface/srv/AddTwoInts "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''}, a: 10, b: 20, op: '+'}"
```

```python
"""
ROS2 Dynamic TF Broadcaster 예제
- 동적으로 변화하는 좌표계 변환(Transform) 정보를 발행
- world -> map -> joint 계층 구조 생성
- map 프레임이 world 기준으로 회전
"""

# 사전 설치 필요:
# sudo apt install ros-humble-tf-transformations

import rclpy
import rclpy.logging
from geometry_msgs.msg import TransformStamped  # 좌표 변환 메시지
from rclpy.node import Node
from tf2_ros.transform_broadcaster import TransformBroadcaster  # TF 브로드캐스터
from tf_transformations import quaternion_from_euler  # 오일러각 -> 쿼터니언 변환


class DynamicFramePublisher(Node):
    """
    동적으로 변화하는 TF를 발행하는 노드
    world -> map (회전) -> joint (고정) 구조
    """
    
    def __init__(self):
        """Dynamic TF Publisher 초기화"""
        # "dynamic_tf2_broadcaster"라는 이름의 노드 생성
        super().__init__("dynamic_tf2_broadcaster")
        
        # Timer 생성: 1/30초(약 33ms)마다 pub_cb 호출 (30Hz)
        self.create_timer(1 / 30, self.pub_cb)
        
        # TransformBroadcaster 생성 (TF 발행용)
        self.tf_br = TransformBroadcaster(self)
        
        # 회전 각도 변수 (시간에 따라 증가)
        self.t = 0.0

    def pub_cb(self):
        """
        주기적으로 호출되어 TF를 발행하는 함수
        """
        # === 첫 번째 Transform: world -> map (회전) ===
        t = TransformStamped()
        
        # 헤더 정보 설정
        t.header.stamp = self.get_clock().now().to_msg()  # 현재 시간
        t.header.frame_id = "world"  # 부모 프레임
        t.child_frame_id = "map"  # 자식 프레임
        
        # 위치 설정 (translation)
        t.transform.translation.x = 1.0  # x축으로 1m 이동
        t.transform.translation.y = 1.0  # y축으로 1m 이동
        t.transform.translation.z = 0.0  # z축 이동 없음
        
        # 회전 설정 (rotation)
        # 오일러각(roll, pitch, yaw)을 쿼터니언으로 변환
        quat = quaternion_from_euler(0, 0, self.t)  # z축(yaw) 회전
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        # === 두 번째 Transform: map -> joint (고정) ===
        t2 = TransformStamped()
        
        # 헤더 정보
        t2.header.stamp = self.get_clock().now().to_msg()
        t2.header.frame_id = "map"  # 부모 프레임
        t2.child_frame_id = "joint"  # 자식 프레임
        
        # 위치 설정
        t2.transform.translation.x = 3.0  # x축으로 3m 이동
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = 0.0
        
        # 회전 없음 (identity quaternion)
        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        t2.transform.rotation.w = 1.0

        # 회전 각도 증가 (1/60 라디안씩)
        self.t += 1 / 60
        print(self.t)

        # TF 발행
        self.tf_br.sendTransform(t)  # world -> map
        self.tf_br.sendTransform(t2)  # map -> joint


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Dynamic TF Publisher 노드 생성
    node = DynamicFramePublisher()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: TF 브로드캐스터 실행
ros2 run hello_ros2 dynamic_tf

# 터미널 2: RViz로 TF 시각화
rviz2
# RViz에서 Fixed Frame을 "world"로 설정
# Add -> TF 추가

# 터미널 3: TF 확인
ros2 run tf2_ros tf2_echo world map
ros2 run tf2_ros tf2_echo world joint
```

```python
"""
ROS2 TF Listener 예제
- TF 정보를 수신하여 좌표계 간의 변환 정보를 확인
- joint 프레임과 world 프레임 간의 상대 위치를 계산
"""

# 사전 설치 필요:
# sudo apt install ros-humble-tf-transformations

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy import time
from rclpy.node import Node
from tf2_ros.buffer import Buffer  # TF 정보를 저장하는 버퍼
from tf2_ros.transform_listener import TransformListener  # TF 수신용

# from tf2_ros import TransformException


class FrameListener(Node):
    """
    TF를 수신하여 좌표 변환 정보를 출력하는 노드
    """
    
    def __init__(self):
        """TF Listener 초기화"""
        # "tf2_listener"라는 이름의 노드 생성
        super().__init__("tf2_listener")
        
        # TF Buffer 생성 (TF 정보를 저장)
        self.tf_buffer = Buffer()
        
        # TransformListener 생성 (TF 수신)
        # tf_buffer에 수신한 TF 정보가 자동으로 저장됨
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Timer 생성: 0.1초마다 on_timer 호출 (10Hz)
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        """
        주기적으로 호출되어 TF 조회를 수행하는 함수
        """
        try:
            # TF 조회 (lookup_transform)
            # 첫 번째 인자: 목표 프레임 (target frame)
            # 두 번째 인자: 소스 프레임 (source frame)
            # 세 번째 인자: 시간 (Time()는 최신 정보)
            # 의미: "world 기준으로 joint의 위치는?"
            t = self.tf_buffer.lookup_transform("joint", "world", time.Time())
        except Exception:
            # TF 조회 실패 시 (아직 TF가 발행되지 않았거나 연결 안 됨)
            self.get_logger().info("lookup 실패!!")
            return
        
        # TF 조회 성공: 위치 정보 출력
        self.get_logger().info(f"{t.transform.translation.x}")
        self.get_logger().info(f"{t.transform.translation.y}")
        self.get_logger().info(f"{t.transform.translation.z}")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # TF Listener 노드 생성
    node = FrameListener()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: TF 브로드캐스터 실행 (TF 정보 발행)
ros2 run hello_ros2 dynamic_tf

# 터미널 2: TF 리스너 실행 (TF 정보 수신)
ros2 run hello_ros2 tf_listener
```

---

**User**

계속해

---

**Cursor**

계속해서 나머지 파일들의 주석을 달아드리겠습니다!

---

## 📄 16. follow_turtlesim.py (터틀 따라가기 - TF 응용)

```python
"""
ROS2 TF 응용 예제 - Turtle Following
- turtle2가 turtle1을 자동으로 따라가는 프로그램
- TF를 사용하여 두 터틀 간의 상대 위치를 계산
- TransformBroadcaster와 TransformListener를 모두 사용
"""

# 사전 설치 필요:
# sudo apt install ros-humble-tf-transformations

# 실행 방법:
# ros2 run turtlesim turtlesim_node
# ros2 run hello_ros2 follow_turtlesim
# rviz2 -> tf 확인
# ros2 run turtlesim turtle_teleop_key

import math

import rclpy
from geometry_msgs.msg import TransformStamped, Twist
from rclpy import time
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf2_ros.transform_listener import TransformListener
from tf_transformations import euler_from_quaternion, quaternion_from_euler
from turtlesim.msg import Pose  # 터틀의 위치 정보
from turtlesim.srv import Spawn  # 새 터틀 생성 서비스


class Follow_turtle(Node):
    """
    turtle2가 turtle1을 따라가는 노드
    TF를 사용하여 두 터틀의 상대 위치를 계산하고 제어
    """
    
    def __init__(self):
        """Follow Turtle 노드 초기화"""
        # "follow_turtle"이라는 이름의 노드 생성
        super().__init__("follow_turtle")
        
        # === TF 관련 설정 ===
        # TF Buffer 생성 (TF 정보 저장)
        self.tf_buffer = Buffer()
        
        # TransformListener 생성 (TF 수신)
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Timer: 0.1초마다 on_timer 호출 (제어 루프)
        self.timer = self.create_timer(0.1, self.on_timer)
        
        # TransformBroadcaster 생성 (TF 발행)
        self.tf_br = TransformBroadcaster(self)
        
        # === turtle2 생성 서비스 호출 ===
        # Spawn 서비스 클라이언트 생성
        self.spawner = self.create_client(Spawn, "spawn")
        
        # Spawn 요청 생성
        request = Spawn.Request()
        request.x = 3.0  # 초기 x 위치
        request.y = 3.0  # 초기 y 위치
        request.theta = 0.0  # 초기 방향
        
        # 비동기로 turtle2 생성 요청
        self.result = self.spawner.call_async(request)
        self.result.add_done_callback(self.spawn_cb)
        
        # === Subscriber 설정 ===
        # turtle1의 위치 정보 구독
        self.sub = self.create_subscription(Pose, "/turtle1/pose", self.sub_cb, 10)
        
        # turtle2의 위치 정보 구독
        self.sub2 = self.create_subscription(Pose, "/turtle2/pose", self.sub_cb2, 10)
        
        # === Publisher 설정 ===
        # turtle2에게 속도 명령 발행
        self.pub = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)

    def spawn_cb(self, future):
        """
        turtle2 생성 서비스 응답 콜백
        
        Args:
            future: 서비스 응답이 담긴 Future
        """
        try:
            response = future.result()
            if response.name == "turtle2":
                self.get_logger().info("Turtle2 spawned successfully!")
            else:
                self.get_logger().error("Failed to spawn turtle2.")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

    def sub_cb(self, msg: Pose):
        """
        turtle1의 위치를 TF로 브로드캐스트하는 콜백
        
        Args:
            msg: turtle1의 Pose 메시지 (x, y, theta)
        """
        # TransformStamped 메시지 생성
        t = TransformStamped()
        
        # 헤더 설정
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"  # 부모 프레임 (고정 좌표계)
        t.child_frame_id = "turtle1"  # 자식 프레임 (turtle1)
        
        # 위치 설정 (translation)
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0  # 2D이므로 z는 0
        
        # 방향 설정 (rotation)
        # 오일러각(theta)을 쿼터니언으로 변환
        quat = quaternion_from_euler(0, 0, msg.theta)  # roll, pitch, yaw
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]
        
        # TF 브로드캐스트
        self.tf_br.sendTransform(t)

    def sub_cb2(self, msg: Pose):
        """
        turtle2의 위치를 TF로 브로드캐스트하는 콜백
        
        Args:
            msg: turtle2의 Pose 메시지 (x, y, theta)
        """
        # TransformStamped 메시지 생성
        t = TransformStamped()
        
        # 헤더 설정
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"  # 부모 프레임
        t.child_frame_id = "turtle2"  # 자식 프레임 (turtle2)
        
        # 위치 설정
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0
        
        # 방향 설정
        quat = quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]
        
        # TF 브로드캐스트
        self.tf_br.sendTransform(t)

    def on_timer(self):
        """
        주기적으로 호출되는 제어 루프
        turtle2를 turtle1 방향으로 이동시킴
        """
        try:
            # TF 조회: turtle2 기준으로 turtle1의 상대 위치
            # "turtle2에서 turtle1을 보면 어디에 있나?"
            t = self.tf_buffer.lookup_transform("turtle2", "turtle1", time.Time())
        except Exception as e:
            self.get_logger().info(f"Lookup transform 실패!!: {e}")
            return

        # Twist 메시지 생성 (속도 명령)
        msg = Twist()
        
        # === 각도 제어 (방향 맞추기) ===
        # turtle2 기준으로 turtle1까지의 각도 계산
        angle_error_rad = math.atan2(
            t.transform.translation.y,  # y 방향 거리
            t.transform.translation.x,  # x 방향 거리
        )

        # 회전 제어 로직
        if angle_error_rad > 0.1:
            # 목표가 왼쪽에 있음 -> 반시계 방향 회전
            msg.angular.z = 4.0
        elif angle_error_rad < -0.1:
            # 목표가 오른쪽에 있음 -> 시계 방향 회전
            msg.angular.z = -4.0
        else:
            # 방향이 거의 맞음 -> 회전 멈춤
            msg.angular.z = 0.0

        # === 거리 제어 (전진/정지) ===
        # turtle2와 turtle1 사이의 거리 계산 (유클리드 거리)
        distance = math.sqrt(
            t.transform.translation.x**2 + t.transform.translation.y**2
        )
        
        if distance > 0.2:
            # 거리가 0.2보다 크면 전진
            msg.linear.x = 2.0
        else:
            # 충분히 가까우면 정지
            msg.linear.x = 0.0

        # 속도 명령 발행
        self.pub.publish(msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Follow Turtle 노드 생성
    node = Follow_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: follow_turtlesim 실행
ros2 run hello_ros2 follow_turtlesim

# 터미널 3: turtle1을 키보드로 조종 (turtle2가 따라옴)
ros2 run turtlesim turtle_teleop_key

# 터미널 4: RViz로 TF 시각화
rviz2
# Fixed Frame: world
# Add -> TF
```

---

## 📄 17. my_topic_pub.py (커스텀 메시지 Publisher)

```python
"""
ROS2 커스텀 메시지 Publisher 예제
- user_interface 패키지의 MyTopic 메시지 사용
- Header와 정수 필드를 포함한 커스텀 메시지 발행
"""

# 실행 방법:
# ros2 run hello_ros2 my_topic_pub
# ros2 topic echo /message

import rclpy
from rclpy.node import Node
from user_interface.msg import MyTopic  # 커스텀 메시지 타입


class Simple_pub(Node):
    """
    커스텀 메시지를 발행하는 Publisher 노드
    MyTopic 메시지를 /message 토픽으로 전송
    """
    
    def __init__(self):
        """커스텀 메시지 Publisher 초기화"""
        # "myTopicPub"이라는 이름의 노드 생성
        super().__init__("myTopicPub")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출 (10Hz)
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # MyTopic 타입의 메시지를 "/message" 토픽으로 발행
        self.pub = self.create_publisher(MyTopic, "/message", 10)
        
        # 카운터 초기화
        self.count = 0

    def pub_turtle(self):
        """
        주기적으로 호출되어 커스텀 메시지를 발행하는 함수
        """
        # MyTopic 메시지 객체 생성
        msg = MyTopic()
        
        # 메시지 필드 설정
        msg.a = 10  # 정수 필드 a
        msg.b = 20  # 정수 필드 b
        
        # Header 설정
        # stamp: 현재 시간 (타임스탬프)
        msg.header.stamp = self.get_clock().now().to_msg()
        # frame_id: 프레임 ID (여기서는 설명 문자열로 사용)
        msg.header.frame_id = f"내가 만든 토픽 입니다.{self.count}"
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 카운터 증가
        self.count += 1


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # 커스텀 메시지 Publisher 노드 생성
    node = Simple_pub()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**MyTopic.msg 구조:**
```
std_msgs/Header header  # 타임스탬프와 프레임 ID
int32 a                 # 정수 a
int32 b                 # 정수 b
```

**실행 방법:**
```bash
# 터미널 1: 커스텀 메시지 Publisher 실행
ros2 run hello_ros2 my_topic_pub

# 터미널 2: 메시지 확인
ros2 topic echo /message

# 터미널 3: 메시지 타입 확인
ros2 interface show user_interface/msg/MyTopic
```

---

## 📄 18. patrol.py (Nav2 순찰 - Action 응용)

```python
"""
ROS2 Navigation2 순찰 예제
- Nav2의 FollowWaypoints 액션을 사용
- 미리 정의된 경로점(waypoints)을 순환하며 순찰
- TurtleBot3 시뮬레이션과 함께 사용
"""

# 실행 방법:
# ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
# ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=/home/aa/kuLimo/map.yaml
# initial pose 잡아서 amcl 활성화
# ros2 run hello_ros2 patrol

import math
import time

import rclpy
from action_msgs.msg import GoalStatus  # Action goal 상태
from geometry_msgs.msg import PoseStamped  # 목표 위치
from nav2_msgs.action import FollowWaypoints  # Nav2 순찰 액션
from nav2_msgs.action._follow_waypoints import FollowWaypoints_GetResult_Response
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from rclpy.node import Node
from rclpy.task import Future


class Action_client(Node):
    """
    Nav2를 사용하여 지정된 경로점을 순환하며 순찰하는 노드
    """
    
    def __init__(self):
        """Patrol 노드 초기화"""
        # "fibonacci_client"라는 이름의 노드 생성 (이름 변경 권장)
        super().__init__("fibonacci_client")
        
        # Action Client 생성
        # FollowWaypoints 액션: Nav2의 경로점 추적 기능
        self.action_client = ActionClient(self, FollowWaypoints, "follow_waypoints")
        
        # Future 객체들
        self.future = Future()
        self.get_result_future = Future()
        
        # === 순찰 경로 정의 ===
        # patrol_points: (x, y) 좌표 리스트 (map 좌표계 기준)
        self.patrol_points = [(4.0, 0.0), (4.0, 1.0), (2.0, 2.5), (0.0, 1.0)]
        
        # patrol_degree: 각 지점에서의 방향 (도 단위)
        self.patrol_degree = [0, 90, 180, 90]
        
        # 현재 순찰 인덱스
        self.patrol_index = 0
        
        # Goal 객체 생성
        self.goal = FollowWaypoints.Goal()
        
        # 첫 번째 경로점으로 이동 시작
        self.go_next()

    def go_next(self):
        """
        다음 순찰 지점으로 이동
        순환 방식: 마지막 지점 이후 다시 첫 번째로
        """
        # 현재 인덱스의 경로점으로 이동 요청
        self.send_goal(
            self.patrol_points[self.patrol_index][0],  # x 좌표
            self.patrol_points[self.patrol_index][1],  # y 좌표
            self.patrol_degree[self.patrol_index],      # 방향
        )
        
        # 인덱스 증가
        self.patrol_index += 1
        
        # 마지막 지점을 지나면 처음으로 되돌림 (순환)
        if self.patrol_index >= len(self.patrol_points):
            self.patrol_index = 0

    def send_goal(self, x: float, y: float, theta: int):
        """
        지정된 위치로 이동하는 goal을 전송
        
        Args:
            x: 목표 x 좌표 (미터)
            y: 목표 y 좌표 (미터)
            theta: 목표 방향 (도)
        """
        # PoseStamped 메시지 생성 (위치와 방향)
        pose = PoseStamped()
        
        # 헤더 설정
        pose.header.frame_id = "map"  # map 좌표계 기준
        pose.header.stamp = self.get_clock().now().to_msg()
        
        # 위치 설정
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0  # 2D 네비게이션이므로 z는 0
        
        # 방향 설정 (쿼터니언)
        # 도(degree)를 라디안(radian)으로 변환
        rad = math.radians(theta)
        
        # Yaw 각도를 쿼터니언으로 변환
        # q = [x, y, z, w] = [0, 0, sin(θ/2), cos(θ/2)]
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = math.sin(rad / 2.0)
        pose.pose.orientation.w = math.cos(rad / 2.0)
        
        # Goal의 poses 리스트 초기화 및 추가
        self.goal.poses.clear()  # type : ignore
        self.goal.poses.append(pose)  # type : ignore
        
        # Nav2 서버 접속 대기
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("nav2 서버 접속중 ...")
        
        # 비동기로 goal 전송
        self.future: Future = self.action_client.send_goal_async(
            self.goal, 
            feedback_callback=self.feedback_callback
        )
        
        # goal 응답 콜백 등록
        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future):
        """
        goal이 서버에 접수되었는지 확인하는 콜백
        
        Args:
            future: goal 전송 결과
        """
        # goal 핸들 추출
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        
        # goal이 거부된 경우
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        
        # goal이 접수된 경우, 결과 요청
        self.get_result_future: Future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        """
        네비게이션 진행 중 피드백 수신 콜백
        
        Args:
            msg: 피드백 메시지
        """
        feedback: FollowWaypoints.Feedback = msg.feedback
        
        # 현재 경로점 번호 출력
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.current_waypoint}")
        self.get_logger().info(f" patrol index{self.patrol_index}")

    def done_callback(self, future: Future):
        """
        네비게이션 완료 시 호출되는 콜백
        
        Args:
            future: 결과가 담긴 Future
        """
        # 결과 추출
        result: FollowWaypoints_GetResult_Response = future.result()  # type : ignore
        
        # 성공 여부에 따라 처리
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            # 성공: 다음 경로점으로 이동
            self.get_logger().info(f"result: {result.result.missed_waypoints} 성공!!")
            self.go_next()  # 다음 순찰 지점으로
        if result.status == GoalStatus.STATUS_ABORTED:
            # 실패: 로그 출력
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Patrol 노드 생성
    node = Action_client()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 1단계: TurtleBot3 모델 설정
export TURTLEBOT3_MODEL=waffle_pi

# 2단계: Gazebo 시뮬레이션 실행
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 3단계: Navigation2 실행 (새 터미널)
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
    use_sim_time:=True \
    map:=/path/to/your/map.yaml

# 4단계: RViz에서 "2D Pose Estimate" 설정 (로봇의 초기 위치)

# 5단계: 순찰 노드 실행 (새 터미널)
ros2 run hello_ros2 patrol
```

---

## 📄 19. publish_map.py (OccupancyGrid 맵 발행)

```python
"""
ROS2 OccupancyGrid 맵 발행 예제
- 점유 격자 지도(Occupancy Grid)를 동적으로 생성하여 발행
- RViz에서 시각화 가능
- 맵 데이터를 순차적으로 변경하여 애니메이션 효과
"""

# 실행 방법:
# ros2 topic echo /map --once
# ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
# ros2 run hello_ros2 publish_map

import rclpy
from nav_msgs.msg import OccupancyGrid  # 점유 격자 지도 메시지
from rclpy.node import Node


class PublishMap(Node):
    """
    동적으로 변화하는 OccupancyGrid 맵을 발행하는 노드
    """
    
    def __init__(self):
        """Map Publisher 초기화"""
        # "publish_map"이라는 이름의 노드 생성
        super().__init__("publish_map")
        
        # Timer 생성: 0.001초마다 pub_cb 호출 (1000Hz - 매우 빠름)
        self.create_timer(0.001, self.pub_cb)
        
        # Publisher 생성
        # OccupancyGrid 메시지를 "/map" 토픽으로 발행
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        
        # OccupancyGrid 메시지 생성
        self.msg = OccupancyGrid()
        
        # === 맵 헤더 설정 ===
        self.msg.header.frame_id = "odom"  # 좌표계
        
        # === 맵 메타데이터 설정 ===
        self.msg.info.resolution = 0.1  # 해상도: 한 셀당 0.1m (10cm)
        self.msg.info.width = 200  # 맵 너비: 200셀
        self.msg.info.height = 100  # 맵 높이: 100셀
        
        # 맵 원점 위치 (맵의 좌하단 코너)
        self.msg.info.origin.position.x = 0.0
        self.msg.info.origin.position.y = 0.0
        self.msg.info.origin.position.z = 0.0
        
        # 맵 원점 방향 (회전 없음)
        self.msg.info.origin.orientation.x = 0.0
        self.msg.info.origin.orientation.y = 0.0
        self.msg.info.origin.orientation.z = 0.0
        self.msg.info.origin.orientation.w = 1.0

        # === 맵 데이터 초기화 ===
        # OccupancyGrid 값:
        # -1: 미지의 영역 (unknown)
        # 0: 빈 공간 (free)
        # 100: 장애물 (occupied)
        
        # 처음 10,000셀은 100 (장애물)
        self.msg.data = [100 for _ in range(10_000)]
        # 나머지 10,000셀은 0 (빈 공간)
        self.msg.data.extend([0 for _ in range(10_000)])

        # 현재 수정 중인 셀의 열(column) 인덱스
        self.count = 0
        # 현재 수정 중인 셀의 행(row) 인덱스
        self.row = 0

    def pub_cb(self):
        """
        주기적으로 호출되어 맵을 발행하는 함수
        맵의 각 셀을 순차적으로 변경하여 애니메이션 효과
        """
        # 타임스탬프 업데이트
        self.msg.header.stamp = self.get_clock().now().to_msg()

        # 현재 수정할 셀의 1차원 인덱스 계산
        # 2D 좌표 (row, count)를 1D 인덱스로 변환
        # index = x + (width * y)
        index = self.count + (self.msg.info.width * self.row)
        
        # 현재 셀의 값을 토글
        if self.msg.data[index] == -1:
            # 미지의 영역(-1)을 장애물(100)로 변경
            self.msg.data[index] = 100
        else:
            # 그 외의 값을 미지의 영역(-1)로 변경
            self.msg.data[index] = -1

        # 다음 셀로 이동 (열 증가)
        self.count += 1
        
        # 행의 끝에 도달하면 다음 행으로
        if self.count >= self.msg.info.width:
            self.count = 0  # 열 인덱스 초기화
            self.row += 1  # 다음 행으로
        
        # 맵의 끝에 도달하면 처음으로
        if self.row >= self.msg.info.height:
            self.row = 0

        # 맵 메시지 발행
        self.pub.publish(self.msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Map Publisher 노드 생성
    node = PublishMap()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: TF 발행 (map -> odom)
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom

# 터미널 2: 맵 발행
ros2 run hello_ros2 publish_map

# 터미널 3: RViz로 시각화
rviz2
# Fixed Frame: map
# Add -> Map
# Topic: /map
```

---

## 📄 20. scan_map.py (LaserScan + Map 통합)

```python
"""
ROS2 LaserScan과 OccupancyGrid 통합 예제
- publish_map.py를 확장한 버전
- LaserScan 데이터를 구독하여 맵 생성에 활용 가능
- SLAM 알고리즘의 기초 개념
"""

# 실행 방법:
# ros2 topic echo /map --once
# ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
# ros2 run hello_ros2 scan_map

import rclpy
from nav_msgs.msg import OccupancyGrid
from rclpy.node import Node
from sensor_msgs.msg import LaserScan  # LiDAR 스캔 데이터


class PublishMap(Node):
    """
    LaserScan 데이터를 사용하여 OccupancyGrid 맵을 생성하는 노드
    (SLAM의 간단한 예시)
    """
    
    def __init__(self):
        """Scan Map 노드 초기화"""
        # "publish_map"이라는 이름의 노드 생성
        super().__init__("publish_map")
        
        # === Timer 설정 ===
        # Timer 1: 0.001초마다 pub_cb 호출 (맵 발행)
        self.create_timer(0.001, self.pub_cb)
        
        # Timer 2: 1/60초마다 update 호출 (맵 업데이트 알고리즘)
        self.create_timer(1 / 60, self.update)
        
        # === Publisher 설정 ===
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        
        # === OccupancyGrid 메시지 초기화 ===
        self.msg = OccupancyGrid()
        self.msg.header.frame_id = "odom"
        
        # 맵 메타데이터
        self.msg.info.resolution = 0.1  # 10cm per cell
        self.msg.info.width = 200
        self.msg.info.height = 100
        
        # 맵 원점
        self.msg.info.origin.position.x = 0.0
        self.msg.info.origin.position.y = 0.0
        self.msg.info.origin.position.z = 0.0
        self.msg.info.origin.orientation.x = 0.0
        self.msg.info.origin.orientation.y = 0.0
        self.msg.info.origin.orientation.z = 0.0
        self.msg.info.origin.orientation.w = 1.0

        # === LaserScan Subscriber 설정 ===
        # "scan" 토픽을 구독하여 LiDAR 데이터 수신
        self.create_subscription(LaserScan, "scan", self.laser_cb, 10)

        # 맵 데이터 초기화
        self.msg.data = [100 for _ in range(10_000)]
        self.msg.data.extend([0 for _ in range(10_000)])

        # 인덱스 변수
        self.count = 0
        self.row = 0
        
        # LaserScan 데이터 저장 변수
        self.laser_s = LaserScan()

    def update(self):
        """
        주기적으로 호출되어 LaserScan 데이터를 처리하는 함수
        여기에 SLAM 알고리즘을 구현할 수 있음
        """
        # === 알고리즘 구현 영역 ===
        # self.laser_s에 저장된 LaserScan 데이터를 사용하여
        # self.msg.data를 업데이트하는 코드를 작성
        
        # 예시:
        # 1. self.laser_s.ranges에서 거리 데이터 추출
        # 2. 각 거리 데이터를 좌표로 변환
        # 3. 해당 좌표의 맵 셀을 장애물(100)로 표시
        # 4. 로봇과 장애물 사이는 빈 공간(0)으로 표시
        
        pass  # 실제 구현은 학생이 작성

    def laser_cb(self, msg):
        """
        LaserScan 데이터를 수신하는 콜백
        
        Args:
            msg: LaserScan 메시지
                - ranges: 거리 측정값 배열
                - angle_min: 최소 각도
                - angle_max: 최대 각도
                - angle_increment: 각도 증분
                - range_min: 최소 측정 거리
                - range_max: 최대 측정 거리
        """
        # 수신한 LaserScan 데이터를 저장
        self.laser_s = msg

    def pub_cb(self):
        """
        맵을 발행하는 함수
        (publish_map.py와 동일)
        """
        # 타임스탬프 업데이트
        self.msg.header.stamp = self.get_clock().now().to_msg()

        # 현재 셀 인덱스 계산
        index = self.count + (self.msg.info.width * self.row)
        
        # 셀 값 토글
        if self.msg.data[index] == -1:
            self.msg.data[index] = 100
        else:
            self.msg.data[index] = -1

        # 다음 셀로 이동
        self.count += 1
        if self.count >= self.msg.info.width:
            self.count = 0
            self.row += 1
        if self.row >= self.msg.info.height:
            self.row = 0

        # 맵 발행
        self.pub.publish(self.msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Scan Map 노드 생성
    node = PublishMap()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

**실행 방법:**
```bash
# 터미널 1: Gazebo + LiDAR 장착 로봇 실행
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 터미널 2: TF 발행
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom

# 터미널 3: Scan Map 노드 실행
ros2 run hello_ros2 scan_map

# 터미널 4: RViz로 시각화
rviz2
# Fixed Frame: map
# Add -> Map (Topic: /map)
# Add -> LaserScan (Topic: /scan)
```

---

## 🎉 모든 파일 주석 완료!

이제 hello_ros2 폴더의 모든 Python 코드 파일에 상세한 주석이 추가되었습니다!

### 📚 학습 순서 추천:

1. **기초** (1-5): hello_ros → simple_pub/sub → service → action → parameter
2. **응용** (6-12): move_turtle → tf_listener → dynamic_tf → follow_turtlesim
3. **고급** (13-20): custom messages → navigation → mapping

각 파일을 위에서 제공한 주석 버전으로 교체하시면 코드 이해에 큰 도움이 될 것입니다! 😊

```python
"""
ROS2 TF 응용 예제 - Turtle Following
- turtle2가 turtle1을 자동으로 따라가는 프로그램
- TF를 사용하여 두 터틀 간의 상대 위치를 계산
- TransformBroadcaster와 TransformListener를 모두 사용
"""

# 사전 설치 필요:
# sudo apt install ros-humble-tf-transformations

# 실행 방법:
# ros2 run turtlesim turtlesim_node
# ros2 run hello_ros2 follow_turtlesim
# rviz2 -> tf 확인
# ros2 run turtlesim turtle_teleop_key

import math

import rclpy
from geometry_msgs.msg import TransformStamped, Twist
from rclpy import time
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf2_ros.transform_listener import TransformListener
from tf_transformations import euler_from_quaternion, quaternion_from_euler
from turtlesim.msg import Pose  # 터틀의 위치 정보
from turtlesim.srv import Spawn  # 새 터틀 생성 서비스


class Follow_turtle(Node):
    """
    turtle2가 turtle1을 따라가는 노드
    TF를 사용하여 두 터틀의 상대 위치를 계산하고 제어
    """
    
    def __init__(self):
        """Follow Turtle 노드 초기화"""
        # "follow_turtle"이라는 이름의 노드 생성
        super().__init__("follow_turtle")
        
        # === TF 관련 설정 ===
        # TF Buffer 생성 (TF 정보 저장)
        self.tf_buffer = Buffer()
        
        # TransformListener 생성 (TF 수신)
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Timer: 0.1초마다 on_timer 호출 (제어 루프)
        self.timer = self.create_timer(0.1, self.on_timer)
        
        # TransformBroadcaster 생성 (TF 발행)
        self.tf_br = TransformBroadcaster(self)
        
        # === turtle2 생성 서비스 호출 ===
        # Spawn 서비스 클라이언트 생성
        self.spawner = self.create_client(Spawn, "spawn")
        
        # Spawn 요청 생성
        request = Spawn.Request()
        request.x = 3.0  # 초기 x 위치
        request.y = 3.0  # 초기 y 위치
        request.theta = 0.0  # 초기 방향
        
        # 비동기로 turtle2 생성 요청
        self.result = self.spawner.call_async(request)
        self.result.add_done_callback(self.spawn_cb)
        
        # === Subscriber 설정 ===
        # turtle1의 위치 정보 구독
        self.sub = self.create_subscription(Pose, "/turtle1/pose", self.sub_cb, 10)
        
        # turtle2의 위치 정보 구독
        self.sub2 = self.create_subscription(Pose, "/turtle2/pose", self.sub_cb2, 10)
        
        # === Publisher 설정 ===
        # turtle2에게 속도 명령 발행
        self.pub = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)

    def spawn_cb(self, future):
        """
        turtle2 생성 서비스 응답 콜백
        
        Args:
            future: 서비스 응답이 담긴 Future
        """
        try:
            response = future.result()
            if response.name == "turtle2":
                self.get_logger().info("Turtle2 spawned successfully!")
            else:
                self.get_logger().error("Failed to spawn turtle2.")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

    def sub_cb(self, msg: Pose):
        """
        turtle1의 위치를 TF로 브로드캐스트하는 콜백
        
        Args:
            msg: turtle1의 Pose 메시지 (x, y, theta)
        """
        # TransformStamped 메시지 생성
        t = TransformStamped()
        
        # 헤더 설정
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"  # 부모 프레임 (고정 좌표계)
        t.child_frame_id = "turtle1"  # 자식 프레임 (turtle1)
        
        # 위치 설정 (translation)
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0  # 2D이므로 z는 0
        
        # 방향 설정 (rotation)
        # 오일러각(theta)을 쿼터니언으로 변환
        quat = quaternion_from_euler(0, 0, msg.theta)  # roll, pitch, yaw
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]
        
        # TF 브로드캐스트
        self.tf_br.sendTransform(t)

    def sub_cb2(self, msg: Pose):
        """
        turtle2의 위치를 TF로 브로드캐스트하는 콜백
        
        Args:
            msg: turtle2의 Pose 메시지 (x, y, theta)
        """
        # TransformStamped 메시지 생성
        t = TransformStamped()
        
        # 헤더 설정
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"  # 부모 프레임
        t.child_frame_id = "turtle2"  # 자식 프레임 (turtle2)
        
        # 위치 설정
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0
        
        # 방향 설정
        quat = quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]
        
        # TF 브로드캐스트
        self.tf_br.sendTransform(t)

    def on_timer(self):
        """
        주기적으로 호출되는 제어 루프
        turtle2를 turtle1 방향으로 이동시킴
        """
        try:
            # TF 조회: turtle2 기준으로 turtle1의 상대 위치
            # "turtle2에서 turtle1을 보면 어디에 있나?"
            t = self.tf_buffer.lookup_transform("turtle2", "turtle1", time.Time())
        except Exception as e:
            self.get_logger().info(f"Lookup transform 실패!!: {e}")
            return

        # Twist 메시지 생성 (속도 명령)
        msg = Twist()
        
        # === 각도 제어 (방향 맞추기) ===
        # turtle2 기준으로 turtle1까지의 각도 계산
        angle_error_rad = math.atan2(
            t.transform.translation.y,  # y 방향 거리
            t.transform.translation.x,  # x 방향 거리
        )

        # 회전 제어 로직
        if angle_error_rad > 0.1:
            # 목표가 왼쪽에 있음 -> 반시계 방향 회전
            msg.angular.z = 4.0
        elif angle_error_rad < -0.1:
            # 목표가 오른쪽에 있음 -> 시계 방향 회전
            msg.angular.z = -4.0
        else:
            # 방향이 거의 맞음 -> 회전 멈춤
            msg.angular.z = 0.0

        # === 거리 제어 (전진/정지) ===
        # turtle2와 turtle1 사이의 거리 계산 (유클리드 거리)
        distance = math.sqrt(
            t.transform.translation.x**2 + t.transform.translation.y**2
        )
        
        if distance > 0.2:
            # 거리가 0.2보다 크면 전진
            msg.linear.x = 2.0
        else:
            # 충분히 가까우면 정지
            msg.linear.x = 0.0

        # 속도 명령 발행
        self.pub.publish(msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Follow Turtle 노드 생성
    node = Follow_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: follow_turtlesim 실행
ros2 run hello_ros2 follow_turtlesim

# 터미널 3: turtle1을 키보드로 조종 (turtle2가 따라옴)
ros2 run turtlesim turtle_teleop_key

# 터미널 4: RViz로 TF 시각화
rviz2
# Fixed Frame: world
# Add -> TF
```

```python
"""
ROS2 커스텀 메시지 Publisher 예제
- user_interface 패키지의 MyTopic 메시지 사용
- Header와 정수 필드를 포함한 커스텀 메시지 발행
"""

# 실행 방법:
# ros2 run hello_ros2 my_topic_pub
# ros2 topic echo /message

import rclpy
from rclpy.node import Node
from user_interface.msg import MyTopic  # 커스텀 메시지 타입


class Simple_pub(Node):
    """
    커스텀 메시지를 발행하는 Publisher 노드
    MyTopic 메시지를 /message 토픽으로 전송
    """
    
    def __init__(self):
        """커스텀 메시지 Publisher 초기화"""
        # "myTopicPub"이라는 이름의 노드 생성
        super().__init__("myTopicPub")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출 (10Hz)
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # MyTopic 타입의 메시지를 "/message" 토픽으로 발행
        self.pub = self.create_publisher(MyTopic, "/message", 10)
        
        # 카운터 초기화
        self.count = 0

    def pub_turtle(self):
        """
        주기적으로 호출되어 커스텀 메시지를 발행하는 함수
        """
        # MyTopic 메시지 객체 생성
        msg = MyTopic()
        
        # 메시지 필드 설정
        msg.a = 10  # 정수 필드 a
        msg.b = 20  # 정수 필드 b
        
        # Header 설정
        # stamp: 현재 시간 (타임스탬프)
        msg.header.stamp = self.get_clock().now().to_msg()
        # frame_id: 프레임 ID (여기서는 설명 문자열로 사용)
        msg.header.frame_id = f"내가 만든 토픽 입니다.{self.count}"
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 카운터 증가
        self.count += 1


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # 커스텀 메시지 Publisher 노드 생성
    node = Simple_pub()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```plaintext
std_msgs/Header header  # 타임스탬프와 프레임 ID
int32 a                 # 정수 a
int32 b                 # 정수 b
```

```shellscript
# 터미널 1: 커스텀 메시지 Publisher 실행
ros2 run hello_ros2 my_topic_pub

# 터미널 2: 메시지 확인
ros2 topic echo /message

# 터미널 3: 메시지 타입 확인
ros2 interface show user_interface/msg/MyTopic
```

```python
"""
ROS2 Navigation2 순찰 예제
- Nav2의 FollowWaypoints 액션을 사용
- 미리 정의된 경로점(waypoints)을 순환하며 순찰
- TurtleBot3 시뮬레이션과 함께 사용
"""

# 실행 방법:
# ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
# ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=/home/aa/kuLimo/map.yaml
# initial pose 잡아서 amcl 활성화
# ros2 run hello_ros2 patrol

import math
import time

import rclpy
from action_msgs.msg import GoalStatus  # Action goal 상태
from geometry_msgs.msg import PoseStamped  # 목표 위치
from nav2_msgs.action import FollowWaypoints  # Nav2 순찰 액션
from nav2_msgs.action._follow_waypoints import FollowWaypoints_GetResult_Response
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from rclpy.node import Node
from rclpy.task import Future


class Action_client(Node):
    """
    Nav2를 사용하여 지정된 경로점을 순환하며 순찰하는 노드
    """
    
    def __init__(self):
        """Patrol 노드 초기화"""
        # "fibonacci_client"라는 이름의 노드 생성 (이름 변경 권장)
        super().__init__("fibonacci_client")
        
        # Action Client 생성
        # FollowWaypoints 액션: Nav2의 경로점 추적 기능
        self.action_client = ActionClient(self, FollowWaypoints, "follow_waypoints")
        
        # Future 객체들
        self.future = Future()
        self.get_result_future = Future()
        
        # === 순찰 경로 정의 ===
        # patrol_points: (x, y) 좌표 리스트 (map 좌표계 기준)
        self.patrol_points = [(4.0, 0.0), (4.0, 1.0), (2.0, 2.5), (0.0, 1.0)]
        
        # patrol_degree: 각 지점에서의 방향 (도 단위)
        self.patrol_degree = [0, 90, 180, 90]
        
        # 현재 순찰 인덱스
        self.patrol_index = 0
        
        # Goal 객체 생성
        self.goal = FollowWaypoints.Goal()
        
        # 첫 번째 경로점으로 이동 시작
        self.go_next()

    def go_next(self):
        """
        다음 순찰 지점으로 이동
        순환 방식: 마지막 지점 이후 다시 첫 번째로
        """
        # 현재 인덱스의 경로점으로 이동 요청
        self.send_goal(
            self.patrol_points[self.patrol_index][0],  # x 좌표
            self.patrol_points[self.patrol_index][1],  # y 좌표
            self.patrol_degree[self.patrol_index],      # 방향
        )
        
        # 인덱스 증가
        self.patrol_index += 1
        
        # 마지막 지점을 지나면 처음으로 되돌림 (순환)
        if self.patrol_index >= len(self.patrol_points):
            self.patrol_index = 0

    def send_goal(self, x: float, y: float, theta: int):
        """
        지정된 위치로 이동하는 goal을 전송
        
        Args:
            x: 목표 x 좌표 (미터)
            y: 목표 y 좌표 (미터)
            theta: 목표 방향 (도)
        """
        # PoseStamped 메시지 생성 (위치와 방향)
        pose = PoseStamped()
        
        # 헤더 설정
        pose.header.frame_id = "map"  # map 좌표계 기준
        pose.header.stamp = self.get_clock().now().to_msg()
        
        # 위치 설정
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0  # 2D 네비게이션이므로 z는 0
        
        # 방향 설정 (쿼터니언)
        # 도(degree)를 라디안(radian)으로 변환
        rad = math.radians(theta)
        
        # Yaw 각도를 쿼터니언으로 변환
        # q = [x, y, z, w] = [0, 0, sin(θ/2), cos(θ/2)]
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = math.sin(rad / 2.0)
        pose.pose.orientation.w = math.cos(rad / 2.0)
        
        # Goal의 poses 리스트 초기화 및 추가
        self.goal.poses.clear()  # type : ignore
        self.goal.poses.append(pose)  # type : ignore
        
        # Nav2 서버 접속 대기
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("nav2 서버 접속중 ...")
        
        # 비동기로 goal 전송
        self.future: Future = self.action_client.send_goal_async(
            self.goal, 
            feedback_callback=self.feedback_callback
        )
        
        # goal 응답 콜백 등록
        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future):
        """
        goal이 서버에 접수되었는지 확인하는 콜백
        
        Args:
            future: goal 전송 결과
        """
        # goal 핸들 추출
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        
        # goal이 거부된 경우
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        
        # goal이 접수된 경우, 결과 요청
        self.get_result_future: Future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        """
        네비게이션 진행 중 피드백 수신 콜백
        
        Args:
            msg: 피드백 메시지
        """
        feedback: FollowWaypoints.Feedback = msg.feedback
        
        # 현재 경로점 번호 출력
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.current_waypoint}")
        self.get_logger().info(f" patrol index{self.patrol_index}")

    def done_callback(self, future: Future):
        """
        네비게이션 완료 시 호출되는 콜백
        
        Args:
            future: 결과가 담긴 Future
        """
        # 결과 추출
        result: FollowWaypoints_GetResult_Response = future.result()  # type : ignore
        
        # 성공 여부에 따라 처리
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            # 성공: 다음 경로점으로 이동
            self.get_logger().info(f"result: {result.result.missed_waypoints} 성공!!")
            self.go_next()  # 다음 순찰 지점으로
        if result.status == GoalStatus.STATUS_ABORTED:
            # 실패: 로그 출력
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Patrol 노드 생성
    node = Action_client()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 1단계: TurtleBot3 모델 설정
export TURTLEBOT3_MODEL=waffle_pi

# 2단계: Gazebo 시뮬레이션 실행
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 3단계: Navigation2 실행 (새 터미널)
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
    use_sim_time:=True \
    map:=/path/to/your/map.yaml

# 4단계: RViz에서 "2D Pose Estimate" 설정 (로봇의 초기 위치)

# 5단계: 순찰 노드 실행 (새 터미널)
ros2 run hello_ros2 patrol
```

```python
"""
ROS2 OccupancyGrid 맵 발행 예제
- 점유 격자 지도(Occupancy Grid)를 동적으로 생성하여 발행
- RViz에서 시각화 가능
- 맵 데이터를 순차적으로 변경하여 애니메이션 효과
"""

# 실행 방법:
# ros2 topic echo /map --once
# ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
# ros2 run hello_ros2 publish_map

import rclpy
from nav_msgs.msg import OccupancyGrid  # 점유 격자 지도 메시지
from rclpy.node import Node


class PublishMap(Node):
    """
    동적으로 변화하는 OccupancyGrid 맵을 발행하는 노드
    """
    
    def __init__(self):
        """Map Publisher 초기화"""
        # "publish_map"이라는 이름의 노드 생성
        super().__init__("publish_map")
        
        # Timer 생성: 0.001초마다 pub_cb 호출 (1000Hz - 매우 빠름)
        self.create_timer(0.001, self.pub_cb)
        
        # Publisher 생성
        # OccupancyGrid 메시지를 "/map" 토픽으로 발행
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        
        # OccupancyGrid 메시지 생성
        self.msg = OccupancyGrid()
        
        # === 맵 헤더 설정 ===
        self.msg.header.frame_id = "odom"  # 좌표계
        
        # === 맵 메타데이터 설정 ===
        self.msg.info.resolution = 0.1  # 해상도: 한 셀당 0.1m (10cm)
        self.msg.info.width = 200  # 맵 너비: 200셀
        self.msg.info.height = 100  # 맵 높이: 100셀
        
        # 맵 원점 위치 (맵의 좌하단 코너)
        self.msg.info.origin.position.x = 0.0
        self.msg.info.origin.position.y = 0.0
        self.msg.info.origin.position.z = 0.0
        
        # 맵 원점 방향 (회전 없음)
        self.msg.info.origin.orientation.x = 0.0
        self.msg.info.origin.orientation.y = 0.0
        self.msg.info.origin.orientation.z = 0.0
        self.msg.info.origin.orientation.w = 1.0

        # === 맵 데이터 초기화 ===
        # OccupancyGrid 값:
        # -1: 미지의 영역 (unknown)
        # 0: 빈 공간 (free)
        # 100: 장애물 (occupied)
        
        # 처음 10,000셀은 100 (장애물)
        self.msg.data = [100 for _ in range(10_000)]
        # 나머지 10,000셀은 0 (빈 공간)
        self.msg.data.extend([0 for _ in range(10_000)])

        # 현재 수정 중인 셀의 열(column) 인덱스
        self.count = 0
        # 현재 수정 중인 셀의 행(row) 인덱스
        self.row = 0

    def pub_cb(self):
        """
        주기적으로 호출되어 맵을 발행하는 함수
        맵의 각 셀을 순차적으로 변경하여 애니메이션 효과
        """
        # 타임스탬프 업데이트
        self.msg.header.stamp = self.get_clock().now().to_msg()

        # 현재 수정할 셀의 1차원 인덱스 계산
        # 2D 좌표 (row, count)를 1D 인덱스로 변환
        # index = x + (width * y)
        index = self.count + (self.msg.info.width * self.row)
        
        # 현재 셀의 값을 토글
        if self.msg.data[index] == -1:
            # 미지의 영역(-1)을 장애물(100)로 변경
            self.msg.data[index] = 100
        else:
            # 그 외의 값을 미지의 영역(-1)로 변경
            self.msg.data[index] = -1

        # 다음 셀로 이동 (열 증가)
        self.count += 1
        
        # 행의 끝에 도달하면 다음 행으로
        if self.count >= self.msg.info.width:
            self.count = 0  # 열 인덱스 초기화
            self.row += 1  # 다음 행으로
        
        # 맵의 끝에 도달하면 처음으로
        if self.row >= self.msg.info.height:
            self.row = 0

        # 맵 메시지 발행
        self.pub.publish(self.msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Map Publisher 노드 생성
    node = PublishMap()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: TF 발행 (map -> odom)
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom

# 터미널 2: 맵 발행
ros2 run hello_ros2 publish_map

# 터미널 3: RViz로 시각화
rviz2
# Fixed Frame: map
# Add -> Map
# Topic: /map
```

```python
"""
ROS2 LaserScan과 OccupancyGrid 통합 예제
- publish_map.py를 확장한 버전
- LaserScan 데이터를 구독하여 맵 생성에 활용 가능
- SLAM 알고리즘의 기초 개념
"""

# 실행 방법:
# ros2 topic echo /map --once
# ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
# ros2 run hello_ros2 scan_map

import rclpy
from nav_msgs.msg import OccupancyGrid
from rclpy.node import Node
from sensor_msgs.msg import LaserScan  # LiDAR 스캔 데이터


class PublishMap(Node):
    """
    LaserScan 데이터를 사용하여 OccupancyGrid 맵을 생성하는 노드
    (SLAM의 간단한 예시)
    """
    
    def __init__(self):
        """Scan Map 노드 초기화"""
        # "publish_map"이라는 이름의 노드 생성
        super().__init__("publish_map")
        
        # === Timer 설정 ===
        # Timer 1: 0.001초마다 pub_cb 호출 (맵 발행)
        self.create_timer(0.001, self.pub_cb)
        
        # Timer 2: 1/60초마다 update 호출 (맵 업데이트 알고리즘)
        self.create_timer(1 / 60, self.update)
        
        # === Publisher 설정 ===
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        
        # === OccupancyGrid 메시지 초기화 ===
        self.msg = OccupancyGrid()
        self.msg.header.frame_id = "odom"
        
        # 맵 메타데이터
        self.msg.info.resolution = 0.1  # 10cm per cell
        self.msg.info.width = 200
        self.msg.info.height = 100
        
        # 맵 원점
        self.msg.info.origin.position.x = 0.0
        self.msg.info.origin.position.y = 0.0
        self.msg.info.origin.position.z = 0.0
        self.msg.info.origin.orientation.x = 0.0
        self.msg.info.origin.orientation.y = 0.0
        self.msg.info.origin.orientation.z = 0.0
        self.msg.info.origin.orientation.w = 1.0

        # === LaserScan Subscriber 설정 ===
        # "scan" 토픽을 구독하여 LiDAR 데이터 수신
        self.create_subscription(LaserScan, "scan", self.laser_cb, 10)

        # 맵 데이터 초기화
        self.msg.data = [100 for _ in range(10_000)]
        self.msg.data.extend([0 for _ in range(10_000)])

        # 인덱스 변수
        self.count = 0
        self.row = 0
        
        # LaserScan 데이터 저장 변수
        self.laser_s = LaserScan()

    def update(self):
        """
        주기적으로 호출되어 LaserScan 데이터를 처리하는 함수
        여기에 SLAM 알고리즘을 구현할 수 있음
        """
        # === 알고리즘 구현 영역 ===
        # self.laser_s에 저장된 LaserScan 데이터를 사용하여
        # self.msg.data를 업데이트하는 코드를 작성
        
        # 예시:
        # 1. self.laser_s.ranges에서 거리 데이터 추출
        # 2. 각 거리 데이터를 좌표로 변환
        # 3. 해당 좌표의 맵 셀을 장애물(100)로 표시
        # 4. 로봇과 장애물 사이는 빈 공간(0)으로 표시
        
        pass  # 실제 구현은 학생이 작성

    def laser_cb(self, msg):
        """
        LaserScan 데이터를 수신하는 콜백
        
        Args:
            msg: LaserScan 메시지
                - ranges: 거리 측정값 배열
                - angle_min: 최소 각도
                - angle_max: 최대 각도
                - angle_increment: 각도 증분
                - range_min: 최소 측정 거리
                - range_max: 최대 측정 거리
        """
        # 수신한 LaserScan 데이터를 저장
        self.laser_s = msg

    def pub_cb(self):
        """
        맵을 발행하는 함수
        (publish_map.py와 동일)
        """
        # 타임스탬프 업데이트
        self.msg.header.stamp = self.get_clock().now().to_msg()

        # 현재 셀 인덱스 계산
        index = self.count + (self.msg.info.width * self.row)
        
        # 셀 값 토글
        if self.msg.data[index] == -1:
            self.msg.data[index] = 100
        else:
            self.msg.data[index] = -1

        # 다음 셀로 이동
        self.count += 1
        if self.count >= self.msg.info.width:
            self.count = 0
            self.row += 1
        if self.row >= self.msg.info.height:
            self.row = 0

        # 맵 발행
        self.pub.publish(self.msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Scan Map 노드 생성
    node = PublishMap()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
```

```shellscript
# 터미널 1: Gazebo + LiDAR 장착 로봇 실행
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 터미널 2: TF 발행
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom

# 터미널 3: Scan Map 노드 실행
ros2 run hello_ros2 scan_map

# 터미널 4: RViz로 시각화
rviz2
# Fixed Frame: map
# Add -> Map (Topic: /map)
# Add -> LaserScan (Topic: /scan)
```

---

**User**

launch 폴더의 모든 코드에 이해하기 쉽게 주석을 달아줘

---

**Cursor**

launch 폴더의 모든 코드에 상세한 주석을 달아드리겠습니다!

---

## 📄 1. message.launch.py (간단한 Launch 파일)

```python
"""
ROS2 Launch 파일 예제 - 기본
- 여러 노드를 동시에 실행하는 가장 간단한 형태
- simple_pub과 simple_sub 노드를 함께 실행
- Publisher와 Subscriber가 자동으로 통신
"""

from launch import LaunchDescription  # Launch 파일의 기본 클래스
from launch_ros.actions import Node  # ROS2 노드 실행 액션


def generate_launch_description():
    """
    Launch 파일의 필수 함수
    - ROS2 launch 시스템이 이 함수를 호출하여 실행할 내용을 가져옴
    - LaunchDescription 객체를 반환해야 함
    
    Returns:
        LaunchDescription: 실행할 노드 및 액션들의 목록
    """
    return LaunchDescription([
        # === Publisher 노드 실행 ===
        Node(
            package="hello_ros2",      # 패키지 이름
            executable="simple_pub"     # 실행할 노드 이름 (setup.py의 entry_points에 정의됨)
        ),
        
        # === Subscriber 노드 실행 ===
        Node(
            package="hello_ros2",       # 패키지 이름
            executable="simple_sub"     # 실행할 노드 이름
        )
    ])


"""
실행 방법:
-----------
ros2 launch hello_ros2 message.launch.py

설명:
----
1. simple_pub 노드가 /message 토픽으로 메시지를 발행
2. simple_sub 노드가 /message 토픽을 구독하여 메시지를 수신
3. 두 노드가 자동으로 통신하며 실행됨
4. Ctrl+C로 종료하면 두 노드 모두 종료됨

장점:
----
- 여러 터미널을 열 필요 없음
- 한 번의 명령으로 전체 시스템 실행
- 노드 간 실행 순서 및 의존성 관리 가능
"""
```

---

## 📄 2. moveTurtle.launch.py (고급 Launch 파일 - 파라미터 포함)

```python
"""
ROS2 Launch 파일 예제 - 고급
- 파라미터 파일(YAML)을 사용하여 노드 설정
- 여러 노드를 파라미터와 함께 실행
- Launch Argument를 사용한 유연한 설정
"""

# === 실행 방법 주석 ===
# ros2 param list                    # 파라미터 목록 확인
# ros2 param dump                     # 모든 파라미터 덤프
# ros2 param dump turtlesim           # turtlesim 노드의 파라미터만 덤프
# ros2 param dump turtlesim >> turtlesim.yaml  # 파일로 저장
# ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim.yaml  # 파라미터 파일로 실행
# ros2 launch hello_ros2 moveTurtle.launch.py  # Launch 파일로 실행

import os  # 운영체제 기능 (경로 처리)

from ament_index_python.packages import get_package_share_directory  # 패키지 경로 찾기
from launch import LaunchDescription  # Launch 기본 클래스
from launch.actions import DeclareLaunchArgument  # Launch 인자 선언
from launch.substitutions import LaunchConfiguration  # Launch 인자 사용
from launch_ros.actions import Node  # ROS2 노드 실행


def generate_launch_description():
    """
    고급 Launch Description 생성 함수
    - 파라미터 파일 경로를 Launch Argument로 설정 가능
    - 여러 노드를 파라미터와 함께 실행
    
    Returns:
        LaunchDescription: 실행할 노드들과 설정
    """
    
    # === 파라미터 파일 경로 설정 ===
    # LaunchConfiguration: Launch 시 전달되는 인자 값
    param_dir = LaunchConfiguration(
        "param_dir",  # 인자 이름
        default=os.path.join(  # 기본값 설정
            get_package_share_directory("hello_ros2"),  # hello_ros2 패키지의 설치 경로
            "param",  # param 디렉토리
            "turtlesim.yaml"  # 파라미터 파일 이름
        ),
    )
    
    # === LaunchDescription 반환 ===
    return LaunchDescription(
        [
            # === Launch Argument 선언 ===
            DeclareLaunchArgument(
                "param_dir",  # 인자 이름 (명령줄에서 param_dir:=값 형태로 전달 가능)
                default_value=param_dir,  # 기본값
                description="turtlesim paramdter dump file",  # 설명
            ),
            
            # === 노드 1: turtlesim_node ===
            Node(
                package="turtlesim",  # turtlesim 패키지 (ROS2 기본 패키지)
                executable="turtlesim_node",  # turtlesim 시뮬레이터 실행
                parameters=[param_dir]  # 파라미터 파일 로드
                # turtlesim.yaml의 /turtlesim 섹션 파라미터 적용됨
                # 예: background_r, background_g, background_b (배경색)
            ),
            
            # === 노드 2: move_turtle ===
            Node(
                package="hello_ros2",  # hello_ros2 패키지
                executable="move_turtle",  # 터틀 이동 노드
                parameters=[param_dir]  # 파라미터 파일 로드
                # turtlesim.yaml의 /move_turtle 섹션 파라미터 적용됨
                # 예: vel (선속도), angle_vel (각속도)
            ),
            
            # === 노드 3: change_color_client ===
            Node(
                package="hello_ros2",  # hello_ros2 패키지
                executable="change_color_client"  # 색상 변경 클라이언트
                # parameters 없음: 파라미터 파일 사용하지 않음
            ),
        ]
    )


"""
상세 설명:
---------

1. LaunchConfiguration과 DeclareLaunchArgument
   - LaunchConfiguration: Launch 인자의 값을 저장
   - DeclareLaunchArgument: Launch 인자를 선언하고 기본값 설정
   - 사용자가 명령줄에서 값을 변경 가능

2. get_package_share_directory()
   - 패키지가 설치된 share 디렉토리 경로를 반환
   - colcon build 후 install/share/패키지명/ 디렉토리
   - 파라미터 파일, Launch 파일 등이 이곳에 설치됨

3. os.path.join()
   - 플랫폼 독립적으로 경로를 결합
   - Windows: 역슬래시(\)
   - Linux/Mac: 슬래시(/)

4. parameters=[param_dir]
   - 노드에 파라미터 파일을 로드
   - YAML 파일의 해당 노드 섹션 파라미터가 적용됨


실행 방법:
---------

# 1. 기본 실행 (기본 파라미터 파일 사용)
ros2 launch hello_ros2 moveTurtle.launch.py

# 2. 커스텀 파라미터 파일 사용
ros2 launch hello_ros2 moveTurtle.launch.py param_dir:=/path/to/custom.yaml

# 3. Launch 파일 정보 확인
ros2 launch hello_ros2 moveTurtle.launch.py --show-args


실행 결과:
---------
1. turtlesim 창이 열림
   - 배경색이 turtlesim.yaml의 설정대로 변경됨
   - background_r: 10, background_g: 16, background_b: 200

2. 터틀이 자동으로 움직임
   - move_turtle 노드가 속도 명령을 전송
   - vel: 1.0 m/s, angle_vel: 3.0 rad/s

3. 터틀의 궤적 색상이 계속 변함
   - change_color_client 노드가 0.3초마다 색상 변경


파라미터 파일 (turtlesim.yaml) 구조:
-----------------------------------
/turtlesim:
  ros__parameters:
    background_r: 10      # 빨강 (0-255)
    background_g: 16      # 초록 (0-255)
    background_b: 200     # 파랑 (0-255)

/move_turtle:
  ros__parameters:
    vel: 1.0              # 선속도 (m/s)
    angle_vel: 3.0        # 각속도 (rad/s)


실시간 파라미터 변경:
-------------------
Launch 파일 실행 중에도 파라미터 변경 가능:

# 터틀 속도 변경
ros2 param set /move_turtle vel 2.0
ros2 param set /move_turtle angle_vel 5.0

# 배경색 변경 (실시간 반영 안 됨, 재시작 필요)
ros2 param set /turtlesim background_r 255


디버깅 팁:
---------
# Launch 파일 실행 중 노드 목록 확인
ros2 node list

# 각 노드의 파라미터 확인
ros2 param list
ros2 param get /turtlesim background_r
ros2 param get /move_turtle vel

# 토픽 통신 확인
ros2 topic list
ros2 topic echo /turtle1/cmd_vel
ros2 topic hz /turtle1/cmd_vel

# 서비스 확인
ros2 service list
ros2 service type /turtle1/set_pen


Launch 파일의 장점:
-----------------
1. 복잡한 시스템을 한 번에 실행
2. 노드 간 의존성 관리
3. 파라미터 중앙 관리
4. 재사용 가능한 설정
5. 환경에 따른 유연한 구성
"""
```

---

## 🎯 Launch 파일 비교

### message.launch.py (간단한 버전)
- **목적**: 기본적인 Publisher/Subscriber 예제
- **노드**: simple_pub, simple_sub
- **특징**: 
  - 파라미터 없음
  - 가장 간단한 형태
  - 학습용으로 적합

### moveTurtle.launch.py (고급 버전)
- **목적**: 실제 로봇 제어 시뮬레이션
- **노드**: turtlesim_node, move_turtle, change_color_client
- **특징**:
  - 파라미터 파일 사용
  - Launch Argument로 유연한 설정
  - 실전 프로젝트에 적용 가능

---

## 📚 Launch 파일 작성 패턴

### 기본 패턴:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package="패키지명", executable="노드명"),
    ])
```

### 파라미터 포함 패턴:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="패키지명",
            executable="노드명",
            parameters=[{"파라미터명": 값}]
        ),
    ])
```

### 파라미터 파일 사용 패턴:
```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    param_file = os.path.join(
        get_package_share_directory("패키지명"),
        "param", "파일명.yaml"
    )
    
    return LaunchDescription([
        Node(
            package="패키지명",
            executable="노드명",
            parameters=[param_file]
        ),
    ])
```

---

## 🚀 실습 가이드

### 1. message.launch.py 실행
```bash
# Launch 파일 실행
ros2 launch hello_ros2 message.launch.py

# 다른 터미널에서 확인
ros2 node list
ros2 topic list
ros2 topic echo /message
```

### 2. moveTurtle.launch.py 실행
```bash
# Launch 파일 실행
ros2 launch hello_ros2 moveTurtle.launch.py

# 실시간 파라미터 변경
ros2 param set /move_turtle vel 0.5
ros2 param set /move_turtle angle_vel 2.0

# 파라미터 확인
ros2 param list
ros2 param get /move_turtle vel
```

### 3. 커스텀 파라미터로 실행
```bash
# 먼저 현재 파라미터를 파일로 저장
ros2 param dump /turtlesim > my_params.yaml

# my_params.yaml 파일 수정 (배경색 변경 등)
# 그런 다음 커스텀 파라미터로 실행
ros2 launch hello_ros2 moveTurtle.launch.py param_dir:=/path/to/my_params.yaml
```

---

이제 launch 폴더의 모든 코드에 상세한 주석이 추가되었습니다! 두 Launch 파일을 비교하면서 ROS2 Launch 시스템의 기본부터 고급 기능까지 이해할 수 있을 것입니다! 😊

```python
"""
ROS2 Launch 파일 예제 - 기본
- 여러 노드를 동시에 실행하는 가장 간단한 형태
- simple_pub과 simple_sub 노드를 함께 실행
- Publisher와 Subscriber가 자동으로 통신
"""

from launch import LaunchDescription  # Launch 파일의 기본 클래스
from launch_ros.actions import Node  # ROS2 노드 실행 액션


def generate_launch_description():
    """
    Launch 파일의 필수 함수
    - ROS2 launch 시스템이 이 함수를 호출하여 실행할 내용을 가져옴
    - LaunchDescription 객체를 반환해야 함
    
    Returns:
        LaunchDescription: 실행할 노드 및 액션들의 목록
    """
    return LaunchDescription([
        # === Publisher 노드 실행 ===
        Node(
            package="hello_ros2",      # 패키지 이름
            executable="simple_pub"     # 실행할 노드 이름 (setup.py의 entry_points에 정의됨)
        ),
        
        # === Subscriber 노드 실행 ===
        Node(
            package="hello_ros2",       # 패키지 이름
            executable="simple_sub"     # 실행할 노드 이름
        )
    ])


"""
실행 방법:
-----------
ros2 launch hello_ros2 message.launch.py

설명:
----
1. simple_pub 노드가 /message 토픽으로 메시지를 발행
2. simple_sub 노드가 /message 토픽을 구독하여 메시지를 수신
3. 두 노드가 자동으로 통신하며 실행됨
4. Ctrl+C로 종료하면 두 노드 모두 종료됨

장점:
----
- 여러 터미널을 열 필요 없음
- 한 번의 명령으로 전체 시스템 실행
- 노드 간 실행 순서 및 의존성 관리 가능
"""
```

```python
"""
ROS2 Launch 파일 예제 - 고급
- 파라미터 파일(YAML)을 사용하여 노드 설정
- 여러 노드를 파라미터와 함께 실행
- Launch Argument를 사용한 유연한 설정
"""

# === 실행 방법 주석 ===
# ros2 param list                    # 파라미터 목록 확인
# ros2 param dump                     # 모든 파라미터 덤프
# ros2 param dump turtlesim           # turtlesim 노드의 파라미터만 덤프
# ros2 param dump turtlesim >> turtlesim.yaml  # 파일로 저장
# ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim.yaml  # 파라미터 파일로 실행
# ros2 launch hello_ros2 moveTurtle.launch.py  # Launch 파일로 실행

import os  # 운영체제 기능 (경로 처리)

from ament_index_python.packages import get_package_share_directory  # 패키지 경로 찾기
from launch import LaunchDescription  # Launch 기본 클래스
from launch.actions import DeclareLaunchArgument  # Launch 인자 선언
from launch.substitutions import LaunchConfiguration  # Launch 인자 사용
from launch_ros.actions import Node  # ROS2 노드 실행


def generate_launch_description():
    """
    고급 Launch Description 생성 함수
    - 파라미터 파일 경로를 Launch Argument로 설정 가능
    - 여러 노드를 파라미터와 함께 실행
    
    Returns:
        LaunchDescription: 실행할 노드들과 설정
    """
    
    # === 파라미터 파일 경로 설정 ===
    # LaunchConfiguration: Launch 시 전달되는 인자 값
    param_dir = LaunchConfiguration(
        "param_dir",  # 인자 이름
        default=os.path.join(  # 기본값 설정
            get_package_share_directory("hello_ros2"),  # hello_ros2 패키지의 설치 경로
            "param",  # param 디렉토리
            "turtlesim.yaml"  # 파라미터 파일 이름
        ),
    )
    
    # === LaunchDescription 반환 ===
    return LaunchDescription(
        [
            # === Launch Argument 선언 ===
            DeclareLaunchArgument(
                "param_dir",  # 인자 이름 (명령줄에서 param_dir:=값 형태로 전달 가능)
                default_value=param_dir,  # 기본값
                description="turtlesim paramdter dump file",  # 설명
            ),
            
            # === 노드 1: turtlesim_node ===
            Node(
                package="turtlesim",  # turtlesim 패키지 (ROS2 기본 패키지)
                executable="turtlesim_node",  # turtlesim 시뮬레이터 실행
                parameters=[param_dir]  # 파라미터 파일 로드
                # turtlesim.yaml의 /turtlesim 섹션 파라미터 적용됨
                # 예: background_r, background_g, background_b (배경색)
            ),
            
            # === 노드 2: move_turtle ===
            Node(
                package="hello_ros2",  # hello_ros2 패키지
                executable="move_turtle",  # 터틀 이동 노드
                parameters=[param_dir]  # 파라미터 파일 로드
                # turtlesim.yaml의 /move_turtle 섹션 파라미터 적용됨
                # 예: vel (선속도), angle_vel (각속도)
            ),
            
            # === 노드 3: change_color_client ===
            Node(
                package="hello_ros2",  # hello_ros2 패키지
                executable="change_color_client"  # 색상 변경 클라이언트
                # parameters 없음: 파라미터 파일 사용하지 않음
            ),
        ]
    )


"""
상세 설명:
---------

1. LaunchConfiguration과 DeclareLaunchArgument
   - LaunchConfiguration: Launch 인자의 값을 저장
   - DeclareLaunchArgument: Launch 인자를 선언하고 기본값 설정
   - 사용자가 명령줄에서 값을 변경 가능

2. get_package_share_directory()
   - 패키지가 설치된 share 디렉토리 경로를 반환
   - colcon build 후 install/share/패키지명/ 디렉토리
   - 파라미터 파일, Launch 파일 등이 이곳에 설치됨

3. os.path.join()
   - 플랫폼 독립적으로 경로를 결합
   - Windows: 역슬래시(\)
   - Linux/Mac: 슬래시(/)

4. parameters=[param_dir]
   - 노드에 파라미터 파일을 로드
   - YAML 파일의 해당 노드 섹션 파라미터가 적용됨


실행 방법:
---------

# 1. 기본 실행 (기본 파라미터 파일 사용)
ros2 launch hello_ros2 moveTurtle.launch.py

# 2. 커스텀 파라미터 파일 사용
ros2 launch hello_ros2 moveTurtle.launch.py param_dir:=/path/to/custom.yaml

# 3. Launch 파일 정보 확인
ros2 launch hello_ros2 moveTurtle.launch.py --show-args


실행 결과:
---------
1. turtlesim 창이 열림
   - 배경색이 turtlesim.yaml의 설정대로 변경됨
   - background_r: 10, background_g: 16, background_b: 200

2. 터틀이 자동으로 움직임
   - move_turtle 노드가 속도 명령을 전송
   - vel: 1.0 m/s, angle_vel: 3.0 rad/s

3. 터틀의 궤적 색상이 계속 변함
   - change_color_client 노드가 0.3초마다 색상 변경


파라미터 파일 (turtlesim.yaml) 구조:
-----------------------------------
/turtlesim:
  ros__parameters:
    background_r: 10      # 빨강 (0-255)
    background_g: 16      # 초록 (0-255)
    background_b: 200     # 파랑 (0-255)

/move_turtle:
  ros__parameters:
    vel: 1.0              # 선속도 (m/s)
    angle_vel: 3.0        # 각속도 (rad/s)


실시간 파라미터 변경:
-------------------
Launch 파일 실행 중에도 파라미터 변경 가능:

# 터틀 속도 변경
ros2 param set /move_turtle vel 2.0
ros2 param set /move_turtle angle_vel 5.0

# 배경색 변경 (실시간 반영 안 됨, 재시작 필요)
ros2 param set /turtlesim background_r 255


디버깅 팁:
---------
# Launch 파일 실행 중 노드 목록 확인
ros2 node list

# 각 노드의 파라미터 확인
ros2 param list
ros2 param get /turtlesim background_r
ros2 param get /move_turtle vel

# 토픽 통신 확인
ros2 topic list
ros2 topic echo /turtle1/cmd_vel
ros2 topic hz /turtle1/cmd_vel

# 서비스 확인
ros2 service list
ros2 service type /turtle1/set_pen


Launch 파일의 장점:
-----------------
1. 복잡한 시스템을 한 번에 실행
2. 노드 간 의존성 관리
3. 파라미터 중앙 관리
4. 재사용 가능한 설정
5. 환경에 따른 유연한 구성
"""
```

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package="패키지명", executable="노드명"),
    ])
```

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="패키지명",
            executable="노드명",
            parameters=[{"파라미터명": 값}]
        ),
    ])
```

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    param_file = os.path.join(
        get_package_share_directory("패키지명"),
        "param", "파일명.yaml"
    )
    
    return LaunchDescription([
        Node(
            package="패키지명",
            executable="노드명",
            parameters=[param_file]
        ),
    ])
```

```shellscript
# Launch 파일 실행
ros2 launch hello_ros2 message.launch.py

# 다른 터미널에서 확인
ros2 node list
ros2 topic list
ros2 topic echo /message
```

```shellscript
# Launch 파일 실행
ros2 launch hello_ros2 moveTurtle.launch.py

# 실시간 파라미터 변경
ros2 param set /move_turtle vel 0.5
ros2 param set /move_turtle angle_vel 2.0

# 파라미터 확인
ros2 param list
ros2 param get /move_turtle vel
```

```shellscript
# 먼저 현재 파라미터를 파일로 저장
ros2 param dump /turtlesim > my_params.yaml

# my_params.yaml 파일 수정 (배경색 변경 등)
# 그런 다음 커스텀 파라미터로 실행
ros2 launch hello_ros2 moveTurtle.launch.py param_dir:=/path/to/my_params.yaml
```

