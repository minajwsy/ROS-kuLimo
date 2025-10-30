"""
ROS2 Parameter 예제
- 런타임에 동적으로 변경 가능한 파라미터 사용
- 외부에서 파라미터 값을 설정하고 변경 가능
"""

# 실행 방법:
# ros2 run hello_ros2 simple_parameter --ros-args -p para1:=True
# ros2 run hello_ros2 simple_parameter
# ros2 param set simple_parameter para1 1000
# ros2 param get simple_parameter para1

import rclpy
from rcl_interfaces.msg import SetParametersResult  # 파라미터 설정 결과
from rclpy.node import Node
from rclpy.parameter import Parameter  # 파라미터 클래스


class Simple_parameter(Node):
    """
    파라미터를 사용하는 간단한 노드
    para1 파라미터를 주기적으로 증가시키며 외부에서도 변경 가능
    """
    
    def __init__(self):
        """파라미터 노드 초기화"""
        # "simple_parameter"라는 이름의 노드 생성
        super().__init__("simple_parameter")
        
        # Timer 생성: 1초마다 update 함수 호출
        self.create_timer(1, self.update)
        
        # 파라미터 선언
        # 첫 번째 인자: 파라미터 이름 ("para1")
        # 두 번째 인자: 기본값 (0)
        self.declare_parameter("para1", 0)
        
        # 파라미터 값 가져오기
        self.para1 = self.get_parameter("para1").get_parameter_value().integer_value

        # 파라미터 변경 콜백 등록
        # 외부에서 파라미터가 변경될 때 호출됨
        self.add_on_set_parameters_callback(self.parameter_callback)

    def update(self):
        """
        주기적으로 호출되는 업데이트 함수
        파라미터 값을 1씩 증가시킴
        """
        # 현재 파라미터 값 출력
        self.get_logger().info(f"parameter : {self.para1}")
        
        # 파라미터 값 증가
        self.para1 += 1
        
        # 변경된 파라미터 값 설정
        # Parameter 객체 생성: (이름, 타입, 값)
        self.set_parameters([
            Parameter("para1", Parameter.Type.INTEGER, self.para1)
        ])

    def parameter_callback(self, parameters: list[Parameter]):
        """
        파라미터가 외부에서 변경될 때 호출되는 콜백
        
        Args:
            parameters: 변경된 파라미터 리스트
            
        Returns:
            SetParametersResult: 파라미터 변경 성공 여부
        """
        # 변경된 파라미터들을 순회
        for parameter in parameters:
            # para1 파라미터가 변경된 경우
            if parameter.name == "para1":
                # 내부 변수에 새 값 저장
                self.para1 = int(parameter.value)  # type: ignore
        
        # 변경 성공 반환
        return SetParametersResult(successful=True)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # 파라미터 노드 생성
    node = Simple_parameter()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
