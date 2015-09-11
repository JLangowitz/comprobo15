#!/usr/bin/env python

"""
Node for getting neato to stop when it is close to something
"""

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class DistanceEmergencyStop():
    """Class that stops the neato on collision"""
    THRESHOLD = .5

    def __init__(self):
        rospy.init_node("distance_emergency_stop")
        
    def _stop(self):
        """
        Stops the neato
        """
        self.movement.linear.x = 0.0

    def _forward(self):
        """
        Tells the neato to move forward
        """
        self.movement.linear.x = 1.0

    def _getting_too_close(self, ranges):
        for i in xrange(len(ranges)):
            if ranges[i] != 0.0 and ranges[i] < DistanceEmergencyStop.THRESHOLD:
                return True
        return False


    def _handle_laser(self, laser_msg):
        """
        Stops the neato on a collision with something.
        Otherwise resumes forward motion

        laser_msg: message representing the laser scan
        """
        # print laser_msg
        if self._getting_too_close(laser_msg.ranges):
            self._stop()
        else:
            self._forward()

    def run(self):
        print "runnin runnin"
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.movement = Twist()
        self.rate = rospy.Rate(10);
        rospy.Subscriber("/scan", LaserScan, self._handle_laser)
        while not rospy.is_shutdown():
            print(self.movement)
            self.pub.publish(self.movement)
            self.rate.sleep();

if __name__ == '__main__':
    DistanceEmergencyStop().run()