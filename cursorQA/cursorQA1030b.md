# 코드 해설 및 실습 방법 설명
_Exported on 2025. 10. 30. at 17시 39분 48초 GMT+9 from Cursor (2.0.38)_

---

**User**

[Code해설] 이 디렉토리는 실제 진행되었던 수업 내용에 대한 기록이야. 이를 분석해서 hello_ros2 폴더의 코드 내용을 해설하고, 실습하는 방법까지 같이 이해하기 쉽게 설명해줘. 수업내용을 제대로 이해하지 못해서 그래

---

**Cursor**

## 패키지 개요
- `hello_ros2`는 `ament_python` 기반 ROS2 예제 묶음으로, `setup.py`의 `console_scripts`에서 각 노드를 실행 엔트리로 노출합니다.  
```32:52:colcon_ws/src/hello_ros2/setup.py
    entry_points={
        "console_scripts": [
            "hello_ros = hello_ros2.hello_ros:main",
            "simple_pub = hello_ros2.simple_pub:main",
            "simple_sub = hello_ros2.simple_sub:main",
            "simple_service_client = hello_ros2.simple_service_client:main",
            "action_server = hello_ros2.action_server:main",
            "follow_turtlesim = hello_ros2.follow_turtlesim:main",
        ],
    },
```
- `launch/`, `param/`, `resource/`까지 설치에 포함되므로 `colcon build` 후 어느 워크스페이스에서도 동일하게 실행할 수 있습니다.

