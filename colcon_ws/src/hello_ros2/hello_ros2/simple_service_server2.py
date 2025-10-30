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
