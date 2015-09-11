#!/usr/bin/env python

"""
Script for sending ROS messages in python
"""

import rospy
from geometry_msgs.msg import PointStamped, Point
from std_msgs.msg import Header

rospy.init_node("test_message")

point_msg = Point(x=1.0, y=2.0, z=0.0)
header_msg = Header(frame_id="odom")
msg = PointStamped(point=point_msg, header=header_msg)

pub = rospy.Publisher("/my_point", PointStamped, queue_size=10)

r = rospy.Rate(10)
while not rospy.is_shutdown():
    header_msg.stamp = rospy.Time.now()
    pub.publish(msg)
    r.sleep()