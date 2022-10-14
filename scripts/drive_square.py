#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class MoveRobotSquare:
	""" This node moves a turtlebot in a square pattern. """
	def __init__(self): # define node, publisher, and initiate toggle
		self.counter = 1
		rospy.init_node('drive_in_square')
		self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.move = Twist()
	def run(self):
		print("testing in drive square")
		while not rospy.is_shutdown():
			if self.counter%2 == 0: # if toggle is even, turn now
				self.move.angular.z = 0.55
				self.move.linear.x = 0
			else: # if toggle is odd go straight
				self.move.angular.z = 0
				self.move.linear.x = 0.1
			self.counter += 1 # update the toggle by incrementing by 1
			self.publisher.publish(self.move)
			rospy.sleep(3) # allow robot to travel straight or to turn for 3 seconds before switching motion

if __name__ == '__main__':
	node = MoveRobotSquare()
	node.run()