## 핵심 예제 해설
- **기초 노드**: `hello_ros`는 노드 상속, 타이머 생성, 간단한 출력 구조를 익히기 위한 최소 예제입니다.  
```27:52:colcon_ws/src/hello_ros2/hello_ros2/hello_ros.py
class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.create_timer(1, self.print_hello)
        self.count = 0

    def print_hello(self):
        print(f"hello, ROS2 humble!! {self.count}")
        self.count += 1
```
- **토픽 통신**: `simple_pub`/`simple_sub`가 10Hz 주기로 문자열을 발행·수신하며 QoS 의 기본 인자를 체험하게 해 줍니다.  
```13:48:colcon_ws/src/hello_ros2/hello_ros2/simple_pub.py
class Simple_pub(Node):
    def __init__(self):
        super().__init__('simple_pub')
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(String, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = String()
        msg.data = f'hello, ros2 {self.count}'
        self.pub.publish(msg)
        self.count += 1
```
```12:39:colcon_ws/src/hello_ros2/hello_ros2/simple_sub.py
class Simple_sub(Node):
    def __init__(self):
        super().__init__('simple_sub')
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        self.get_logger().info(msg.data)
```
- **서비스 패턴**: `simple_service_server`/`simple_service_server2`는 단일 스레드와 `ReentrantCallbackGroup`+`MultiThreadedExecutor`의 차이를 보여주고, `simple_service_client`는 비동기 `call_async`와 `Future` 콜백 체인을 실습하도록 구성되어 있습니다.  
```26:82:colcon_ws/src/hello_ros2/hello_ros2/simple_service_client.py
class Service_client(Node):
    def __init__(self):
        super().__init__("service_client")
        self.client = self.create_client(SetBool, "setBool")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        self.create_timer(1, self.update)
        self.create_timer(2, self.send_request)
        self.request = SetBool.Request()
        self.future = Future()

    def send_request(self):
        self.request.data = not self.request.data
        self.future = self.client.call_async(self.request)
        self.future.add_done_callback(self.done_callback)
```
- **파라미터와 커스텀 메시지**: `simple_parameter`는 파라미터 선언·변경 콜백을 실시간으로 확인하게 해 주며, `my_topic_pub`은 `user_interface` 패키지의 커스텀 메시지를 퍼블리시하는 구조입니다.  
```25:60:colcon_ws/src/hello_ros2/hello_ros2/simple_parameter.py
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
        self.set_parameters([
            Parameter("para1", Parameter.Type.INTEGER, self.para1)
        ])
```
- **액션**: `action_server`/`action_client`는 Fibonacci 계산을 통해 goal 수락, 진행 피드백, 결과 확인 전체 흐름을 다룹니다.  
```28:88:colcon_ws/src/hello_ros2/hello_ros2/action_server.py
class Action_server(Node):
    def __init__(self):
        super().__init__("fibonacci_server")
        self.callback_group = ReentrantCallbackGroup()
        self.action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci",
            execute_callback=self.execute_callback
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [0, 1]
        for i in range(1, goal_handle.request.step):
            feedback.temp_seq.append(
                feedback.temp_seq[i] + feedback.temp_seq[i - 1]
            )
            goal_handle.publish_feedback(feedback)
            time.sleep(1)
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.seq = feedback.temp_seq
        return result
```
- **Turtlesim + Launch**: `move_turtle`는 파라미터 기반 속도 제어, `change_color_client`는 `SetPen` 서비스 호출을 담당하며, 두 노드는 `moveTurtle.launch.py`로 한 번에 기동할 수 있습니다.  
```35:80:colcon_ws/src/hello_ros2/launch/moveTurtle.launch.py
    param_dir = LaunchConfiguration(
        "param_dir",
        default=os.path.join(
            get_package_share_directory("hello_ros2"),
            "param",
            "turtlesim.yaml"
        ),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("param_dir", default_value=param_dir),
            Node(package="turtlesim", executable="turtlesim_node", parameters=[param_dir]),
            Node(package="hello_ros2", executable="move_turtle", parameters=[param_dir]),
            Node(package="hello_ros2", executable="change_color_client"),
        ]
    )
```
- **TF 학습**: `dynamic_tf`로 변환을 방송하고 `tf_listener`로 조회하는 기초를 익힌 뒤, `follow_turtlesim`에서 Transform 조회와 속도 제어를 결합해 turtle2가 turtle1을 추적하도록 만듭니다.  
```42:205:colcon_ws/src/hello_ros2/hello_ros2/follow_turtlesim.py
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.1, self.on_timer)
        self.tf_br = TransformBroadcaster(self)
        self.spawner = self.create_client(Spawn, "spawn")
        self.sub = self.create_subscription(Pose, "/turtle1/pose", self.sub_cb, 10)
        self.sub2 = self.create_subscription(Pose, "/turtle2/pose", self.sub_cb2, 10)
        self.pub = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform("turtle2", "turtle1", time.Time())
        except Exception as e:
            self.get_logger().info(f"Lookup transform 실패!!: {e}")
            return
        msg = Twist()
        angle_error_rad = math.atan2(
            t.transform.translation.y,
            t.transform.translation.x,
        )
        if angle_error_rad > 0.1:
            msg.angular.z = 4.0
        elif angle_error_rad < -0.1:
            msg.angular.z = -4.0
        else:
            msg.angular.z = 0.0
        distance = math.sqrt(
            t.transform.translation.x**2 + t.transform.translation.y**2
        )
        msg.linear.x = 2.0 if distance > 0.2 else 0.0
        self.pub.publish(msg)
```
- **맵·내비게이션**: `publish_map`은 OccupancyGrid 생성·발행 루프, `scan_map`은 LiDAR 구독 구조를 제공하며, `patrol`은 Nav2 `FollowWaypoints` 액션을 이용해 다중 목표 순찰을 구현합니다.  
```24:107:colcon_ws/src/hello_ros2/hello_ros2/publish_map.py
class PublishMap(Node):
    def __init__(self):
        super().__init__("publish_map")
        self.create_timer(0.001, self.pub_cb)
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        self.msg = OccupancyGrid()
        self.msg.info.resolution = 0.1
        self.msg.info.width = 200
        self.msg.info.height = 100
        self.msg.data = [100 for _ in range(10_000)]
        self.msg.data.extend([0 for _ in range(10_000)])
        self.count = 0
        self.row = 0

    def pub_cb(self):
        self.msg.header.stamp = self.get_clock().now().to_msg()
        index = self.count + (self.msg.info.width * self.row)
        if self.msg.data[index] == -1:
            self.msg.data[index] = 100
        else:
            self.msg.data[index] = -1
        self.count += 1
        if self.count >= self.msg.info.width:
            self.count = 0
            self.row += 1
        if self.row >= self.msg.info.height:
            self.row = 0
        self.pub.publish(self.msg)
```
```46:148:colcon_ws/src/hello_ros2/hello_ros2/patrol.py
        self.patrol_points = [(4.0, 0.0), (4.0, 1.0), (2.0, 2.5), (0.0, 1.0)]
        self.patrol_degree = [0, 90, 180, 90]
        self.patrol_index = 0
        self.goal = FollowWaypoints.Goal()
        self.go_next()

    def send_goal(self, x: float, y: float, theta: int):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        rad = math.radians(theta)
        pose.pose.orientation.z = math.sin(rad / 2.0)
        pose.pose.orientation.w = math.cos(rad / 2.0)
        self.goal.poses.clear()
        self.goal.poses.append(pose)
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("nav2 서버 접속중 ...")
        self.future = self.action_client.send_goal_async(
            self.goal,
            feedback_callback=self.feedback_callback
        )
        self.future.add_done_callback(self.goal_response_callback)
```
- **Limo 제어**: `move_limo`는 `/cmd_vel` 토픽과 파라미터를 사용해 실제 혹은 Gazebo Limo를 제어하도록 구조화되었습니다.  
```24:84:colcon_ws/src/hello_ros2/hello_ros2/move_limo.py
class Move_turtle(Node):
    def __init__(self):
        super().__init__("move_limo")
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.declare_parameter("vel", 1.0)
        self.declare_parameter("angle_vel", 1.2)
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value
        self.add_on_set_parameters_callback(self.param_callback)

    def pub_turtle(self):
        msg = Twist()
        msg.angular.z = self.angle_vel
        msg.linear.x = self.vel
        self.pub.publish(msg)
```

