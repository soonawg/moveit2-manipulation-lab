# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
# from builtin_interfaces.msg import Duration
# import time

# class WorkingRobotController(Node):
#     def __init__(self):
#         super().__init__('working_robot_controller')
        
#         # 퍼블리셔들 생성
#         self.joint_publishers = {}
#         joints = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 
#                  'gripper_right', 'gripper_left']
        
#         for joint in joints:
#             topic = f'/{joint}_position_controller/joint_trajectory'
#             self.joint_publishers[joint] = self.create_publisher(JointTrajectory, topic, 10)
        
#         # 조인트 이름 매핑
#         self.joint_mapping = {
#             'joint1': 'base_link__link1',
#             'joint2': 'link1__link2', 
#             'joint3': 'link2__link3',
#             'joint4': 'link3__link4',
#             'joint5': 'link4__link5',
#             'joint6': 'link5__tcp_connector',
#             'gripper_right': 'tcp_connector__gripper_right',
#             'gripper_left': 'tcp_connector__gripper_left',
#         }

#     def move_joint(self, joint, position, duration=2.0):
#         """조인트를 특정 위치로 이동 (직접 명령어와 동일한 형식)"""
#         msg = JointTrajectory()
        
#         # 헤더는 비워둠 (직접 명령어와 동일)
#         msg.header.frame_id = ""
#         # timestamp는 설정하지 않음
        
#         msg.joint_names = [self.joint_mapping[joint]]
        
#         point = JointTrajectoryPoint()
#         point.positions = [float(position)]
#         # velocities, accelerations, effort는 설정하지 않음 (직접 명령어와 동일)
#         point.time_from_start = Duration(sec=int(duration), nanosec=0)
        
#         msg.points = [point]
        
#         self.joint_publishers[joint].publish(msg)
#         print(f"Moving {joint} ({self.joint_mapping[joint]}) to {position} radians")

#     def move_joint_alternative(self, joint, position, duration=2.0):
#         """대안 방법: 타임스탬프 포함"""
#         msg = JointTrajectory()
        
#         # 현재 시간으로 타임스탬프 설정
#         msg.header.stamp = self.get_clock().now().to_msg()
#         msg.header.frame_id = ""
        
#         msg.joint_names = [self.joint_mapping[joint]]
        
#         point = JointTrajectoryPoint()
#         point.positions = [float(position)]
#         point.velocities = []
#         point.accelerations = []
#         point.effort = []
#         point.time_from_start = Duration(sec=int(duration), nanosec=0)
        
#         msg.points = [point]
        
#         self.joint_publishers[joint].publish(msg)
#         print(f"Moving {joint} ({self.joint_mapping[joint]}) to {position} radians (with timestamp)")

# def main():
#     rclpy.init()
#     controller = WorkingRobotController()
    
#     print("\n=== Working Robot Controller ===")
#     print("Commands:")
#     print("  move <joint> <position>     - Move joint (no timestamp)")
#     print("  move2 <joint> <position>    - Move joint (with timestamp)")
#     print("  home                        - Move all joints to 0")
#     print("  open                        - Open gripper")
#     print("  close                       - Close gripper")
#     print("  demo                        - Run demo sequence")
#     print("  quit                        - Exit")
#     print("\nJoints: joint1, joint2, joint3, joint4, joint5, joint6, gripper_right, gripper_left")
#     print("Example: move joint1 0.5")
    
#     while True:
#         try:
#             command = input("\n> ").strip().split()
            
#             if not command:
#                 continue
                
#             if command[0] == 'quit':
#                 break
#             elif command[0] == 'move' and len(command) == 3:
#                 joint = command[1]
#                 position = float(command[2])
#                 if joint in controller.joint_publishers:
#                     controller.move_joint(joint, position)
#                 else:
#                     print(f"Unknown joint: {joint}")
#             elif command[0] == 'move2' and len(command) == 3:
#                 joint = command[1]
#                 position = float(command[2])
#                 if joint in controller.joint_publishers:
#                     controller.move_joint_alternative(joint, position)
#                 else:
#                     print(f"Unknown joint: {joint}")
#             elif command[0] == 'home':
#                 print("Moving to home position...")
#                 for joint in ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']:
#                     controller.move_joint(joint, 0.0)
#             elif command[0] == 'open':
#                 print("Opening gripper...")
#                 controller.move_joint('gripper_right', 0.02)
#                 controller.move_joint('gripper_left', -0.02)
#             elif command[0] == 'close':
#                 print("Closing gripper...")
#                 controller.move_joint('gripper_right', 0.0)
#                 controller.move_joint('gripper_left', 0.0)
#             elif command[0] == 'demo':
#                 print("Running demo sequence...")
#                 # 홈 포지션
#                 for joint in ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']:
#                     controller.move_joint(joint, 0.0)
#                 time.sleep(3)
                
