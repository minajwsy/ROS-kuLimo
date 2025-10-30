"""
ROS2 Action Server 예제
- 장시간 실행되는 작업에 사용 (Service + Feedback)
- 피보나치 수열을 계산하며 중간 과정(feedback)을 전송
"""

# 명령줄로 액션 테스트:
# ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 15 }"

import time

import rclpy
from rclpy.action import ActionServer  # Action Server 클래스
from rclpy.action.server import ServerGoalHandle  # Goal 핸들러
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sympy import fibonacci  # 피보나치 수 계산 (사용되지 않음)
from user_interface.action import Fibonacci  # 커스텀 액션 타입


class Action_server(Node):
    """
    Fibonacci Action Server
    피보나치 수열을 계산하며 진행 상황을 피드백으로 전송
    """
    
    def __init__(self):
        """Action Server 초기화"""
        # "fibonacci_server"라는 이름의 노드 생성
        super().__init__("fibonacci_server")
        
        # ReentrantCallbackGroup 생성 (멀티스레드 처리용)
        self.callback_group = ReentrantCallbackGroup()
        
        # Action Server 생성
        # self: 노드 인스턴스
        # Fibonacci: 액션 타입
        # "fibonacci": 액션 이름
        # execute_callback: goal을 처리하는 함수
        self.action_server = ActionServer(
            self, 
            Fibonacci, 
            "fibonacci", 
            execute_callback=self.execute_callback
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        """
        Action goal을 처리하는 콜백 함수
        
        Args:
            goal_handle: goal 처리를 위한 핸들 객체
            
        Returns:
            result: 최종 결과 (피보나치 수열)
        """
        # goal에서 요청 데이터 추출
        request: Fibonacci.Goal = goal_handle.request
        self.get_logger().info(f"{request.step}")
        
        # Feedback 객체 생성 (중간 진행 상황 전송용)
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [0, 1]  # 피보나치 초기값
        
        # Result 객체 생성 (최종 결과 전송용)
        result = Fibonacci.Result()

        # 피보나치 수열 계산 (feedback 전송)
        for i in range(1, request.step):
            # 다음 피보나치 수 계산
            feedback.temp_seq.append(
                feedback.temp_seq[i] + feedback.temp_seq[i - 1]
            )
            
            # 피드백 발행 (클라이언트에게 중간 결과 전송)
            goal_handle.publish_feedback(feedback)
            
            # 1초 대기 (진행 상황 시뮬레이션)
            time.sleep(1)

        # 작업 완료 상태 설정
        print(type(goal_handle))
        goal_handle.succeed()  # 완료 status 보내기
        # goal_handle.abort()  # aborted 상태로 보내기 (실패 시)
        
        # 최종 결과 설정
        result.seq = feedback.temp_seq
        
        # result 반환 (action 종료)
        return result


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Action Server 노드 생성
    node = Action_server()
    
    # MultiThreadedExecutor 생성 (5개 스레드)
    # 피드백을 보내면서 다른 작업도 처리할 수 있도록
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
