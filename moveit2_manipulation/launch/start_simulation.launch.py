import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command

def generate_launch_description():
    # 패키지 경로 가져오기
    pkg_name = 'my_manipulation_robot'
    pkg_dir = get_package_share_directory(pkg_name)

    # URDF 파일 경로
    urdf_file = os.path.join(pkg_dir, 'urdf', 'cobot.urdf')

    # Robot state publisher의 파라미터
    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]), 
        value_type=str
    )

    # Robot State Publisher 노드
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Joint State Publisher GUI 노드
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    # RViz2 노드
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])