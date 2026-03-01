# 파일명: ur5e_test_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class UR5eTestNode(Node):
    def __init__(self):
        super().__init__('ur5e_test_node')
        
        # Joint 상태 구독
        self.joint_sub = self.create_subscription(
            JointState,
            '/ur5e/joint_states',
            self.joint_callback,
            10
        )
        
        # Trajectory 발행
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/ur5e/ur_joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # 2초 후 테스트 동작 실행
        self.timer = self.create_timer(2.0, self.send_test_trajectory)
        self.sent = False

    def joint_callback(self, msg: JointState):
        self.get_logger().info(f"Current joint positions: {['{:.2f}'.format(p) for p in msg.position]}")

    def send_test_trajectory(self):
        if self.sent:
            return
        
        traj = JointTrajectory()
        traj.joint_names = [
            'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
            'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'
        ]
        
        point = JointTrajectoryPoint()
        point.positions = [0.0, -1.57, 1.57, 0.0, 0.0, 0.0]  # 목표 관절 각도
        point.time_from_start.sec = 2
        traj.points.append(point)
        
        self.traj_pub.publish(traj)
        self.get_logger().info("Sent test trajectory to UR5e")
        self.sent = True

def main(args=None):
    rclpy.init(args=args)
    node = UR5eTestNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
