import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import math

class URDemoControl(Node):
    def __init__(self):
        super().__init__('ur_demo_control')
        self.pub = self.create_publisher(JointTrajectory, '/ur5e/ur_joint_trajectory_controller/joint_trajectory', 10)

        # 초기 실행 (원하는 동작 선택)
        self.timer = self.create_timer(5.0, self.demo_motion)
        self.step = 0
    
    def send_joint_command(self, positions, duration=2.0):
        msg = JointTrajectory()
        msg.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

        point = JointTrajectoryPoint()
        point.positions = positions
        # time_from_start must be a builtin_interfaces/Duration with int fields
        secs = int(duration)
        nsecs = int((duration - secs) * 1e9)
        point.time_from_start = Duration(sec=secs, nanosec=nsecs)
        msg.points.append(point)

        self.pub.publish(msg)
        self.get_logger().info(f"Sent joint command: {positions}")
    
    def demo_motion(self):
        # 1단계씩 동작을 수행
        if self.step == 0:
            # 팔꿈치 45도
            self.send_joint_command([0.0, -1.0, math.radians(45), 0.0, 0.0, 0.0])
        elif self.step == 1:
            # 인사하기 (어깨 살짝 올리고 손목 좌우 흔들기)
            self.send_joint_command([0.0, -1.2, 1.2, 0.0, 0.5, 0.0])
        elif self.step == 2:
            self.send_joint_command([0.0, -1.2, 1.2, 0.0, -0.5, 0.0])
        elif self.step == 3:
            self.send_joint_command([0.0, -1.2, 1.2, 0.0, 0.5, 0.0])
        elif self.step == 4:
            # 엔드이펙터 직선 이동 흉내 (조인트 두 개만 변경)
            self.send_joint_command([0.0, -0.8, 1.0, 0.3, 0.0, 0.0])
        elif self.step == 5:
            self.send_joint_command([0.0, -0.8, 1.0, -0.3, 0.0, 0.0])
        else:
            self.get_logger().info("Motion sequence finished.")
            self.timer.cancel()

        self.step += 1

def main(args=None):
    rclpy.init(args=args)
    node = URDemoControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()