## 실습 가이드
- 빌드 준비: `cd colcon_ws`, (가상환경/ROS2 humble) `colcon build --packages-select hello_ros2`.  
- 환경 설정: 신규 터미널마다 `source install/local_setup.bash` (Windows PowerShell이면 `install\local_setup.ps1`).  
- 단일 노드 실행: `ros2 run hello_ros2 hello_ros` 처럼 `setup.py`에 등록된 이름 사용.  
- 퍼블리셔·서브스크립터 동시 실행: `ros2 launch hello_ros2 message.launch.py`.  
- 서비스 비교 실습: 서버1 `ros2 run hello_ros2 simple_service_server`, 서버2 `ros2 run hello_ros2 simple_service_server2`, 클라이언트 `ros2 run hello_ros2 simple_service_client`를 각각 다른 터미널에서 실행하고 응답 지연과 동시 처리 차이를 관찰.  
- 파라미터 조작: `ros2 run hello_ros2 simple_parameter --ros-args -p para1:=5` 실행 후 `ros2 param set /simple_parameter para1 100`으로 외부 설정을 시험.  
- Turtlesim 시나리오: `ros2 launch hello_ros2 moveTurtle.launch.py` 실행, `ros2 param set /move_turtle vel 2.0`으로 실시간 속도 조절, `ros2 topic echo /turtle2/pose` 등으로 상태 확인.  
- TF/액션/네비게이션: Turtlesim과 RViz, Nav2는 각각의 선행 노드(`turtlesim_node`, `rviz2`, `navigation2.launch.py`)를 올려둔 뒤 예제 실행. TF 관련 패키지(`tf-transformations`)는 사전에 설치해야 합니다.  
- Limo/Gazebo: `ros2 launch limo_description gazebo_models_diff.launch.py`로 시뮬레이터를 켠 뒤 `ros2 run hello_ros2 move_limo`로 제어. 파라미터를 바꿔 각속도/선속도 반응을 확인.

## 추천 학습 흐름
- 수업 메모에 적힌 순서처럼 기초(Hello → Pub/Sub → Service → Action → Parameter)에서 시작해 응용(Turtlesim 제어, TF) → 고급(커스텀 메시지, Nav2 순찰, 맵 발행)으로 확장하면 이해가 수월합니다.  
- 각 단계에서 `ros2 topic list`, `ros2 service list`, `ros2 action list`, `ros2 param list`로 통신 상태를 확인하고, RViz나 `ros2 topic echo`를 함께 사용하면 데이터 흐름이 눈에 보입니다.  
- 마지막으로 `scan_map`의 `update()`처럼 빈 영역으로 남겨둔 함수에 직접 알고리즘을 채워 넣어보면 SLAM·센서 융합의 기반 개념을 실습형으로 복습할 수 있습니다.

```python
    entry_points={
        "console_scripts": [
            "hello_ros = hello_ros2.hello_ros:main",
            "simple_pub = hello_ros2.simple_pub:main",
            "simple_sub = hello_ros2.simple_sub:main",
            "simple_service_client = hello_ros2.simple_service_client:main",
            "action_server = hello_ros2.action_server:main",
            "follow_turtlesim = hello_ros2.follow_turtlesim:main",
        ],
    },
```

```python
class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.create_timer(1, self.print_hello)
        self.count = 0

    def print_hello(self):
        print(f"hello, ROS2 humble!! {self.count}")
        self.count += 1
```

```python
class Simple_pub(Node):
    def __init__(self):
        super().__init__('simple_pub')
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(String, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = String()
        msg.data = f'hello, ros2 {self.count}'
        self.pub.publish(msg)
        self.count += 1
```

