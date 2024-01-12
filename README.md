 # Description
 The package contains 5 nodes (written in 5 Python script files). 
`bug_as` is the action server that provides the brain to the robot, it makes use of two alternating services called `go_to_point_service` and `wall_follower_services`, which help the robot to navigate in the environment.  
The nodes written for this assignment were:  
* `bug_ac`: contains two distinct parts:
  * `bug0_client`: which is the action client coupled with `bug_as`. This allows the interaction of the user with the action server and then with the robot. This requires some target coordinates provided through the shell by the user. After the coordinates are successfully sent to the server, the user is free to cancel the current goal of the robot and change it.  
  * `clbk_funct`: is the callback function associated with the subscriber to the `/odom` topic. This provides extensive information about the robot's pose and velocities. This node takes the planar position of the robot and its linear velocity along the x-axis and angular velocity along the z-axis and publishes them on a custom topic called `/posVel`.  
Below a flowchart for the logic of the `bug_ac` node:
  
![flow2 drawio](https://github.com/DndrGunnr/RT1_Assignment_2/assets/80176557/44d1eca8-920e-455a-aca1-72fe7c15434c)

* `target_service`: service providing the cartesian coordinates of the target, by retrieving them from the parameters server, these are transmitted through a custom service called `target.srv`
* `stats_service`:service provides the Euclidean distance between the target and the robot's current position, this is done in two separate blocks of code:
  * `stats_clbk`: is the callback linked to a subscriber to the `/posVel` topic. Each time a message is published there, this function retrieves and stores the current position and linear velocity. The latter is used to compute the average through a moving window (customizable through the `assignment1.launch` file, changing the value contained in the variable `avg_window`).
  * `stats_service`: provides on demand the average linear velocity computed in the callback function and the current distance between the robot and the target, which are retrieved using the `target_service`.  
# How to run
To run this package using noetic ROS, you must place the contents of this directory in a folder named `assign_2` inside the `src` folder of the ROS workspace.  
This is because the package name is indeed `assign_2`.  
Then in the root folder of the ROS workspace, you must run from the shell the command `$catkin_make` to build the package.  
Finally, you can type in `$roslaunch assign_2 assignment1.launch` to launch the program.
# Possible improvements
Possible improvements apart from boosts in speed, may be the logic of the robot itself, in this implementation the robot always follows the walls keeping it on the right. This is a simple solution but far from the optimal one. By changing how the information about the laser range finder is elaborated, the robot could become capable of choosing the most appropriate way to get around obstacles.  
The feedback information produced by the action client could be further developed in order to give the user a better idea of what the robot is doing without necessarily looking at the simulation.



