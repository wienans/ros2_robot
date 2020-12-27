import os
import sys

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchService
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
   # Load the URDF into a parameter
    description_dir = get_package_share_directory('robot_description')
    xacro_path = os.path.join(description_dir, 'urdf', 'robot.xacro')
    urdf_path = os.path.join(description_dir, 'urdf', 'robot.urdf')
    os.system("xacro -o {out_file_path} {in_file_path}".format(out_file_path=urdf_path,in_file_path=xacro_path))
    return LaunchDescription([
        Node(
            name='robot_state_publisher',
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description':Command(['xacro',' ', xacro_path])
                }],
        ),
        Node(
            name='joint_state_publisher',
            package='joint_state_publisher',
            executable='joint_state_publisher',
            arguments=[urdf_path],
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(description_dir, 'rviz', 'robot.rviz')],
        )
    ])