```python
class Simple_sub(Node):
    def __init__(self):
        super().__init__('simple_sub')
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        self.get_logger().info(msg.data)
```

```python
class Service_client(Node):
    def __init__(self):
        super().__init__("service_client")
        self.client = self.create_client(SetBool, "setBool")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")
        self.create_timer(1, self.update)
        self.create_timer(2, self.send_request)
        self.request = SetBool.Request()
        self.future = Future()

    def send_request(self):
        self.request.data = not self.request.data
        self.future = self.client.call_async(self.request)
        self.future.add_done_callback(self.done_callback)
```

```python
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
        self.set_parameters([
            Parameter("para1", Parameter.Type.INTEGER, self.para1)
        ])
```

```python
class Action_server(Node):
    def __init__(self):
        super().__init__("fibonacci_server")
        self.callback_group = ReentrantCallbackGroup()
        self.action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci",
            execute_callback=self.execute_callback
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [0, 1]
        for i in range(1, goal_handle.request.step):
            feedback.temp_seq.append(
                feedback.temp_seq[i] + feedback.temp_seq[i - 1]
            )
            goal_handle.publish_feedback(feedback)
            time.sleep(1)
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.seq = feedback.temp_seq
        return result
```

```python
    param_dir = LaunchConfiguration(
        "param_dir",
        default=os.path.join(
            get_package_share_directory("hello_ros2"),
            "param",
            "turtlesim.yaml"
        ),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("param_dir", default_value=param_dir),
            Node(package="turtlesim", executable="turtlesim_node", parameters=[param_dir]),
            Node(package="hello_ros2", executable="move_turtle", parameters=[param_dir]),
            Node(package="hello_ros2", executable="change_color_client"),
        ]
    )
```

```python
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.1, self.on_timer)
        self.tf_br = TransformBroadcaster(self)
        self.spawner = self.create_client(Spawn, "spawn")
        self.sub = self.create_subscription(Pose, "/turtle1/pose", self.sub_cb, 10)
        self.sub2 = self.create_subscription(Pose, "/turtle2/pose", self.sub_cb2, 10)
        self.pub = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform("turtle2", "turtle1", time.Time())
        except Exception as e:
            self.get_logger().info(f"Lookup transform 실패!!: {e}")
            return
        msg = Twist()
        angle_error_rad = math.atan2(
            t.transform.translation.y,
            t.transform.translation.x,
        )
        if angle_error_rad > 0.1:
            msg.angular.z = 4.0
        elif angle_error_rad < -0.1:
            msg.angular.z = -4.0
        else:
            msg.angular.z = 0.0
        distance = math.sqrt(
            t.transform.translation.x**2 + t.transform.translation.y**2
        )
        msg.linear.x = 2.0 if distance > 0.2 else 0.0
        self.pub.publish(msg)
```

```python
class PublishMap(Node):
    def __init__(self):
        super().__init__("publish_map")
        self.create_timer(0.001, self.pub_cb)
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        self.msg = OccupancyGrid()
        self.msg.info.resolution = 0.1
        self.msg.info.width = 200
        self.msg.info.height = 100
        self.msg.data = [100 for _ in range(10_000)]
        self.msg.data.extend([0 for _ in range(10_000)])
        self.count = 0
        self.row = 0

    def pub_cb(self):
        self.msg.header.stamp = self.get_clock().now().to_msg()
        index = self.count + (self.msg.info.width * self.row)
        if self.msg.data[index] == -1:
            self.msg.data[index] = 100
        else:
            self.msg.data[index] = -1
        self.count += 1
        if self.count >= self.msg.info.width:
            self.count = 0
            self.row += 1
        if self.row >= self.msg.info.height:
            self.row = 0
        self.pub.publish(self.msg)
```

```python
        self.patrol_points = [(4.0, 0.0), (4.0, 1.0), (2.0, 2.5), (0.0, 1.0)]
        self.patrol_degree = [0, 90, 180, 90]
        self.patrol_index = 0
        self.goal = FollowWaypoints.Goal()
        self.go_next()

    def send_goal(self, x: float, y: float, theta: int):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        rad = math.radians(theta)
        pose.pose.orientation.z = math.sin(rad / 2.0)
        pose.pose.orientation.w = math.cos(rad / 2.0)
        self.goal.poses.clear()
        self.goal.poses.append(pose)
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("nav2 서버 접속중 ...")
        self.future = self.action_client.send_goal_async(
            self.goal,
            feedback_callback=self.feedback_callback
        )
        self.future.add_done_callback(self.goal_response_callback)
```

