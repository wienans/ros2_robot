# ros2_robot
export ROS_DOMAIN_ID=45

sudo apt install ros-foxy-xacro
sudo apt install ros-foxy-joint-state-publisher
ros2 control compilieren https://github.com/ros-controls/ros2_control
sudo apt install python3-vcstool
sudo apt install ros-foxy-test-msgs

## slam_toolbox:
service: 
ros2 service call /serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: 'map'}"
ros2 service call /save_map slam_toolbox/srv/SaveMap "{name: {data: ''}}"
ros2 service call /deserialize_map slam_toolbox/srv/DeserializePoseGraph "{filename: 'map', match_type: 2, initial_pose: {x: 0.0, y: 20.0, theta: 0}}"