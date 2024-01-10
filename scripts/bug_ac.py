#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Pose, Twist
from nav_msgs.msg import Odometry
import assign_2.msg
from assign_2.msg import posVel
import actionlib
import actionlib.msg
import time

#publisher for position and velocity
pvel=rospy.Publisher('/posVel', posVel, queue_size=1)

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
		enter=input("type anything to continue or 'c' to cancel the goal \n")
		if enter=='c':
			client.cancel_goal()
			print("goal cancelled")

		client.wait_for_result()



def main():
	rospy.init_node('bug0_client')

	#subscriver to /odom topic
	odom = rospy.Subscriber('/odom', Odometry, clbk_funct)
	
	bug0_client()
    

if __name__=='__main__':
	main()
