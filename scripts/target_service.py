#! /usr/bin/env python

import rospy
from assign_2.srv import target,targetResponse

#The function gets info about the robot target by checking the parameter server
#for the variables updated by the action server
def target_service(req):
	coords=targetResponse()
	coords.x=rospy.get_param("des_pos_x")
	coords.y=rospy.get_param("des_pos_y")
	return coords

def main():
	rospy.init_node('target_service')
	srv=rospy.Service('target_service', target , target_service)
	
	#used to prevent the node from shutting down
	rospy.spin()

if __name__=='__main__':
	main()
