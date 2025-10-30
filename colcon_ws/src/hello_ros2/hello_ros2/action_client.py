"""
ROS2 Action Client 예제
- Action 서버에 goal을 전송하고 피드백과 결과를 받음
- 피보나치 수열 계산을 요청
"""

# 명령줄로 액션 테스트:
# ros2 action send_goal --feedback /fibonacci user_interface/Fibonacci "{step: 15 }"

import time

import rclpy
from action_msgs.msg import GoalStatus  # Goal 상태 (성공, 실패 등)
from rclpy.action import ActionClient  # Action Client 클래스
from rclpy.action.client import ClientGoalHandle  # Client Goal 핸들러
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.task import Future  # 비동기 작업용 Future
from user_interface.action import Fibonacci  # 커스텀 액션 타입
from user_interface.action._fibonacci import Fibonacci_GetResult_Response


class Action_client(Node):
    """
    Fibonacci Action Client
    피보나치 계산을 요청하고 피드백과 결과를 받음
    """
    
    def __init__(self):
        """Action Client 초기화"""
        # "fibonacci_client"라는 이름의 노드 생성
        super().__init__("fibonacci_client")
        
        # ReentrantCallbackGroup 생성
        self.callback_group = ReentrantCallbackGroup()
        
        # Action Client 생성
        # self: 노드 인스턴스
        # Fibonacci: 액션 타입
        # "fibonacci": 액션 이름
        self.action_client = ActionClient(self, Fibonacci, "fibonacci")
        
        # Future 객체들 초기화
        self.future = Future()  # goal 전송용
        self.get_result_future = Future()  # 결과 수신용
        
        # 서버 접속 대기
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("피보나치 서버 접속중 ...")
        
        # goal 전송
        self.send_goal()

    def send_goal(self):
        """
        Action 서버에 goal을 전송하는 함수
        """
        # Goal 객체 생성
        goal = Fibonacci.Goal()
        goal.step = 8  # 피보나치 8단계 요청
        
        # 비동기로 goal 전송
        # feedback_callback: 피드백 수신 시 호출될 함수
        self.future: Future = self.action_client.send_goal_async(
            goal, 
            feedback_callback=self.feedback_callback
        )
        
        # goal 응답이 도착하면 goal_response_callback 호출
        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future):
        """
        goal이 서버에 접수되었는지 확인하는 콜백
        (ROS1에는 없던 체크 포인트)
        
        Args:
            future: goal 전송 결과가 담긴 Future
        """
        # goal 핸들 추출
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        
        # goal이 거부된 경우
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        
        # goal이 접수된 경우, 결과를 비동기로 요청
        self.get_result_future: Future = goal_handle.get_result_async()
        
        # 결과가 도착하면 done_callback 호출
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        """
        Action 실행 중 피드백이 도착할 때마다 호출되는 콜백
        
        Args:
            msg: 피드백 메시지
        """
        # 피드백에서 데이터 추출
        feedback: Fibonacci.Feedback = msg.feedback
        
        # 지금까지의 계산 결과 출력
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.temp_seq}")

    def done_callback(self, future: Future):
        """
        Action이 완료되었을 때 호출되는 콜백
        최종 결과를 처리
        
        Args:
            future: 결과가 담긴 Future
        """
        # 결과 추출
        result: Fibonacci_GetResult_Response = future.result()  # type : ignore
        
        # 성공 여부에 따라 처리
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            # 성공한 경우
            self.get_logger().info(f"result: {result.result.seq} 성공!!")
        if result.status == GoalStatus.STATUS_ABORTED:
            # 중단된 경우
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Action Client 노드 생성
    node = Action_client()
    
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
