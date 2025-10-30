"""
ROS2 Navigation2 순찰 예제
- Nav2의 FollowWaypoints 액션을 사용
- 미리 정의된 경로점(waypoints)을 순환하며 순찰
- TurtleBot3 시뮬레이션과 함께 사용
"""

# 실행 방법:
# ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
# ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=/home/aa/kuLimo/map.yaml
# initial pose 잡아서 amcl 활성화
# ros2 run hello_ros2 patrol

import math
import time

import rclpy
from action_msgs.msg import GoalStatus  # Action goal 상태
from geometry_msgs.msg import PoseStamped  # 목표 위치
from nav2_msgs.action import FollowWaypoints  # Nav2 순찰 액션
from nav2_msgs.action._follow_waypoints import FollowWaypoints_GetResult_Response
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from rclpy.node import Node
from rclpy.task import Future


class Action_client(Node):
    """
    Nav2를 사용하여 지정된 경로점을 순환하며 순찰하는 노드
    """
    
    def __init__(self):
        """Patrol 노드 초기화"""
        # "fibonacci_client"라는 이름의 노드 생성 (이름 변경 권장)
        super().__init__("fibonacci_client")
        
        # Action Client 생성
        # FollowWaypoints 액션: Nav2의 경로점 추적 기능
        self.action_client = ActionClient(self, FollowWaypoints, "follow_waypoints")
        
        # Future 객체들
        self.future = Future()
        self.get_result_future = Future()
        
        # === 순찰 경로 정의 ===
        # patrol_points: (x, y) 좌표 리스트 (map 좌표계 기준)
        self.patrol_points = [(4.0, 0.0), (4.0, 1.0), (2.0, 2.5), (0.0, 1.0)]
        
        # patrol_degree: 각 지점에서의 방향 (도 단위)
        self.patrol_degree = [0, 90, 180, 90]
        
        # 현재 순찰 인덱스
        self.patrol_index = 0
        
        # Goal 객체 생성
        self.goal = FollowWaypoints.Goal()
        
        # 첫 번째 경로점으로 이동 시작
        self.go_next()

    def go_next(self):
        """
        다음 순찰 지점으로 이동
        순환 방식: 마지막 지점 이후 다시 첫 번째로
        """
        # 현재 인덱스의 경로점으로 이동 요청
        self.send_goal(
            self.patrol_points[self.patrol_index][0],  # x 좌표
            self.patrol_points[self.patrol_index][1],  # y 좌표
            self.patrol_degree[self.patrol_index],      # 방향
        )
        
        # 인덱스 증가
        self.patrol_index += 1
        
        # 마지막 지점을 지나면 처음으로 되돌림 (순환)
        if self.patrol_index >= len(self.patrol_points):
            self.patrol_index = 0

    def send_goal(self, x: float, y: float, theta: int):
        """
        지정된 위치로 이동하는 goal을 전송
        
        Args:
            x: 목표 x 좌표 (미터)
            y: 목표 y 좌표 (미터)
            theta: 목표 방향 (도)
        """
        # PoseStamped 메시지 생성 (위치와 방향)
        pose = PoseStamped()
        
        # 헤더 설정
        pose.header.frame_id = "map"  # map 좌표계 기준
        pose.header.stamp = self.get_clock().now().to_msg()
        
        # 위치 설정
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0  # 2D 네비게이션이므로 z는 0
        
        # 방향 설정 (쿼터니언)
        # 도(degree)를 라디안(radian)으로 변환
        rad = math.radians(theta)
        
        # Yaw 각도를 쿼터니언으로 변환
        # q = [x, y, z, w] = [0, 0, sin(θ/2), cos(θ/2)]
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = math.sin(rad / 2.0)
        pose.pose.orientation.w = math.cos(rad / 2.0)
        
        # Goal의 poses 리스트 초기화 및 추가
        self.goal.poses.clear()  # type : ignore
        self.goal.poses.append(pose)  # type : ignore
        
        # Nav2 서버 접속 대기
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("nav2 서버 접속중 ...")
        
        # 비동기로 goal 전송
        self.future: Future = self.action_client.send_goal_async(
            self.goal, 
            feedback_callback=self.feedback_callback
        )
        
        # goal 응답 콜백 등록
        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future):
        """
        goal이 서버에 접수되었는지 확인하는 콜백
        
        Args:
            future: goal 전송 결과
        """
        # goal 핸들 추출
        goal_handle: ClientGoalHandle = future.result()  # type : ignore
        
        # goal이 거부된 경우
        if not goal_handle.accepted:
            self.get_logger().info("골이 접수 안 되었습니다.")
            return
        
        # goal이 접수된 경우, 결과 요청
        self.get_result_future: Future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.done_callback)

    def feedback_callback(self, msg):
        """
        네비게이션 진행 중 피드백 수신 콜백
        
        Args:
            msg: 피드백 메시지
        """
        feedback: FollowWaypoints.Feedback = msg.feedback
        
        # 현재 경로점 번호 출력
        self.get_logger().info(f" 지금까지 처리 결과 seq{feedback.current_waypoint}")
        self.get_logger().info(f" patrol index{self.patrol_index}")

    def done_callback(self, future: Future):
        """
        네비게이션 완료 시 호출되는 콜백
        
        Args:
            future: 결과가 담긴 Future
        """
        # 결과 추출
        result: FollowWaypoints_GetResult_Response = future.result()  # type : ignore
        
        # 성공 여부에 따라 처리
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            # 성공: 다음 경로점으로 이동
            self.get_logger().info(f"result: {result.result.missed_waypoints} 성공!!")
            self.go_next()  # 다음 순찰 지점으로
        if result.status == GoalStatus.STATUS_ABORTED:
            # 실패: 로그 출력
            self.get_logger().info(f"result: aborted 실패!!")


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Patrol 노드 생성
    node = Action_client()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
