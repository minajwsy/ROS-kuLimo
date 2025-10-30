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
