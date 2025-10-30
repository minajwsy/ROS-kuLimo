"""
ROS2 커스텀 Service Server 예제
- user_interface 패키지의 AddTwoInts 서비스 사용
- 두 정수를 더하는 서비스 제공
- 멀티스레드로 동작
"""

import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from user_interface.srv import AddTwoInts  # 커스텀 서비스 타입


class Service_server(Node):
    """
    두 정수를 더하는 서비스를 제공하는 서버
    요청에 포함된 a와 b를 더한 결과를 반환
    """
    
    def __init__(self):
        """Add Service Server 초기화"""
        # "add_service_server"라는 이름의 노드 생성
        super().__init__("add_service_server")
        
        # ReentrantCallbackGroup 생성 (동시 요청 처리용)
        self.callback_group = ReentrantCallbackGroup()
        
        # Service Server 생성
        self.create_service(
            AddTwoInts,  # 서비스 타입
            "add_ints",  # 서비스 이름
            self.setBool_callback,  # 콜백 함수
            callback_group=self.callback_group,  # 콜백 그룹
        )

    def setBool_callback(
        self, request: AddTwoInts.Request, response: AddTwoInts.Response
    ):
        """
        덧셈 서비스 요청을 처리하는 콜백
        
        Args:
            request: 요청 (header, a, b, op)
            response: 응답 (success, result, message)
            
        Returns:
            response: 처리된 응답
        """
        # 서버의 작동 알고리즘
        
        # 요청 시간 로그 출력
        self.get_logger().info(f"{request.header.stamp} 시간")
        
        # 요청 값 로그 출력
        self.get_logger().info(f"a : {request.a}")
        self.get_logger().info(f"b : {request.b}")
        
        # 덧셈 수행
        response.result = request.a + request.b
        
        # 성공 플래그 설정
        response.success = True
        
        # 응답 메시지 설정
        response.message = "a 와 b 의 값을 더해서 반환 했다!"
        
        # 처리 시간 시뮬레이션 (5초 대기)
        time.sleep(5)
        
        # 응답 반환
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Add Service Server 노드 생성
    node = Service_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    executor = MultiThreadedExecutor(num_threads=5)
    
    # Executor에 노드 추가
    executor.add_node(node)
    
    try:
        # Executor 실행
        executor.spin()
    except KeyboardInterrupt:
        # 종료 시 정리
        executor.shutdown()
        node.destroy_node()


if __name__ == "__main__":
    main()
