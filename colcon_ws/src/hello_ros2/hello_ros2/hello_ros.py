
"""
📚 학습 순서 추천 by Claude4.5:
기초 (1-5): hello_ros → simple_pub/sub → service → action → parameter
응용 (6-12): move_turtle → tf_listener → dynamic_tf → follow_turtlesim
고급 (13-20): custom messages → navigation → mapping
---------------------------------------------------
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
