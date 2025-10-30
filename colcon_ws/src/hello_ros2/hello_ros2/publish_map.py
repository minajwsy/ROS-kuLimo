"""
ROS2 OccupancyGrid 맵 발행 예제
- 점유 격자 지도(Occupancy Grid)를 동적으로 생성하여 발행
- RViz에서 시각화 가능
- 맵 데이터를 순차적으로 변경하여 애니메이션 효과
"""

# 실행 방법:
# ros2 topic echo /map --once
# ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
# ros2 run hello_ros2 publish_map

import rclpy
from nav_msgs.msg import OccupancyGrid  # 점유 격자 지도 메시지
from rclpy.node import Node


class PublishMap(Node):
    """
    동적으로 변화하는 OccupancyGrid 맵을 발행하는 노드
    """
    
    def __init__(self):
        """Map Publisher 초기화"""
        # "publish_map"이라는 이름의 노드 생성
        super().__init__("publish_map")
        
        # Timer 생성: 0.001초마다 pub_cb 호출 (1000Hz - 매우 빠름)
        self.create_timer(0.001, self.pub_cb)
        
        # Publisher 생성
        # OccupancyGrid 메시지를 "/map" 토픽으로 발행
        self.pub = self.create_publisher(OccupancyGrid, "/map", 100)
        
        # OccupancyGrid 메시지 생성
        self.msg = OccupancyGrid()
        
        # === 맵 헤더 설정 ===
        self.msg.header.frame_id = "odom"  # 좌표계
        
        # === 맵 메타데이터 설정 ===
        self.msg.info.resolution = 0.1  # 해상도: 한 셀당 0.1m (10cm)
        self.msg.info.width = 200  # 맵 너비: 200셀
        self.msg.info.height = 100  # 맵 높이: 100셀
        
        # 맵 원점 위치 (맵의 좌하단 코너)
        self.msg.info.origin.position.x = 0.0
        self.msg.info.origin.position.y = 0.0
        self.msg.info.origin.position.z = 0.0
        
        # 맵 원점 방향 (회전 없음)
        self.msg.info.origin.orientation.x = 0.0
        self.msg.info.origin.orientation.y = 0.0
        self.msg.info.origin.orientation.z = 0.0
        self.msg.info.origin.orientation.w = 1.0

        # === 맵 데이터 초기화 ===
        # OccupancyGrid 값:
        # -1: 미지의 영역 (unknown)
        # 0: 빈 공간 (free)
        # 100: 장애물 (occupied)
        
        # 처음 10,000셀은 100 (장애물)
        self.msg.data = [100 for _ in range(10_000)]
        # 나머지 10,000셀은 0 (빈 공간)
        self.msg.data.extend([0 for _ in range(10_000)])

        # 현재 수정 중인 셀의 열(column) 인덱스
        self.count = 0
        # 현재 수정 중인 셀의 행(row) 인덱스
        self.row = 0

    def pub_cb(self):
        """
        주기적으로 호출되어 맵을 발행하는 함수
        맵의 각 셀을 순차적으로 변경하여 애니메이션 효과
        """
        # 타임스탬프 업데이트
        self.msg.header.stamp = self.get_clock().now().to_msg()

        # 현재 수정할 셀의 1차원 인덱스 계산
        # 2D 좌표 (row, count)를 1D 인덱스로 변환
        # index = x + (width * y)
        index = self.count + (self.msg.info.width * self.row)
        
        # 현재 셀의 값을 토글
        if self.msg.data[index] == -1:
            # 미지의 영역(-1)을 장애물(100)로 변경
            self.msg.data[index] = 100
        else:
            # 그 외의 값을 미지의 영역(-1)로 변경
            self.msg.data[index] = -1

        # 다음 셀로 이동 (열 증가)
        self.count += 1
        
        # 행의 끝에 도달하면 다음 행으로
        if self.count >= self.msg.info.width:
            self.count = 0  # 열 인덱스 초기화
            self.row += 1  # 다음 행으로
        
        # 맵의 끝에 도달하면 처음으로
        if self.row >= self.msg.info.height:
            self.row = 0

        # 맵 메시지 발행
        self.pub.publish(self.msg)


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Map Publisher 노드 생성
    node = PublishMap()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
