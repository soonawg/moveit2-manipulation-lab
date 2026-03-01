import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

# joint base_link__link1, link1__link2, link2__link3, link3__link4, link4__link5, gripper_right_position_controller/joint_trajectory, gripper_left_position_controller/joint_trajectory 주기적 이동 노드

class SinePublisherFive(Node):
    def __init__(self):
        super().__init__('sine_pub_five')
        # Publishers for three joint trajectory controllers
        self.pub1 = self.create_publisher(
            JointTrajectory,
            '/joint1_position_controller/joint_trajectory',
            10
        )
        self.pub2 = self.create_publisher(
            JointTrajectory,
            '/joint2_position_controller/joint_trajectory',
            10
        )
        self.pub3 = self.create_publisher(
            JointTrajectory,
            '/joint3_position_controller/joint_trajectory',
            10
        )
        self.pub4 = self.create_publisher(
            JointTrajectory,
            '/joint4_position_controller/joint_trajectory',
            10
        )
        self.pub5 = self.create_publisher(
            JointTrajectory,
            '/joint5_position_controller/joint_trajectory',
            10
        )
        # Gripper publishers
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
        # Gripper state and timing params
        self.prev_right = 0.0  # [0.0, 0.055]
        self.prev_left = 0.0   # [-0.055, 0.0]
        self.horizon_sec = 0.3
        self.freq_scale = 2.0
        self.timer = self.create_timer(0.05, self.timer_callback)  # 20Hz
        self.i = 0

    def timer_callback(self):
        # base_joint: base_link__link1 -> 1.57*sin(i/100)
        msg1 = JointTrajectory()
        msg1.joint_names = ['base_link__link1']
        point1 = JointTrajectoryPoint()
        point1.positions = [1.57 * math.sin(self.i / 100.0)]
        point1.time_from_start.sec = 1
        point1.time_from_start.nanosec = 0
        msg1.points.append(point1)
        self.pub1.publish(msg1)

        # joint1: link1__link2 -> 1*sin(i/100)
        msg2 = JointTrajectory()
        msg2.joint_names = ['link1__link2']
        point2 = JointTrajectoryPoint()
        point2.positions = [1.0 * math.sin(self.i / 100.0*2)]
        point2.time_from_start.sec = 1
        point2.time_from_start.nanosec = 0
        msg2.points.append(point2)
        self.pub2.publish(msg2)

        # joint2: link2__link3 -> 1*sin(i/100)
        msg3 = JointTrajectory()
        msg3.joint_names = ['link2__link3']
        point3 = JointTrajectoryPoint()
        point3.positions = [1.0 * math.sin(self.i / 100.0*3)]
        point3.time_from_start.sec = 1
        point3.time_from_start.nanosec = 0
        msg3.points.append(point3)
        self.pub3.publish(msg3)

        # joint3: link3__link4 -> 1.57*sin(i/100)
        msg4 = JointTrajectory()
        msg4.joint_names = ['link3__link4']
        point4 = JointTrajectoryPoint()
        point4.positions = [1.57 * math.sin(self.i / 100.0*4)]
        point4.time_from_start.sec = 1
        point4.time_from_start.nanosec = 0
        msg4.points.append(point4)
        self.pub4.publish(msg4)

        # joint4: link4__link5 -> 1*sin(i/100)
        msg5 = JointTrajectory()
        msg5.joint_names = ['link4__link5']
        point5 = JointTrajectoryPoint()
        point5.positions = [1.0 * math.sin(self.i / 100.0*4)]
        point5.time_from_start.sec = 1
        point5.time_from_start.nanosec = 0
        msg5.points.append(point5)
        self.pub5.publish(msg5)

        # Gripper sinusoidal targets (mirror)
        amp = 0.025
        base = 0.025
        target_right = base + amp * math.sin(self.i / 100.0 * self.freq_scale)
        target_left = -target_right

        # Build right trajectory (current -> target)
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

        # Build left trajectory (current -> target)
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

        # Publish gripper commands
        self.pub_right.publish(msg_r)
        self.pub_left.publish(msg_l)

        self.get_logger().info(
            f'i={self.i} | j1={point1.positions[0]:.3f}, j2={point2.positions[0]:.3f}, j3={point3.positions[0]:.3f}, gr_r={target_right:.3f}, gr_l={target_left:.3f}'
        )
        # Update gripper state and tick
        self.prev_right = target_right
        self.prev_left = target_left
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = SinePublisherFive()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
