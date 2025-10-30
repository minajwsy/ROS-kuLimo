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
