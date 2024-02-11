#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Pose, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from assign_2.srv import *
from sensor_msgs.msg import LaserScan
import assign_2.msg
from assign_2.msg import posVel, obstDist
import actionlib
import actionlib.msg
import time

#publisher for position and velocity
pvel=rospy.Publisher('/posVel', posVel, queue_size=1)
obstdist=rospy.Publisher('/obstDist', obstDist, queue_size=1)

#Function called whenever the action server some feedback updates.
#Each state message is filtered while the achievement of goal is printed

def feedback_clbk(feedback):
	if feedback.stat=="Target reached!":
		print(feedback.stat)


#Callback function for the topic /odom, the message is repurposed 
#and some information is published on the /posVel topic

def clbk_funct(odometry):
	#creation of instance custom message
	msg=posVel()
	msg.pos_x=odometry.pose.pose.position.x
	msg.pos_y=odometry.pose.pose.position.y
	msg.vel_x=odometry.twist.twist.linear.x
	msg.vel_z=odometry.twist.twist.angular.z
	#publishing the message
	pvel.publish(msg)
	
def clbk_laser(scan):
    global regions_
    regions_ = {
        'right':  min(min(scan.ranges[0:143]), 10),
        'fright': min(min(scan.ranges[144:287]), 10),
        'front':  min(min(scan.ranges[288:431]), 10),
        'fleft':  min(min(scan.ranges[432:575]), 10),
        'left':   min(min(scan.ranges[576:719]), 10),
    }
    min_key= min(regions_, key=regions_.get)
    min_value=regions_.get(min_key)
    msg=obstDist()
    msg.direction=min_key
    msg.distance=min_value
    obstdist.publish(msg)
	



#Main body of the action client. Once initialized this will provide the user with 
#interactive prompts. For each iteration of the while loop the user is asked to enter the target 
#coordinates that are sent to the action server for the robot to reach. The user is free to 
#cancel the  goal anytime by entering 'c' while the node waits for the robot to reach its target before 
#another iteration (or before the user shuts down the nodes). By canceling the goal the cycle
#is preemptively finished, so the user will be prompted again to enter the target coordinates.

def bug0_client():
	#action client initialization
	client = actionlib.SimpleActionClient('/reaching_goal', assign_2.msg.PlanningAction)
	client.wait_for_server()
	while not rospy.is_shutdown():
    	#the node waits 3 seconds before prompting the user to avoid 
    	#the user prompt to be lost between roslaunch messages
		rospy.sleep(3)
		#the try-except block will prevent the user from crashing the node 
    	#by entering values other than numbers
		while True:
			try:
				des_x=float(input("insert x coordinate: "))
				des_y=float(input("insert y coordinate: "))
				break
			except Exception as e:
				print("You have to enter numbers for coordinates!")

		#construction of the message for the action server
		goal = assign_2.msg.PlanningGoal()
		goal.target_pose.pose.position.x=des_x
		goal.target_pose.pose.position.y=des_y
		#send the goal
		client.send_goal(goal, feedback_cb=feedback_clbk)
		while True:
			enter=input("type 'c' to cancel the goal, 't' to get the target coordinates, or 'p' to continue \n")
			if enter=='c':
				client.cancel_goal()
				print("goal cancelled")
			elif enter=='t':
				print("target coords:\n ",target())
			elif enter=='p':
				break

		client.wait_for_result()



def main():
	global target
	rospy.init_node('bug0_client')
	
	#target service proxy init
	rospy.wait_for_service('target_service')
	target=rospy.ServiceProxy('target_service', target)

	#subscriver to /odom topic
	odom = rospy.Subscriber('/odom', Odometry, clbk_funct)
	
	#subscriber to /scan topic
	sub_laser = rospy.Subscriber('/scan', LaserScan, clbk_laser)
	
	bug0_client()
    

if __name__=='__main__':
	main()
