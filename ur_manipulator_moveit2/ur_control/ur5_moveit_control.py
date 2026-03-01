#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from moveit_msgs.srv import GetPositionIK


class UR5IKNode(Node):
    def __init__(self):
        super().__init__("ur5_ik_rclpy_node")

        # IK service client (move_group에서 제공)
        self.cli = self.create_client(GetPositionIK, "compute_ik")
        while not self.cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().info("IK service not available, waiting...")

        # Joint trajectory publisher
        self.trajectory_pub = self.create_publisher(
            JointTrajectory,
            "/ur5e/ur_joint_trajectory_controller/joint_trajectory",
            10
        )

        # 목표 pose 실행
        self.send_goal_pose()

    def send_goal_pose(self):
        # 목표 pose (엔드이펙터 좌표) 설정
        target_pose = PoseStamped()
        target_pose.header.frame_id = "base_link"
        target_pose.pose.position.x = 0.4
        target_pose.pose.position.y = 0.0
        target_pose.pose.position.z = 0.3
        target_pose.pose.orientation.w = 1.0

        # IK 요청 생성
        req = GetPositionIK.Request()
        req.ik_request.group_name = "manipulator"  # UR MoveIt 그룹 이름
        req.ik_request.pose_stamped = target_pose
        req.ik_request.timeout.sec = 2

        # 서비스 호출
        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() and future.result().error_code.val == 1:
            solution = future.result().solution.joint_state
            self.get_logger().info(f"IK solution: {solution.position}")

            # JointTrajectory 메시지 작성
            traj = JointTrajectory()
            traj.joint_names = solution.name

            point = JointTrajectoryPoint()
            point.positions = solution.position
            point.time_from_start.sec = 2
            traj.points.append(point)

            # 퍼블리시
            self.trajectory_pub.publish(traj)
            self.get_logger().info("Trajectory published ✅")

        else:
            self.get_logger().error("IK Failed!")


def main(args=None):
    rclpy.init(args=args)
    node = UR5IKNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
