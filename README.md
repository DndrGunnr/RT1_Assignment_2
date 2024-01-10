To run this package using noetic ROS, you must place the contents of this directory in a folder named `assign_2` inside the `src` folder of the ROS workspace.  
This is because the package name is indeed `assign_2`.  
The package contains 5 nodes (written in 5 Python script files).  
`bug_as` is the action server that provides the brain to the robot, it makes use of two alternating services called `go_to_point_service` and `wall_follower_services`, which help the robot to navigate in the environment.  
The nodes written for this assignment were:  
* `bug_ac`: which is the action client coupled with its server. This serves to set targets for the robot, canceling goals and providing information to the user through shell messages.   
While also publishing on topic `/posVel` position and velocities, more information below:
* `target_service`: service providing the cartesian coordinates of the target, by retrieving them from the parameters server, these are transmitted in the form of **to be continued**
* `stats_service`:service providing the Euclidean distance between the target and the current position of the robot, together with its average linear velocity. The latter is computed through an averaging window that can be
changed in size through the launch file as the variable `avg_window`