```python
class Move_turtle(Node):
    def __init__(self):
        super().__init__("move_limo")
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.declare_parameter("vel", 1.0)
        self.declare_parameter("angle_vel", 1.2)
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value
        self.add_on_set_parameters_callback(self.param_callback)

    def pub_turtle(self):
        msg = Twist()
        msg.angular.z = self.angle_vel
        msg.linear.x = self.vel
        self.pub.publish(msg)
```

---

**User**

rclpy 패키지에 대해 소개해

---

**Cursor**

## rclpy 개요
- `rclpy`는 ROS 2의 **Python 클라이언트 라이브러리**로, ROS 2 미들웨어(`rmw`) 위에 Python 바인딩을 제공해 노드, 토픽, 서비스, 액션, 파라미터 등을 Python 코드에서 직접 다룰 수 있게 합니다.
- 설계는 C 계층(`rcl`) 위에 얇은 래퍼를 두는 구조로, `rclcpp`(C++)와 동일한 통신 모델을 공유하므로 언어만 다를 뿐 기능은 거의 동일합니다.
- `ament_python` 패키지를 빌드하면 `rclpy`에 의존하여 `ros2 run 패키지명 노드명` 형태로 Python 스크립트를 실행할 수 있습니다.

## 핵심 구성 요소
- **Node**: `rclpy.node.Node` 클래스는 ROS 2 노드의 기반으로, 생성자로 이름을 지정하고 퍼블리셔·서브스크립션·서비스·타이머 등을 등록합니다.
- **Publisher / Subscription**: `create_publisher`, `create_subscription`으로 DDS 토픽을 연결합니다. 큐 크기와 QoS 설정을 인자로 전달할 수 있습니다.
- **Service / Client**: `create_service`, `create_client`로 요청-응답 구조를 구현합니다. `call_async` + `Future` 패턴이 기본이며, `wait_for_service`로 서버 준비 여부를 확인합니다.
- **Action**: `ActionServer`, `ActionClient` 클래스를 제공하여 장시간 작업에 대한 goal/feedback/result 흐름을 Python에서 구현할 수 있습니다.
- **파라미터**: `declare_parameter`, `get_parameter`, `set_parameters` 등을 통해 런타임 파라미터를 선언하고 변경 가능하며, `add_on_set_parameters_callback`으로 실시간 변경을 감지할 수 있습니다.
- **타이머 & Executor**: `create_timer`로 주기 실행 콜백을 만들고, `rclpy.spin()` 또는 `MultiThreadedExecutor`를 이용해 이벤트 루프를 유지합니다. 멀티스레드 처리 시 `ReentrantCallbackGroup`을 함께 사용합니다.
- **로그·시간**: `node.get_logger()`로 ROS 2 로그 시스템을 활용하고, `node.get_clock()`에서 ROS 시간을 얻어 메시지 타임스탬프나 TF 계산에 활용합니다.

## 설치 및 사용
- ROS 2 배포판(humble, iron 등)을 설치하면 `rclpy`가 함께 제공되며, 별도 pip 설치 없이 사용합니다. 가상환경에서 필요하면 `sudo apt install ros-<배포판>-rclpy`로 설치 확인이 가능합니다.
- 스크립트는 shebang 없이도 `console_scripts` 엔트리(예: `hello_ros = hello_ros2.hello_ros:main`)로 등록해 `ros2 run` 명령으로 실행합니다.
- 일반 Python 스크립트 실행 시에도 `rclpy.init()`, `rclpy.shutdown()` 호출을 사용하면 됩니다.

## 관련 자료
- 공식 문서: https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/ (Python 섹션 참조)
- ROS 2 예제 패키지: `ros2 run demo_nodes_py talker` 등으로 기본 퍼블리셔/서브스크립션 구조를 빠르게 확인할 수 있습니다.
- 고급 주제: QoS 프로파일 설정, Executor 커스터마이징, TF2(`tf_transformations`), Lifecycle 노드(`rclpy.lifecycle`) 등도 `rclpy`에서 지원합니다.

정리하면 `rclpy`는 ROS 2 시스템의 거의 모든 기능을 Python 코드로 구현할 수 있게 해 주는 핵심 라이브러리이며, 험블과 같은 최신 배포판에서 기본적으로 포함되어 있습니다.

---

**User**

토픽의 발행자 및 구독자 코드로 실험 하는 방법을 구체적으로 알려줘 

