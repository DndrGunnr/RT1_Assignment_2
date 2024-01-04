#! /usr/bin/env python

import rospy
from assign_2.srv import *

def target_service(req):
	x=rospy.get_param("des_pos_x")
	y=rospy.get_param("des_pos_y")
	return targetResponse(x,y)

def main():
	rospy.init_node('target_service')
	srv=rospy.Service('target_service', target , target_service)
	
	rospy.spin()

if __name__=='__main__':
	main()
