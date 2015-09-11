#!/usr/bin/env python

"""
Script for receiving ROS messages in python
"""

import rospy
from geometry_msgs.msg import PointStamped

def process_point(msg):
	print msg

rospy.init_node("receive_message")
rospy.Subscriber("/my_point", PointStamped, process_point)

r = rospy.Rate(10)
while not rospy.is_shutdown():
    r.sleep()