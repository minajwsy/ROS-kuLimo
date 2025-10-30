"""
ROS2 Service Server 예제
- 클라이언트의 요청을 받아 처리하고 응답을 반환
- SetBool 서비스를 사용하여 bool 값 변경
"""

import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool  # 표준 Bool 설정 서비스


class Service_server(Node):
    """
    간단한 Service Server 노드
    SetBool 서비스를 제공하여 bool 값을 변경
    """
    
    def __init__(self):
        """Service Server 초기화"""
        # "service_server"라는 이름의 노드 생성
        super().__init__("service_server")
        
        # Service Server 생성
        # 첫 번째 인자: 서비스 타입 (SetBool)
        # 두 번째 인자: 서비스 이름 ("setBool")
        # 세 번째 인자: 콜백 함수 (요청 처리 함수)
        self.create_service(SetBool, "setBool", self.setBool_callback)
        
        # 내부 bool 상태 변수
        self.bool = False
        
        # 요청 카운터
        self.cnt = 0

    def setBool_callback(self, request: SetBool.Request, response: SetBool.Response):
        """
        서비스 요청을 처리하는 콜백 함수
        
        Args:
            request: 클라이언트로부터 받은 요청 (data: bool)
            response: 클라이언트에게 보낼 응답 (success: bool, message: string)
            
        Returns:
            response: 처리 결과가 담긴 응답 객체
        """
        # 서버의 작동 알고리즘
        
        # 로그 출력: 몇 번째 요청인지
        self.get_logger().info(f"{self.cnt}번째 요청 처리")
        
        # 로그 출력: 현재 bool 상태
        self.get_logger().info(f"현재 bool 정보 {self.bool}")
        
        # 로그 출력: 클라이언트가 요청한 값
        self.get_logger().info(f"변경 요청 값 {request.data}")
        
        # 요청 값과 현재 값이 다른 경우 (변경이 필요한 경우)
        if request.data != self.bool:
            self.bool = not self.bool  # 실제 데이터 변경
            response.success = True  # 성공 플래그 설정
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 성공"
        else:
            # 요청 값과 현재 값이 같은 경우 (변경 불필요)
            response.success = False  # 실패 플래그 설정
            response.message = f"{self.cnt}번째 요청 {self.bool} 변경 실패"
        
        # 처리 시간 시뮬레이션 (5초 대기)
        time.sleep(5)
        
        # 카운터 증가
        self.cnt += 1
        
        # 응답 반환
        return response


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Service Server 노드 생성
    node = Service_server()
    
    try:
        # 노드 실행 (서비스 요청 대기)
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
