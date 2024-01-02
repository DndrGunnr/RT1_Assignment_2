#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Pose, Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import assign_2.msg
import math
import actionlib
import actionlib.msg
from tf import transformations
from std_srvs.srv import *
import time


def bug0_client():
	#action client initialization
	client = actionlib.SimpleActionClient('/reaching_goal', assign_2.msg.PlanningAction)
	
	client.wait_for_server()
	#target coords input
	des_x=float(input("insert x coordinate: "))
	des_y=float(input("insert y coordinate: "))
	#construction of the message for the action server
	goal = assign_2.msg.PlanningGoal()
	goal.target_pose.pose.position.x=des_x
	goal.target_pose.pose.position.y=des_y

	#send the goal
	client.send_goal(goal)
	
	client.wait_for_result()
	
	return client.get_result()

if __name__=='__main__':
	try:
		rospy.init_node('bug0_client')
		result=bug0_client()
		print(result)
	except rospy.ROSInterruptException:
		print("program interrupted bedore completion", file=sys.stderr)
