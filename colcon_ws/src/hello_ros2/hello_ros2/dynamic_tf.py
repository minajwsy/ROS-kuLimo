"""
ROS2 Dynamic TF Broadcaster 예제
- 동적으로 변화하는 좌표계 변환(Transform) 정보를 발행
- world -> map -> joint 계층 구조 생성
- map 프레임이 world 기준으로 회전
"""

# 사전 설치 필요:
# sudo apt install ros-humble-tf-transformations

import rclpy
import rclpy.logging
from geometry_msgs.msg import TransformStamped  # 좌표 변환 메시지
from rclpy.node import Node
from tf2_ros.transform_broadcaster import TransformBroadcaster  # TF 브로드캐스터
from tf_transformations import quaternion_from_euler  # 오일러각 -> 쿼터니언 변환


class DynamicFramePublisher(Node):
    """
    동적으로 변화하는 TF를 발행하는 노드
    world -> map (회전) -> joint (고정) 구조
    """
    
    def __init__(self):
        """Dynamic TF Publisher 초기화"""
        # "dynamic_tf2_broadcaster"라는 이름의 노드 생성
        super().__init__("dynamic_tf2_broadcaster")
        
        # Timer 생성: 1/30초(약 33ms)마다 pub_cb 호출 (30Hz)
        self.create_timer(1 / 30, self.pub_cb)
        
        # TransformBroadcaster 생성 (TF 발행용)
        self.tf_br = TransformBroadcaster(self)
        
        # 회전 각도 변수 (시간에 따라 증가)
        self.t = 0.0

    def pub_cb(self):
        """
        주기적으로 호출되어 TF를 발행하는 함수
        """
        # === 첫 번째 Transform: world -> map (회전) ===
        t = TransformStamped()
        
        # 헤더 정보 설정
        t.header.stamp = self.get_clock().now().to_msg()  # 현재 시간
        t.header.frame_id = "world"  # 부모 프레임
        t.child_frame_id = "map"  # 자식 프레임
        
        # 위치 설정 (translation)
        t.transform.translation.x = 1.0  # x축으로 1m 이동
        t.transform.translation.y = 1.0  # y축으로 1m 이동
        t.transform.translation.z = 0.0  # z축 이동 없음
        
        # 회전 설정 (rotation)
        # 오일러각(roll, pitch, yaw)을 쿼터니언으로 변환
        quat = quaternion_from_euler(0, 0, self.t)  # z축(yaw) 회전
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        # === 두 번째 Transform: map -> joint (고정) ===
        t2 = TransformStamped()
        
        # 헤더 정보
        t2.header.stamp = self.get_clock().now().to_msg()
        t2.header.frame_id = "map"  # 부모 프레임
        t2.child_frame_id = "joint"  # 자식 프레임
        
        # 위치 설정
        t2.transform.translation.x = 3.0  # x축으로 3m 이동
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = 0.0
        
        # 회전 없음 (identity quaternion)
        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        t2.transform.rotation.w = 1.0

        # 회전 각도 증가 (1/60 라디안씩)
        self.t += 1 / 60
        print(self.t)

        # TF 발행
        self.tf_br.sendTransform(t)  # world -> map
        self.tf_br.sendTransform(t2)  # map -> joint


def main():
    """메인 함수"""
    # ROS2 초기화
    rclpy.init()
    
    # Dynamic TF Publisher 노드 생성
    node = DynamicFramePublisher()
    
    try:
        # 노드 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 노드 정리
        node.destroy_node()


if __name__ == "__main__":
    main()
