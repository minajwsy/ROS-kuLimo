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
