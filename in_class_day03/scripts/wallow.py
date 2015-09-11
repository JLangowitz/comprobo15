#!/usr/bin/env python

"""
Node for getting neato to hit things, back up, turn, go forward.
"""

import time

import rospy
from sensor_msgs.msg import LaserScan
from neato_node.msg import Bump
from geometry_msgs.msg import Twist

class Wallow():
    """Class for neato wall follow"""
    THRESHOLD = .5
    MOVEMENTS = {
        "LEFT": Twist(),
        "FORWARD": Twist(),
        "BACKWARD": Twist()
    }
    MOVEMENTS["LEFT"].angular.z = 1.0
    MOVEMENTS["FORWARD"].linear.x = 1.0
    MOVEMENTS["BACKWARD"].linear.x = -1.0

    def __init__(self):
        rospy.init_node("wallow")

    def _getting_too_far(self, ranges):
        if ranges[0] == 0.0 or ranges[0] > Wallow.THRESHOLD:
            return True
        return False

    def _handle_laser(self, laser_msg):
        """
        Stops the neato on a collision with something.
        Otherwise resumes forward motion

        laser_msg: message representing the laser scan
        """
        # print laser_msg
        if self.movement == Wallow.MOVEMENTS["BACKWARD"]:
            if self._getting_too_far(laser_msg.ranges):
                self.movement = Wallow.MOVEMENTS["LEFT"]
                time.sleep(1.0)
                self.movement = Wallow.MOVEMENTS["FORWARD"]

    def _handle_bump(self, bump_msg):
        """
        Stops the neato on a collision with something.
        Otherwise resumes forward motion

        bump_msg: message representing the bump
        """
        if self.movement == Wallow.MOVEMENTS["FORWARD"]:
            if any([bump_msg.leftFront, bump_msg.leftSide, bump_msg.rightFront, bump_msg.rightSide]):
                self.movement = Wallow.MOVEMENTS["BACKWARD"]

    def run(self):
        print "runnin runnin"
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.movement = Wallow.MOVEMENTS["FORWARD"]
        self.rate = rospy.Rate(10);
        rospy.Subscriber("/bump", Bump, self._handle_bump)
        rospy.Subscriber("/scan", LaserScan, self._handle_laser)
        while not rospy.is_shutdown():
            print(self.movement)
            self.pub.publish(self.movement)
            self.rate.sleep();

if __name__ == '__main__':
    Wallow().run()