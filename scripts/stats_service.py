#! /usr/bin/env python

import rospy
from assign_2.msg import posVel
from assign_2.srv import *
from math import dist

"""
..module:: stats_service

..platform: Unix

..synopsis: Python service for the computation of the distance from the target and the average linear velocity

..moduleauthor:: Enrico Dondero enrico.dondero.@gmail.com


"""

#variable counting number of samples from robot velocity
counter=0
#variable containing target coordinates
trgt=[0.0,0.0]
#list of recorded velocities
vels=[0]*rospy.get_param("avg_window")
#variable to store current position of robot, overwritten each time a new sample is available
position=[0,0]
#variable for average speed, overwritten once every averaging-window-lenght samples
avg_speed=0.0

#Function that it's called whenever a message is published on the /posVel topic.
#The vel array is used as the averaging window for the speed, the counter is used to iteratively cycle through
#the samples as the oldest ones are overwritten
def stats_clbk(pos_vel):
	"""
	callback function for the /posVel topic, the data obtained is stored in the vels array and the position is updated
	the average speed is computed and stored in the avg_speed variable

	args: pos_vel(posVel)
	"""
	global counter,vels,position,avg_speed
	position[0]=pos_vel.pos_x
	position[1]=pos_vel.pos_y
	vels[counter]=pos_vel.vel_x
	#for each callback a sample from the robot velocity is taken
	counter=counter+1
	#when all the samples are available, the average speed is computed
	if counter>(rospy.get_param("avg_window")-1):
		avg_speed=sum(vels)/rospy.get_param("avg_window")
		counter=0
	
	

#service that returns target coordinates and average linear velocity.
#Makes use of the target service for target coordinates retrieval
#this was done to make use of the target service
def stats_service(req):
	"""
	service that returns target coordinates and average linear velocity

	"""
	global trgt,avg_speed
	response=statsResponse()
	#service to retrieve target
	returned=(target())
	trgt=[returned.x,returned.y]
	#trgt[0]=rospy.get_param("des_pos_x")
	#trgt[1]=rospy.get_param("des_pos_y")
	response.dist=dist(trgt,position)
	response.avg_vel=avg_speed
	return response
	
	

def main():
	"""
	
	"""
	global target	
	#target service proxy init
	rospy.wait_for_service('target_service')
	target=rospy.ServiceProxy('target_service', target)
	
	#node init
	rospy.init_node('stats_service')
	
	#subscription to /posVel topic for position and velocity info
	sub =rospy.Subscriber('/posVel', posVel, stats_clbk)

	#stats service init
	stats_srv=rospy.Service('stats_service', stats, stats_service)
	rospy.spin()
	

	
if __name__=='__main__':
	main()
