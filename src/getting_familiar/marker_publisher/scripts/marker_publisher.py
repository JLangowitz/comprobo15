#!/usr/bin/env python

"""
Node to publish Markers to a constant position (1,2,0) at 10 Hz
Run with `rosrun getting_familiar marker_publisher.py`
"""

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose, Point, Vector3
from std_msgs.msg import ColorRGBA, Header

rospy.init_node('marker_message');

def main():
	point = Point(x=1, y=2)
	pose = Pose(position=point)
	color = ColorRGBA(r=.4, g=0, b=.8, a=1.0)
	header = Header(frame_id="odom")
	scale = Vector3(x=.5, y=.5, z=.5)
	marker_msg = Marker(type=Marker.SPHERE, pose=pose, color=color, header=header, scale=scale)

	pub = rospy.Publisher("/my_marker", Marker, queue_size=10)
	r = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		header.stamp = rospy.Time.now()
		pub.publish(marker_msg)
		r.sleep()


if __name__ == '__main__':
	main()