#!/usr/bin/env python
"""
Node for robot teleop
"""

import rospy
import tty
import select
import sys
import termios
from geometry_msgs.msg import Twist, Vector3

movements = {
    "forward" : Twist(linear=Vector3(x=1)),
    "left" : Twist(angular=Vector3(z=1)),
}

def main():
    rospy.init_node("drive_square")

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    turn_duration = rospy.Duration(1.65)
    move_duration = rospy.Duration(2.75)
    rospy.sleep(rospy.Duration(1.5))
    for x in xrange(4):
        pub.publish(movements["forward"])
        rospy.sleep(move_duration)
        pub.publish(movements["left"])
        rospy.sleep(turn_duration)
    pub.publish(Twist())

if __name__ == '__main__':
    main()