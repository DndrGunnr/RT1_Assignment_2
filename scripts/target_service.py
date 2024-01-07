#! /usr/bin/env python

import rospy
from assign_2.srv import target

def target_service(req):
	coords=[0,0]
	coords[0]=rospy.get_param("des_pos_x")
	coords[1]=rospy.get_param("des_pos_y")
	return targetResponse(coords)

def main():
	rospy.init_node('target_service')
	srv=rospy.Service('target_service', target , target_service)
	
	rospy.spin()

if __name__=='__main__':
	main()
