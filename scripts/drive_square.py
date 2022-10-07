#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class MoveRobotSquare:
	def __init__(self):
		self.counter = 1
		rospy.init_node('drive_in_square')
		self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.move = Twist()
	def run(self):
		while not rospy.is_shutdown():
			if self.counter%2 == 0: # turn now
				self.move.angular.z = 0.55
				self.move.linear.x = 0
			else: # go straight
				self.move.angular.z = 0
				self.move.linear.x = 0.1
			self.counter += 1
			self.publisher.publish(self.move)
			rospy.sleep(3)

if __name__ == '__main__':
	node = MoveRobotSquare()
	node.run()
