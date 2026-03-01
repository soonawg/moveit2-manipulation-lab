import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

# joint base_link__link1, link1__link2, link2__link3 주기적 이동 노드

class SinePublisherSam(Node):
    def __init__(self):
        super().__init__('sine_pub_sam')
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
        self.timer = self.create_timer(0.05, self.timer_callback)  # 20Hz
        self.i = 0

    def timer_callback(self):
        # joint1: base_link__link1 -> 1*sin(i/100)
        msg1 = JointTrajectory()
        msg1.joint_names = ['base_link__link1']
        point1 = JointTrajectoryPoint()
        point1.positions = [1.0 * math.sin(self.i / 100.0)]
        point1.time_from_start.sec = 1
        point1.time_from_start.nanosec = 0
        msg1.points.append(point1)
        self.pub1.publish(msg1)

        # joint2: link1__link2 -> 1*sin(i/100)
        msg2 = JointTrajectory()
        msg2.joint_names = ['link1__link2']
        point2 = JointTrajectoryPoint()
        point2.positions = [1.0 * math.sin(self.i / 100.0)]
        point2.time_from_start.sec = 1
        point2.time_from_start.nanosec = 0
        msg2.points.append(point2)
        self.pub2.publish(msg2)

        # joint3: link2__link3 -> 1.57*sin(i/100)
        msg3 = JointTrajectory()
        msg3.joint_names = ['link2__link3']
        point3 = JointTrajectoryPoint()
        point3.positions = [1.57 * math.sin(self.i / 100.0)]
        point3.time_from_start.sec = 1
        point3.time_from_start.nanosec = 0
        msg3.points.append(point3)
        self.pub3.publish(msg3)

        self.get_logger().info(
            f'i={self.i} | j1={point1.positions[0]:.3f}, j2={point2.positions[0]:.3f}, j3={point3.positions[0]:.3f}'
        )
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = SinePublisherSam()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
