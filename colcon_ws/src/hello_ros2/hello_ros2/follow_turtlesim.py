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
