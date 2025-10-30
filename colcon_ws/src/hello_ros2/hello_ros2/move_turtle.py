"""
ROS2 Turtlesim 제어 예제
- Twist 메시지를 발행하여 터틀을 움직임
- 파라미터로 속도를 동적으로 조정 가능
"""

# /turtle1/cmd_vel [geometry_msgs/msg/Twist]

import rclpy
from geometry_msgs.msg import Twist  # 로봇 속도 명령 메시지
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter


class Move_turtle(Node):
    """
    Turtlesim을 제어하는 노드
    선속도와 각속도를 파라미터로 제어 가능
    """
    
    def __init__(self):
        """Turtlesim 제어 노드 초기화"""
        # "move_turtle"이라는 이름의 노드 생성
        super().__init__("move_turtle")
        
        # Timer 생성: 0.1초마다 pub_turtle 함수 호출 (10Hz)
        self.create_timer(0.1, self.pub_turtle)
        
        # Publisher 생성
        # Twist 메시지를 "/turtle1/cmd_vel" 토픽으로 발행
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        
        # 파라미터 선언
        # vel: 선속도 (전진/후진 속도)
        self.declare_parameter("vel", 0.0)
        # angle_vel: 각속도 (회전 속도)
        self.declare_parameter("angle_vel", 1.2)
        
        # 파라미터 값 가져오기
        self.vel = self.get_parameter("vel").value
        self.angle_vel = self.get_parameter("angle_vel").value

        # 파라미터 변경 콜백 등록
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, parameters: list[Parameter]):
        """
        파라미터가 외부에서 변경될 때 호출되는 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 변경 성공 여부
        """
        # 변경된 파라미터들을 순회
        for parameter in parameters:
            if parameter.name == "vel":
                # 선속도 파라미터 업데이트
                self.vel = float(parameter.value)  # type: ignore
            if parameter.name == "angle_vel":
                # 각속도 파라미터 업데이트
                self.angle_vel = float(parameter.value)  # type: ignore
        
        # 변경 성공 반환
        return SetParametersResult(successful=True)

    def pub_turtle(self):
        """
        주기적으로 호출되어 터틀에게 속도 명령을 보내는 함수
        """
        # Twist 메시지 생성
        msg = Twist()
        
        # 각속도 설정 (z축 회전 = 평면에서의 회전)
        # python은 type 캐스팅이 자유롭다.
        msg.angular.z = self.angle_vel
        
        # 선속도 설정 (x축 = 전진/후진)
        # 하지만 DDS로 넘길 때는 type check가 되어야 한다.
        msg.linear.x = self.vel
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 선속도를 점진적으로 증가 (가속)
        self.vel += 0.01  # type: ignore


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Turtlesim 제어 노드 생성
    node = Move_turtle()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
