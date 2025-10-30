"""
ROS2 LaserScan과 OccupancyGrid 통합 예제
- publish_map.py를 확장한 버전
- LaserScan 데이터를 구독하여 맵 생성에 활용 가능
- SLAM 알고리즘의 기초 개념
"""

# 실행 방법:
# ros2 topic echo /map --once
# ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
# ros2 run hello_ros2 scan_map

import rclpy
from nav_msgs.msg import OccupancyGrid
from rclpy.node import Node
from sensor_msgs.msg import LaserScan  # LiDAR 스캔 데이터


class PublishMap(Node):
    """
    LaserScan 데이터를 사용하여 OccupancyGrid 맵을 생성하는 노드
    (SLAM의 간단한 예시)
    """
    
    def __init__(self):
        """Scan Map 노드 초기화"""
        # "publish_map"이라는 이름의 노드 생성
        super().__init__("publish_map")
        
        # === Timer 설정 ===
        # Timer 1: 0.001초마다 pub_cb 호출 (맵 발행)
        self.create_timer(0.001, self.pub_cb)
        
        # Timer 2: 1/60초마다 update 호출 (맵 업데이트 알고리즘)
        self.create_timer(1 / 60, self.update)
        
        # === Publisher 설정 ===
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        
        # === OccupancyGrid 메시지 초기화 ===
        self.msg = OccupancyGrid()
        self.msg.header.frame_id = "odom"
        
        # 맵 메타데이터
        self.msg.info.resolution = 0.1  # 10cm per cell
        self.msg.info.width = 200
        self.msg.info.height = 100
        
        # 맵 원점
        self.msg.info.origin.position.x = 0.0
        self.msg.info.origin.position.y = 0.0
        self.msg.info.origin.position.z = 0.0
        self.msg.info.origin.orientation.x = 0.0
        self.msg.info.origin.orientation.y = 0.0
        self.msg.info.origin.orientation.z = 0.0
        self.msg.info.origin.orientation.w = 1.0

        # === LaserScan Subscriber 설정 ===
        # "scan" 토픽을 구독하여 LiDAR 데이터 수신
        self.create_subscription(LaserScan, "scan", self.laser_cb, 10)

        # 맵 데이터 초기화
        self.msg.data = [100 for _ in range(10_000)]
        self.msg.data.extend([0 for _ in range(10_000)])

        # 인덱스 변수
        self.count = 0
        self.row = 0
        
        # LaserScan 데이터 저장 변수
        self.laser_s = LaserScan()

    def update(self):
        """
        주기적으로 호출되어 LaserScan 데이터를 처리하는 함수
        여기에 SLAM 알고리즘을 구현할 수 있음
        """
        # === 알고리즘 구현 영역 ===
        # self.laser_s에 저장된 LaserScan 데이터를 사용하여
        # self.msg.data를 업데이트하는 코드를 작성
        
        # 예시:
        # 1. self.laser_s.ranges에서 거리 데이터 추출
        # 2. 각 거리 데이터를 좌표로 변환
        # 3. 해당 좌표의 맵 셀을 장애물(100)로 표시
        # 4. 로봇과 장애물 사이는 빈 공간(0)으로 표시
        
        pass  # 실제 구현은 학생이 작성

    def laser_cb(self, msg):
        """
        LaserScan 데이터를 수신하는 콜백
        
        Args:
            msg: LaserScan 메시지
                - ranges: 거리 측정값 배열
                - angle_min: 최소 각도
                - angle_max: 최대 각도
                - angle_increment: 각도 증분
                - range_min: 최소 측정 거리
                - range_max: 최대 측정 거리
        """
        # 수신한 LaserScan 데이터를 저장
        self.laser_s = msg

    def pub_cb(self):
        """
        맵을 발행하는 함수
        (publish_map.py와 동일)
        """
        # 타임스탬프 업데이트
        self.msg.header.stamp = self.get_clock().now().to_msg()

        # 현재 셀 인덱스 계산
        index = self.count + (self.msg.info.width * self.row)
        
        # 셀 값 토글
        if self.msg.data[index] == -1:
            self.msg.data[index] = 100
        else:
            self.msg.data[index] = -1

        # 다음 셀로 이동
        self.count += 1
        if self.count >= self.msg.info.width:
            self.count = 0
            self.row += 1
        if self.row >= self.msg.info.height:
            self.row = 0

        # 맵 발행
        self.pub.publish(self.msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Scan Map 노드 생성
    node = PublishMap()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
