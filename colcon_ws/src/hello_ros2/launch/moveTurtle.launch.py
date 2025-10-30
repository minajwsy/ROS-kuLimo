"""
ROS2 Launch 파일 예제 - 고급
- 파라미터 파일(YAML)을 사용하여 노드 설정
- 여러 노드를 파라미터와 함께 실행
- Launch Argument를 사용한 유연한 설정
"""

# === 실행 방법 주석 ===
# ros2 param list                    # 파라미터 목록 확인
# ros2 param dump                     # 모든 파라미터 덤프
# ros2 param dump turtlesim           # turtlesim 노드의 파라미터만 덤프
# ros2 param dump turtlesim >> turtlesim.yaml  # 파일로 저장
# ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim.yaml  # 파라미터 파일로 실행
# ros2 launch hello_ros2 moveTurtle.launch.py  # Launch 파일로 실행

import os  # 운영체제 기능 (경로 처리)

from ament_index_python.packages import get_package_share_directory  # 패키지 경로 찾기
from launch import LaunchDescription  # Launch 기본 클래스
from launch.actions import DeclareLaunchArgument  # Launch 인자 선언
from launch.substitutions import LaunchConfiguration  # Launch 인자 사용
from launch_ros.actions import Node  # ROS2 노드 실행


def generate_launch_description():
    """
    고급 Launch Description 생성 함수
    - 파라미터 파일 경로를 Launch Argument로 설정 가능
    - 여러 노드를 파라미터와 함께 실행
    
    Returns:
        LaunchDescription: 실행할 노드들과 설정
    """
    
    # === 파라미터 파일 경로 설정 ===
    # LaunchConfiguration: Launch 시 전달되는 인자 값
    param_dir = LaunchConfiguration(
        "param_dir",  # 인자 이름
        default=os.path.join(  # 기본값 설정
            get_package_share_directory("hello_ros2"),  # hello_ros2 패키지의 설치 경로
            "param",  # param 디렉토리
            "turtlesim.yaml"  # 파라미터 파일 이름
        ),
    )
    
    # === LaunchDescription 반환 ===
    return LaunchDescription(
        [
            # === Launch Argument 선언 ===
            DeclareLaunchArgument(
                "param_dir",  # 인자 이름 (명령줄에서 param_dir:=값 형태로 전달 가능)
                default_value=param_dir,  # 기본값
                description="turtlesim paramdter dump file",  # 설명
            ),
            
            # === 노드 1: turtlesim_node ===
            Node(
                package="turtlesim",  # turtlesim 패키지 (ROS2 기본 패키지)
                executable="turtlesim_node",  # turtlesim 시뮬레이터 실행
                parameters=[param_dir]  # 파라미터 파일 로드
                # turtlesim.yaml의 /turtlesim 섹션 파라미터 적용됨
                # 예: background_r, background_g, background_b (배경색)
            ),
            
            # === 노드 2: move_turtle ===
            Node(
                package="hello_ros2",  # hello_ros2 패키지
                executable="move_turtle",  # 터틀 이동 노드
                parameters=[param_dir]  # 파라미터 파일 로드
                # turtlesim.yaml의 /move_turtle 섹션 파라미터 적용됨
                # 예: vel (선속도), angle_vel (각속도)
            ),
            
            # === 노드 3: change_color_client ===
            Node(
                package="hello_ros2",  # hello_ros2 패키지
                executable="change_color_client"  # 색상 변경 클라이언트
                # parameters 없음: 파라미터 파일 사용하지 않음
            ),
        ]
    )


"""
상세 설명:
---------

1. LaunchConfiguration과 DeclareLaunchArgument
   - LaunchConfiguration: Launch 인자의 값을 저장
   - DeclareLaunchArgument: Launch 인자를 선언하고 기본값 설정
   - 사용자가 명령줄에서 값을 변경 가능

2. get_package_share_directory()
   - 패키지가 설치된 share 디렉토리 경로를 반환
   - colcon build 후 install/share/패키지명/ 디렉토리
   - 파라미터 파일, Launch 파일 등이 이곳에 설치됨

3. os.path.join()
   - 플랫폼 독립적으로 경로를 결합
   - Windows: 역슬래시(\)
   - Linux/Mac: 슬래시(/)

4. parameters=[param_dir]
   - 노드에 파라미터 파일을 로드
   - YAML 파일의 해당 노드 섹션 파라미터가 적용됨


실행 방법:
---------

# 1. 기본 실행 (기본 파라미터 파일 사용)
ros2 launch hello_ros2 moveTurtle.launch.py

# 2. 커스텀 파라미터 파일 사용
ros2 launch hello_ros2 moveTurtle.launch.py param_dir:=/path/to/custom.yaml

# 3. Launch 파일 정보 확인
ros2 launch hello_ros2 moveTurtle.launch.py --show-args


실행 결과:
---------
1. turtlesim 창이 열림
   - 배경색이 turtlesim.yaml의 설정대로 변경됨
   - background_r: 10, background_g: 16, background_b: 200

2. 터틀이 자동으로 움직임
   - move_turtle 노드가 속도 명령을 전송
   - vel: 1.0 m/s, angle_vel: 3.0 rad/s

3. 터틀의 궤적 색상이 계속 변함
   - change_color_client 노드가 0.3초마다 색상 변경


파라미터 파일 (turtlesim.yaml) 구조:
-----------------------------------
/turtlesim:
  ros__parameters:
    background_r: 10      # 빨강 (0-255)
    background_g: 16      # 초록 (0-255)
    background_b: 200     # 파랑 (0-255)

/move_turtle:
  ros__parameters:
    vel: 1.0              # 선속도 (m/s)
    angle_vel: 3.0        # 각속도 (rad/s)


실시간 파라미터 변경:
-------------------
Launch 파일 실행 중에도 파라미터 변경 가능:

# 터틀 속도 변경
ros2 param set /move_turtle vel 2.0
ros2 param set /move_turtle angle_vel 5.0

# 배경색 변경 (실시간 반영 안 됨, 재시작 필요)
ros2 param set /turtlesim background_r 255


디버깅 팁:
---------
# Launch 파일 실행 중 노드 목록 확인
ros2 node list

# 각 노드의 파라미터 확인
ros2 param list
ros2 param get /turtlesim background_r
ros2 param get /move_turtle vel

# 토픽 통신 확인
ros2 topic list
ros2 topic echo /turtle1/cmd_vel
ros2 topic hz /turtle1/cmd_vel

# 서비스 확인
ros2 service list
ros2 service type /turtle1/set_pen


Launch 파일의 장점:
-----------------
1. 복잡한 시스템을 한 번에 실행
2. 노드 간 의존성 관리
3. 파라미터 중앙 관리
4. 재사용 가능한 설정
5. 환경에 따른 유연한 구성
"""
