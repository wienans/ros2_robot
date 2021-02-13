import os
import sys

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command,LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Use Simulation time from gazebo
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
   # Load the URDF into a parameter
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    description_dir = get_package_share_directory('robot_description')
    gazebo_dir = get_package_share_directory('robot_gazebo')
    world_path = os.path.join(gazebo_dir, 'worlds/empty_world/', 'empty_world.world')
    # world_path = os.path.join(gazebo_dir, 'worlds/office/', 'service.world')
    xacro_path = os.path.join(description_dir, 'urdf', 'robot.xacro')
    urdf_path = os.path.join(description_dir, 'urdf', 'robot.urdf')
    #Launch configurationParam
    world = LaunchConfiguration('world')

    os.system("xacro -o {out_file_path} {in_file_path}".format(out_file_path=urdf_path,in_file_path=xacro_path))
    urdf_code = open(urdf_path).read()

    #Load Controllers
    controller_robot_description = {'robot_description': urdf_code}
    diff_drive_controller = os.path.join(
        get_package_share_directory('robot_control'),
        'controllers',
        'robot_control.yaml'
        )
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        # TODO(orduno) Switch back once ROS argument passing has been fixed upstream
        #              https://github.com/ROBOTIS-GIT/turtlebot3_simulations/issues/91
        # default_value=os.path.join(get_package_share_directory('turtlebot3_gazebo'),
        #                            'worlds/turtlebot3_worlds/waffle.model'),
        default_value=world_path,
        description='Full path to world model file to load')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gazebo.launch.py'),
        )
    )
    spawn_robot_cmd = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=['-entity', 'robot', '-file', urdf_path, '-x','0','-y','20'],
        output='screen'
        )

    start_robot_state_publisher_cmd = Node(
            name='robot_state_publisher',
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description':Command(['xacro',' ', xacro_path])
                }],
        )
    # start_controller_manager_cmd = Node(
    #     package='controller_manager',
    #     executable='ros2_control_node',
    #     parameters=[controller_robot_description, diff_drive_controller],
    #     output={
    #       'stdout': 'screen',
    #       'stderr': 'screen',
    #       },
    # )
    start_rviz_cmd = Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(description_dir, 'rviz', 'robot.rviz')],
        )

    
    ld = LaunchDescription()
    ld.add_action(declare_world_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_rviz_cmd)
    ld.add_action(gazebo)
    ld.add_action(spawn_robot_cmd)
    # ld.add_action(start_controller_manager_cmd)

    return ld