#                 # 그리퍼 열기
#                 controller.move_joint('gripper_right', 0.02)
#                 controller.move_joint('gripper_left', -0.02)
#                 time.sleep(2)
                
#                 # 큐브 방향으로 이동 (더 안전한 각도들)
#                 print("Moving to approach position...")
#                 controller.move_joint('joint1', 0.5)  # 약 28도
#                 time.sleep(3)
#                 controller.move_joint('joint2', -0.3)
#                 time.sleep(3)
#                 controller.move_joint('joint3', 0.5)
#                 time.sleep(3)
                
#                 # 그리퍼 닫기
#                 print("Closing gripper...")
#                 controller.move_joint('gripper_right', 0.0)
#                 controller.move_joint('gripper_left', 0.0)
#                 time.sleep(2)
                
#                 # 들어올리기
#                 print("Lifting...")
#                 controller.move_joint('joint2', 0.2)
#                 time.sleep(3)
                
#                 # 다른 위치로 이동
#                 print("Moving to drop position...")
#                 controller.move_joint('joint1', -0.5)
#                 time.sleep(3)
                
#                 # 내려놓기
#                 print("Lowering...")
#                 controller.move_joint('joint2', -0.2)
#                 time.sleep(3)
                
#                 # 그리퍼 열기
#                 print("Opening gripper...")
#                 controller.move_joint('gripper_right', 0.02)
#                 controller.move_joint('gripper_left', -0.02)
#                 time.sleep(2)
                
#                 # 홈으로 복귀
#                 print("Returning home...")
#                 controller.home_position()
                
#                 print("Demo completed!")
#             else:
#                 print("Unknown command. Type 'quit' to exit.")
                
#         except KeyboardInterrupt:
#             break
#         except ValueError:
#             print("Invalid position value. Use numbers (radians).")
#         except Exception as e:
#             print(f"Error: {e}")
    
#     controller.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time
import math # math.fabs()를 사용하기 위해 추가

class WorkingRobotController(Node):
    def __init__(self):
        super().__init__('working_robot_controller')
        
        # --- 변경된 부분 시작 ---
        self.joint_publishers = {}
        # 'gripper_right', 'gripper_left'를 'gripper' 하나로 통합
        joints = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'gripper']
        
        for joint in joints:
            # 그리퍼의 경우 컨트롤러 이름과 토픽이 다르므로 분기 처리
            if joint == 'gripper':
                topic = '/gripper_trajectory_controller/joint_trajectory'
            else:
                topic = f'/{joint}_position_controller/joint_trajectory'
            
            self.joint_publishers[joint] = self.create_publisher(JointTrajectory, topic, 10)
        
        # 조인트 이름 매핑 (gripper_left 삭제, gripper_right는 남겨둬도 무방)
        self.joint_mapping = {
            'joint1': 'base_link__link1',
            'joint2': 'link1__link2', 
            'joint3': 'link2__link3',
            'joint4': 'link3__link4',
            'joint5': 'link4__link5',
            'joint6': 'link5__tcp_connector',
            'gripper_right': 'tcp_connector__gripper_right',
        }
        # --- 변경된 부분 끝 ---

    def move_joint(self, joint, position, duration=2.0):
        """단일 조인트를 특정 위치로 이동 (암 조인트용)"""
        # 그리퍼는 이 함수로 제어하지 않도록 방지
        if joint == 'gripper':
             self.get_logger().error("Error: Use move_gripper() to control the gripper.")
             return

        msg = JointTrajectory()
        msg.joint_names = [self.joint_mapping[joint]]
        
        point = JointTrajectoryPoint()
        point.positions = [float(position)]
        point.time_from_start = Duration(sec=int(duration), nanosec=0)
        
        msg.points = [point]
        
        self.joint_publishers[joint].publish(msg)
        self.get_logger().info(f"Moving {joint} ({self.joint_mapping[joint]}) to {position} radians")

    # --- 새로운 함수 추가 시작 ---
    def move_gripper(self, position, duration=2.0):
        """그리퍼를 특정 위치(절대값)로 이동. 양쪽을 동시에 제어."""
        msg = JointTrajectory()
        
        # 이 컨트롤러는 두 개의 조인트를 동시에 제어
        msg.joint_names = ['tcp_connector__gripper_right', 'tcp_connector__gripper_left']
        
        point = JointTrajectoryPoint()
        
        # 입력받은 position의 절대값을 사용하여 right는 양수, left는 음수로 설정
        abs_position = math.fabs(float(position))
        point.positions = [abs_position, -abs_position] 
        
        point.time_from_start = Duration(sec=int(duration), nanosec=0)
        msg.points = [point]
        
        # 'gripper'용으로 만든 단일 퍼블리셔를 사용
        self.joint_publishers['gripper'].publish(msg)
        self.get_logger().info(f"Moving gripper to position {position} (right: {abs_position}, left: {-abs_position})")
    # --- 새로운 함수 추가 끝 ---


