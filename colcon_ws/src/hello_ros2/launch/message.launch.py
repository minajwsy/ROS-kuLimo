"""
ROS2 Launch 파일 예제 - 기본
- 여러 노드를 동시에 실행하는 가장 간단한 형태
- simple_pub과 simple_sub 노드를 함께 실행
- Publisher와 Subscriber가 자동으로 통신
"""

from launch import LaunchDescription  # Launch 파일의 기본 클래스
from launch_ros.actions import Node  # ROS2 노드 실행 액션


def generate_launch_description():
    """
    Launch 파일의 필수 함수
    - ROS2 launch 시스템이 이 함수를 호출하여 실행할 내용을 가져옴
    - LaunchDescription 객체를 반환해야 함
    
    Returns:
        LaunchDescription: 실행할 노드 및 액션들의 목록
    """
    return LaunchDescription([
        # === Publisher 노드 실행 ===
        Node(
            package="hello_ros2",      # 패키지 이름
            executable="simple_pub"     # 실행할 노드 이름 (setup.py의 entry_points에 정의됨)
        ),
        
        # === Subscriber 노드 실행 ===
        Node(
            package="hello_ros2",       # 패키지 이름
            executable="simple_sub"     # 실행할 노드 이름
        )
    ])


"""
실행 방법:
-----------
ros2 launch hello_ros2 message.launch.py

설명:
----
1. simple_pub 노드가 /message 토픽으로 메시지를 발행
2. simple_sub 노드가 /message 토픽을 구독하여 메시지를 수신
3. 두 노드가 자동으로 통신하며 실행됨
4. Ctrl+C로 종료하면 두 노드 모두 종료됨

장점:
----
- 여러 터미널을 열 필요 없음
- 한 번의 명령으로 전체 시스템 실행
- 노드 간 실행 순서 및 의존성 관리 가능
"""