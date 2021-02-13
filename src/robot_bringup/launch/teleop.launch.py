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

    start_key_teleop = Node(
        package="teleop_twist_keyboard",
        node_executable="teleop_twist_keyboard",
        output='screen',
        prefix = 'xterm -e',
        node_name='teleop',
        remappings=[
            ("cmd_vel", "/differential_drive_controller/cmd_vel")]
        )
    ld = LaunchDescription()
    ld.add_action(start_key_teleop)

    return ld