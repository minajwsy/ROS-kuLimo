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
