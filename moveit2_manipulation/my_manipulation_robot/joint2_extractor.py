import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from trajectory_msgs.msg import JointTrajectory
from sensor_msgs.msg import JointState

class Joint2Extractor(Node):
    def __init__(self):
        super().__init__('joint2_extractor')

        # Publishers
        self.pub_goal = self.create_publisher(Float64, '/joint2_goal', 10)
        self.pub_actual = self.create_publisher(Float64, '/joint2_actual', 10)

        # Subscribers
        self.sub_goal = self.create_subscription(
            JointTrajectory,
            '/joint2_position_controller/joint_trajectory',
            self.goal_callback,
            10
        )

        self.sub_actual = self.create_subscription(
            JointState,
            '/joint_states',
            self.actual_callback,
            10
        )

    def goal_callback(self, msg):
        # points 배열이 있는지 확인
        if msg.points and len(msg.points[0].positions) > 1:
            # joint2 위치 (index 1)
            joint2_goal = msg.points[0].positions[1]
            self.pub_goal.publish(Float64(data=joint2_goal))

    def actual_callback(self, msg):
        # position 배열이 있는지 확인
        if msg.position and len(msg.position) > 1:
            # joint2 실제 위치 (index 1)
            joint2_actual = msg.position[1]
            self.pub_actual.publish(Float64(data=joint2_actual))


def main(args=None):
    rclpy.init(args=args)
    node = Joint2Extractor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