---

**Cursor**

## 토픽 퍼블리셔·서브스크라이버 실험 절차

- **코드 이해하기**  
  - 퍼블리셔 `simple_pub`는 0.1초마다 `/message` 토픽에 문자열 메시지를 발행합니다.  
```13:48:colcon_ws/src/hello_ros2/hello_ros2/simple_pub.py
class Simple_pub(Node):
    def __init__(self):
        super().__init__('simple_pub')
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(String, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = String()
        msg.data = f'hello, ros2 {self.count}'
        self.pub.publish(msg)
        self.count += 1
```
  - 서브스크라이버 `simple_sub`는 같은 토픽을 구독해 들어온 문자열을 로그로 출력합니다.  
```12:39:colcon_ws/src/hello_ros2/hello_ros2/simple_sub.py
class Simple_sub(Node):
    def __init__(self):
        super().__init__('simple_sub')
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        self.get_logger().info(msg.data)
```

- **빌드 및 환경 준비**  
  - `colcon_ws`에서 `colcon build --packages-select hello_ros2` 실행.  
  - 새 터미널마다 `source install/local_setup.bash` (Windows PowerShell이면 `install\local_setup.ps1`)로 환경 설정.

- **단일 노드 테스트**  
  - 터미널 A: `ros2 run hello_ros2 simple_pub`  
  - 터미널 B: `ros2 run hello_ros2 simple_sub`  
  - 터미널 C(선택): `ros2 topic echo /message`로 데이터 스트림 확인.  
  - 기대 결과: 퍼블리셔가 `hello, ros2 N` 메시지를 계속 보내고, 서브스크라이버와 `ros2 topic echo`가 동일한 문자열을 즉시 표시.

- **토픽 상태 점검**  
  - `ros2 topic list`로 `/message` 토픽 존재 확인.  
  - `ros2 topic info /message`로 퍼블리셔/서브스크라이버 수와 타입 확인.  
  - `ros2 interface show std_msgs/msg/String`으로 메시지 타입 구조 재확인.  
  - 성능 측정: `ros2 topic hz /message`로 발행 주기(약 10Hz) 확인.

- **Launch 파일로 한 번에 실행**  
  - 한 명령으로 퍼블리셔와 서브스크라이버를 동시에 실행하려면:  
    - `ros2 launch hello_ros2 message.launch.py`  
    - 다른 터미널에서 `ros2 topic echo /message`로 모니터링.  
  - 종료 시 Launch 프로세스에서 `Ctrl+C` 하면 두 노드가 함께 종료됨.

- **실험 응용 아이디어**  
  - `simple_pub`를 실행 중에 `ros2 param set /simple_pub use_sim_time true` 등 파라미터 테스트(해당 노드는 파라미터 사용 X이지만 방법 학습).  
  - 토픽 이름 변경 시험: 코드에서 `"/message"` 대신 `"/test_message"`로 바꾸고 동일한 절차를 반복해 연결 실패/성공을 비교(Ask 모드에서는 직접 수정 대신 복사본으로 실습).  
  - QoS 확인: 발행/수신 사이에 `ros2 topic bw /message`로 메시지 대역폭 측정.

- **문제 발생 시 체크리스트**  
  - `source install/local_setup.bash`를 잊지 않았는지 확인.  
  - 노드 이름 충돌 여부: 동일 이름 노드 여러 개 실행 시 경고가 나오면 `--ros-args -r __node:=새이름`으로 재명명.  
  - 다른 ROS 2 워크스페이스가 먼저 소싱된 경우 `printenv | grep ROS`로 환경 변수 확인 후 순서 재조정.

이 순서를 따르면 퍼블리셔/서브스크라이버 구조를 눈으로 확인하면서 ROS 2 토픽 통신의 핵심 개념(토픽 이름, 메시지 타입, QoS 큐 등)을 실습형으로 익힐 수 있습니다.

```python
class Simple_pub(Node):
    def __init__(self):
        super().__init__('simple_pub')
        self.create_timer(0.1, self.pub_turtle)
        self.pub = self.create_publisher(String, "/message", 10)
        self.count = 0

    def pub_turtle(self):
        msg = String()
        msg.data = f'hello, ros2 {self.count}'
        self.pub.publish(msg)
        self.count += 1
```

```python
class Simple_sub(Node):
    def __init__(self):
        super().__init__('simple_sub')
        self.create_subscription(String, 'message', self.sub_callback, 10)

    def sub_callback(self, msg: String):
        self.get_logger().info(msg.data)
```

