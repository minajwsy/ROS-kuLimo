"""
ROS2 Limo 로봇 제어 예제
- Gazebo 시뮬레이션에서 Limo 로봇을 제어
- move_turtle.py와 유사하지만 /cmd_vel 토픽 사용
"""

# /cmd_vel [geometry_msgs/msg/Twist]
# ros2 launch limo_description gazebo_models_diff.launch.py
# ros2 run hello_ros2 move_limo

import rclpy
from geometry_msgs.msg import Twist  # 로봇 속도 명령 메시지
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter


class Move_turtle(Node):
    """
    Limo 로봇을 제어하는 노드
    실제 로봇이나 Gazebo 시뮬레이션에서 사용
    """
    
    def __init__(self):
        """Limo 제어 노드 초기화"""
        # "move_limo"라는 이름의 노드 생성
        super().__init__("move_limo")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # "/cmd_vel" 토픽으로 Twist 메시지 발행
        # (turtlesim은 /turtle1/cmd_vel, 실제 로봇은 /cmd_vel)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        
        # 파라미터 선언 (기본값 지정)
        self.declare_parameter("vel", 1.0)  # 기본 선속도: 1.0 m/s
        self.declare_parameter("angle_vel", 1.2)  # 기본 각속도: 1.2 rad/s
        
        # 파라미터 값 가져오기
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        # 파라미터 변경 콜백 등록
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        """
        파라미터 변경 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 변경 성공 여부
        """
        for parameter in parameters:
            if parameter.name == "vel":
                # 선속도 업데이트
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                # 각속도 업데이트
                self.angle_vel = float(parameter.value)  # type: ignore
        
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        """
        로봇에게 속도 명령을 보내는 함수
        """
        # Twist 메시지 생성
        msg = Twist()
        
        # 각속도 설정 (회전 속도)
        # python은 type 캐스팅이 자유롭다.
        msg.angular.z = self.angle_vel
        
        # 선속도 설정 (전진/후진 속도)
        # 하지만 DDS로 넘길 때는 type check가 되어야 한다.
        msg.linear.x = self.vel
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 주석 처리됨: 속도를 점진적으로 증가시키지 않음
        # self.vel += 0.01  # type: ignore


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Limo 제어 노드 생성
    node = Move_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
