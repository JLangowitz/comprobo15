#!/usr/bin/env python

"""
Node for getting neato to stop when it hits something
"""

import rospy
from neato_node.msg import Bump
from geometry_msgs.msg import Twist

class EmergencyStop():
    """Class that stops the neato on collision"""
    
    def __init__(self):
        rospy.init_node("emergency_stop")
        
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

    def _handle_bump(self, bump_msg):
        """
        Stops the neato on a collision with something.
        Otherwise resumes forward motion

        bump_msg: message representing the bump
        """
        # print bump_msg
        if any([bump_msg.leftFront, bump_msg.leftSide, bump_msg.rightFront, bump_msg.rightSide]):
            self._stop()
        else:
            self._forward()

    def run(self):
        print "runnin runnin"
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.movement = Twist()
        self.rate = rospy.Rate(10);
        rospy.Subscriber("/bump", Bump, self._handle_bump)
        while not rospy.is_shutdown():
            self.pub.publish(self.movement)
            self.rate.sleep();

if __name__ == '__main__':
    EmergencyStop().run()