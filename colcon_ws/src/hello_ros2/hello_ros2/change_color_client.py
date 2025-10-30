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