def main():
    rclpy.init()
    controller = WorkingRobotController()
    
    # --- UI 안내 문구 수정 ---
    print("\n=== Working Robot Controller ===")
    print("Commands:")
    print("  move <joint> <position>   - Move arm joint or gripper")
    print("  home                      - Move all arm joints to 0")
    print("  open                      - Open gripper")
    print("  close                     - Close gripper")
    print("  demo                      - Run demo sequence")
    print("  quit                      - Exit")
    print("\nJoints: joint1, joint2, joint3, joint4, joint5, joint6, gripper")
    print("Example: move gripper 0.02")
    
    while True:
        try:
            command = input("\n> ").strip().split()
            
            if not command:
                continue
            
            if command[0] == 'quit':
                break
            elif command[0] == 'move' and len(command) == 3:
                joint = command[1]
                position = float(command[2])
                if joint in controller.joint_publishers:
                    # --- 변경된 부분: 'gripper' 명령 처리 ---
                    if joint == 'gripper':
                        controller.move_gripper(position)
                    else:
                        controller.move_joint(joint, position)
                else:
                    print(f"Unknown joint: {joint}")
            
            elif command[0] == 'home':
                print("Moving to home position...")
                for joint in ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']:
                    controller.move_joint(joint, 0.0)

            # --- 변경된 부분: open/close 명령을 move_gripper 호출로 변경 ---
            elif command[0] == 'open':
                print("Opening gripper...")
                controller.move_gripper(0.02) # 열 때 목표 위치 (예: 0.02)
            elif command[0] == 'close':
                print("Closing gripper...")
                controller.move_gripper(0.0)  # 닫을 때 목표 위치 (0.0)
            
            elif command[0] == 'demo':
                print("Running demo sequence...")
                # 홈 포지션
                for joint in ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']:
                    controller.move_joint(joint, 0.0)
                time.sleep(3)
                
                # --- 변경된 부분: 데모 시퀀스의 그리퍼 제어를 move_gripper로 변경 ---
                # 그리퍼 열기
                print("Opening gripper...")
                controller.move_gripper(0.02)
                time.sleep(2)
                
                # 큐브 방향으로 이동
                print("Moving to approach position...")
                controller.move_joint('joint1', 0.5)
                time.sleep(3)
                controller.move_joint('joint2', -0.3)
                time.sleep(3)
                controller.move_joint('joint3', 0.5)
                time.sleep(3)
                
                # 그리퍼 닫기
                print("Closing gripper...")
                controller.move_gripper(0.0)
                time.sleep(2)
                
                # 들어올리기
                print("Lifting...")
                controller.move_joint('joint2', 0.2)
                time.sleep(3)
                
                # 다른 위치로 이동
                print("Moving to drop position...")
                controller.move_joint('joint1', -0.5)
                time.sleep(3)
                
                # 내려놓기
                print("Lowering...")
                controller.move_joint('joint2', -0.2)
                time.sleep(3)
                
                # 그리퍼 열기
                print("Opening gripper...")
                controller.move_gripper(0.02)
                time.sleep(2)
                
                # 홈으로 복귀
                print("Returning home...")
                for joint in ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']:
                    controller.move_joint(joint, 0.0)
                time.sleep(3)
                
                print("Demo completed!")
            else:
                print("Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Invalid position value. Use numbers (radians).")
        except Exception as e:
            print(f"Error: {e}")
    
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()