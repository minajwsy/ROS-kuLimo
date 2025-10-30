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
