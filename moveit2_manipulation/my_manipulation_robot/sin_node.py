import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

class SinePublisher(Node):
    def __init__(self):
        super().__init__('sine_pub')
        # Publishers for gripper right/left controllers
        self.pub_right = self.create_publisher(
            JointTrajectory,
            '/gripper_right_position_controller/joint_trajectory',
            10
        )
        self.pub_left = self.create_publisher(
            JointTrajectory,
            '/gripper_left_position_controller/joint_trajectory',
            10
        )
        self.timer = self.create_timer(0.05, self.timer_callback)  # 20Hz
        self.i = 0
        # Remember previous commanded positions for a 2-point trajectory
        self.prev_right = 0.0  # within [0.0, 0.05]
        self.prev_left = 0.0   # within [-0.05, 0.0]
        # Speed tuning
        self.horizon_sec = 0.3   # time to reach next target (smaller = faster)
        self.freq_scale = 2.0    # sine frequency multiplier (bigger = faster oscillation)

    def timer_callback(self):
        # Sinusoidal targets within limits
        # right: [0.0, 0.05], left: [-0.05, 0.0] (mirror)
        amp = 0.025
        base = 0.025
        target_right = base + amp * math.sin(self.i / 100.0 * self.freq_scale)
        target_left = -target_right

        # Build right trajectory (2 points: current->target)
        msg_r = JointTrajectory()
        msg_r.joint_names = ['tcp_connector__gripper_right']
        p0_r = JointTrajectoryPoint()
        p0_r.positions = [self.prev_right]
        p0_r.time_from_start.sec = 0
        p0_r.time_from_start.nanosec = 0
        p1_r = JointTrajectoryPoint()
        p1_r.positions = [target_right]
        sec_r = int(self.horizon_sec)
        nsec_r = int((self.horizon_sec - sec_r) * 1e9)
        p1_r.time_from_start.sec = sec_r
        p1_r.time_from_start.nanosec = nsec_r
        msg_r.points = [p0_r, p1_r]

        # Build left trajectory (2 points: current->target)
        msg_l = JointTrajectory()
        msg_l.joint_names = ['tcp_connector__gripper_left']
        p0_l = JointTrajectoryPoint()
        p0_l.positions = [self.prev_left]
        p0_l.time_from_start.sec = 0
        p0_l.time_from_start.nanosec = 0
        p1_l = JointTrajectoryPoint()
        p1_l.positions = [target_left]
        sec_l = int(self.horizon_sec)
        nsec_l = int((self.horizon_sec - sec_l) * 1e9)
        p1_l.time_from_start.sec = sec_l
        p1_l.time_from_start.nanosec = nsec_l
        msg_l.points = [p0_l, p1_l]

        # Publish
        self.pub_right.publish(msg_r)
        self.pub_left.publish(msg_l)
        self.get_logger().info(f'gripper_r={target_right:.3f}, gripper_l={target_left:.3f}')

        # Update state
        self.prev_right = target_right
        self.prev_left = target_left
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = SinePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
