cmake_minimum_required(VERSION 3.5)
project(robot_description)


# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}/
)
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)
install(
  DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
