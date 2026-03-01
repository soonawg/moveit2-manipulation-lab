import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit # --- 변경점: import 추가 ---
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # ---- 0. ARGUMENTS ----
    # 로봇의 시작 위치를 위한 argument 선언
    arg_x_pos = DeclareLaunchArgument("x", default_value="0.0", description="Robot x position")
    arg_y_pos = DeclareLaunchArgument("y", default_value="0.0", description="Robot y position")
    arg_z_pos = DeclareLaunchArgument("z", default_value="0.0", description="Robot z position")

    # Cube 시작 위치를 위한 argument 선언
    arg_cube_x_pos = DeclareLaunchArgument("cube_x", default_value="1.0", description="Cube x position")
    arg_cube_y_pos = DeclareLaunchArgument("cube_y", default_value="1.0", description="Cube y position")
    arg_cube_z_pos = DeclareLaunchArgument("cube_z", default_value="0.25", description="Cube z position")
    
    # ---- 1. ROBOT DESCRIPTION ----
    # URDF 파일 경로 설정
    urdf_file_path = os.path.join(
        get_package_share_directory('my_manipulation_robot'),
        'urdf',
        'cobot.urdf.xacro'
    )

    cube_urdf_file_path = os.path.join(
        get_package_share_directory('my_manipulation_robot'),
        'urdf',
        'cube_pick_place.urdf.xacro'
    )
    
    # xacro를 실행하여 URDF 생성
    robot_description_content = Command(
        [FindExecutable(name='xacro'), ' ', urdf_file_path]
    )
    robot_description = {
        'robot_description': ParameterValue(robot_description_content, value_type=str)
    }
    
    cube_description_content = Command(
        [FindExecutable(name='xacro'), ' ', cube_urdf_file_path]
    )
    cube_description = {
        'robot_description': ParameterValue(cube_description_content, value_type=str)
    }

    # ---- 2. CONTROLLERS.YAML ----
    # 컨트롤러 설정 파일 경로 설정
    controllers_yaml_path = os.path.join(
        get_package_share_directory('my_manipulation_robot'),
        'config',
        'joints_controllers.yaml'
    )

    # ---- 3. GAZEBO LAUNCH ----
    # Gazebo 실행 (empty_world.launch -> gazebo.launch.py)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]
        ),
        launch_arguments={'paused': 'true'}.items(),
    )

    # ---- 4. ROBOT STATE PUBLISHER ----
    # robot_state_publisher 노드 실행
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description,
                   {'use_sim_time': True}],
    )

    # Cube description publisher
    cube_description_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='cube_description_publisher',
        output='screen',
        parameters=[cube_description,
                   {'use_sim_time': True}],
        remappings=[('robot_description', 'cube_description')],
    )

    # ---- 5. SPAWN ROBOT ----
    # Gazebo에 로봇 모델 스폰
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'cobot',
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z'),
        ],
        output='screen'
    )

    # Gazebo에 Cube 모델 스폰 (파일 직접 참조 방식)
    spawn_cube_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-file', cube_urdf_file_path,  # URDF 파일 직접 참조
            '-entity', 'cube',
            '-x', LaunchConfiguration('cube_x'),
            '-y', LaunchConfiguration('cube_y'),
            '-z', LaunchConfiguration('cube_z'),
        ],
        output='screen'
    )

    # ---- 6. CONTROLLER SPAWNERS ----
    # Gazebo 플러그인이 컨트롤러 매니저를 생성하므로, 
    # 루트 네임스페이스의 controller_manager를 사용합니다.
    
    # a. Joint State Broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    # b. Joint1 Position Controller
    joint1_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint1_position_controller"],
    )
    
    # c. Joint2 Position Controller
    joint2_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint2_position_controller"],
    )
    
    # d. Joint3 Position Controller
    joint3_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint3_position_controller"],
    )

    # e. Joint4 Position Controller
    joint4_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint4_position_controller"],
    )
    
    # f. Joint5 Position Controller
    joint5_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint5_position_controller"],
    )

    # g. Joint6 Position Controller
    joint6_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint6_position_controller"],
    )

    # # h. Gripper Right Position Controller
    # gripper_right_position_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["gripper_right_position_controller"],
    # )

    # # i. Gripper Left Position Controller
    # gripper_left_position_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["gripper_left_position_controller"],
    # )
    # --- 추가 ---
    # h. Gripper Trajectory Controller
    gripper_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_trajectory_controller"], # YAML에 새로 추가한 컨트롤러 이름
    )

    # ---- 7. RQT ----
    # rqt_gui 실행 (선택 사항)
    rqt_gui_node = Node(
        package='rqt_gui',
        executable='rqt_gui',
        name='rqt_gui',
        output='screen'
    )

    # ---- LaunchDescription 반환 ----
    # return LaunchDescription([
    #     arg_x_pos,
    #     arg_y_pos,
    #     arg_z_pos,
    #     arg_cube_x_pos,
    #     arg_cube_y_pos,
    #     arg_cube_z_pos,
    #     gazebo,
    #     robot_state_publisher_node,
    #     spawn_entity_node,
    #     spawn_cube_node,
    #     joint_state_broadcaster_spawner,
    #     joint1_position_controller_spawner,
    #     joint2_position_controller_spawner,
    #     joint3_position_controller_spawner,
    #     joint4_position_controller_spawner,
    #     joint5_position_controller_spawner,
    #     joint6_position_controller_spawner,
    #     # gripper_right_position_controller_spawner,
    #     # gripper_left_position_controller_spawner,
    #     gripper_trajectory_controller_spawner,
    #     rqt_gui_node,
    # ])
    return LaunchDescription([
        # 먼저 실행되어야 할 노드들
        arg_x_pos,
        arg_y_pos,
        arg_z_pos,
        arg_cube_x_pos,
        arg_cube_y_pos,
        arg_cube_z_pos,
        gazebo,
        robot_state_publisher_node,
        spawn_entity_node,
        spawn_cube_node,
        rqt_gui_node,

        # spawn_entity_node 프로세스가 성공적으로 종료된(로봇이 스폰된) 후에
        # 아래의 컨트롤러 spawner들을 실행
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity_node,
                on_exit=[
                    joint_state_broadcaster_spawner,
                    joint1_position_controller_spawner,
                    joint2_position_controller_spawner,
                    joint3_position_controller_spawner,
                    joint4_position_controller_spawner,
                    joint5_position_controller_spawner,
                    joint6_position_controller_spawner,
                    # gripper_right_position_controller_spawner,
                    # gripper_left_position_controller_spawner,
                    gripper_trajectory_controller_spawner,
                ],
            )
        ),
    ])