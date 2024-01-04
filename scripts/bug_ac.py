#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Pose, Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import assign_2.msg
from assign_2.msg import posVel
import math
import actionlib
import actionlib.msg
from tf import transformations
from std_srvs.srv import *
import time

#publisher for position and velocity
pvel=rospy.Publisher('/posVel', posVel, queue_size=1)


def clbk_funct(odometry):
	#creation of instance custom message
	msg=posVel()
	msg.pos_x=odometry.pose.pose.position.x
	msg.pos_y=odometry.pose.pose.position.y
	msg.vel_x=odometry.twist.twist.linear.x
	msg.vel_y=odometry.twist.twist.linear.y
	#publishing the message
	pvel.publish(msg)



def bug0_client():
	#action client initialization
	client = actionlib.SimpleActionClient('/reaching_goal', assign_2.msg.PlanningAction)
	client.wait_for_server()
	while not rospy.is_shutdown():
    	#target coords input
		des_x=float(input("insert x coordinate: "))
		des_y=float(input("insert y coordinate: "))
		#saving parameters on params server in order to be used by target_service node
		rospy.set_param('des_pos_x',des_x)
		rospy.set_param('des_pos_y',des_y)
		#construction of the message for the action server
		goal = assign_2.msg.PlanningGoal()
		goal.target_pose.pose.position.x=des_x
		goal.target_pose.pose.position.y=des_y
		#send the goal
		client.send_goal(goal)
		if input("type anything to continue or 'c' to cancel the goal")=='c':
			client.cancel_goal()
			print("goal cancelled")

		client.wait_for_result()
		print(client.get_result())

def main():
	rospy.init_node('bug0_client')

	#subscriver to /odom topic
	odom = rospy.Subscriber('/odom', Odometry, clbk_funct)
	
	bug0_client()
    

if __name__=='__main__':
	main()
