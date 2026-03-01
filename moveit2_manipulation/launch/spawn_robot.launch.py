import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_name = 'my_manipulation_robot'

    # 로봇 위치 인자
    x_pos = LaunchConfiguration('x')
    y_pos = LaunchConfiguration('y')
    z_pos = LaunchConfiguration('z')

    declare_x = DeclareLaunchArgument('x', default_value='0.0', description='x position')
    declare_y = DeclareLaunchArgument('y', default_value='0.0', description='y position')
    declare_z = DeclareLaunchArgument('z', default_value='0.0', description='z position')

    # xacro -> URDF 자동 변환
    robot_description = Command([
        'xacro ',
        os.path.join(FindPackageShare(pkg_name).find(pkg_name), 'urdf', 'cobot.urdf')
    ])

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    # Joint State Publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'rate': 30}],
        output='screen'
    )

    # Gazebo 실행 
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'verbose': 'false',
            'pause': 'true',
        }.items()
    )

    # 로봇 spawn
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'cobot',
            '-topic', 'robot_description',
            '-x', x_pos,
            '-y', y_pos,
            '-z', z_pos
        ],
        output='screen'
    )

    return LaunchDescription([
        declare_x,
        declare_y,
        declare_z,
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_robot
    ])
