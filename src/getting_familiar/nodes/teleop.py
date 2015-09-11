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

keyBinds = {
    "w" : Twist(linear=Vector3(x=1)),
    "a" : Twist(angular=Vector3(z=1)),
    "d" : Twist(angular=Vector3(z=-1)),
    "s" : Twist()
}

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    rospy.init_node("teleop", anonymous=True)
    print "Move with WASD!\nW = forward\nA = left\nD = right\nS = stop"
    settings = termios.tcgetattr(sys.stdin)
    key = None
    movement = Twist()

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    while key != '\x03':
        key = getKey(settings)
        if key in keyBinds.keys():
            movement = keyBinds[key]
        pub.publish(movement)

if __name__ == '__main__':
	main()