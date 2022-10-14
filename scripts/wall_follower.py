#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

from geometry_msgs.msg import Twist

from geometry_msgs.msg import Vector3

# set sleep toggle to determine when robot turns 90 degrees

class FollowWall(object):
	"""This node makes the robot follow a wall"""
	def __init__(self):
		# print("testing1")
		# start rospy node
		rospy.init_node("follow_wall19")

		# declare node as a subscriber to scan topic
		rospy.Subscriber("/scan", LaserScan, self.process_scan)

		# get a publisher to the cmd_vel topic
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

		# create a default twist msg (all vals 0)
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin, angular=ang)

	def process_scan(self, data):
		# print("testing wall follow")
		# create an array [f, l, r] that keeps track of dist from
		# robot to nearest object on its front, left and right sides
		min_front_dist = 0
		min_front_angle = 0
		left_dist = 0
		left_angle = 0
		# fill in array with distances to nearest robot object on towards its front,
		# left, and right sides

		for a in range(0, 359):
			if (a <= 10 or a>=349) and data.ranges[a] != 0:
				min_front_dist=data.ranges[a] # find first non-zero distance in front of robot
			if(a > 45 and a <= 135) and data.ranges[a] != 0:
				left_dist = data.ranges[a]

		# finding the distance to nearest object in front of robot
		# saving nearest front distance and the angle it falls in
		for a in range(0, 10):
			if data.ranges[a] <= min_front_dist and data.ranges[a] != 0:
				min_front_dist = data.ranges[a]
				min_front_angle = a
		for a in range (349, 359):
			if data.ranges[a] <= min_front_dist and data.ranges[a] != 0:
				min_front_dist = data.ranges[a]
				min_front_angle = a

		# finding distance to nearest object to the left of robot
		# saving nearest left distance and angle it falls in
		for a in range(45, 135):
			if data.ranges[a] <= left_dist  and data.ranges[a] != 0:
				left_dist = data.ranges[a]
				left_angle = a

		self.twist.linear.x = 0.1
		self.twist.angular.z = 0

		# case 3: wall on LHS
		if left_dist  > 0.75:
			print("turning towards wall")
			self.twist.linear.x = 0.1
			self.twist.angular.z = 0.7
		elif .25 <= left_dist <= 0.75:
			print("going parallel to wall")
			if left_angle > 95:
				self.twist.linear.x = 0.1
				self.twist.angular.z = 0.6
			elif left_angle < 85:
				self.twist.linear.x = 0.1
				self.twist.angular.z = -0.6
			else:
				self.twist.linear.x = 0.1
				self.twist.angular.z = 0
		elif left_dist < 0.25  and left_dist != 0:
			print("turning away from wall")
			self.twist.linear.x = 0.1
			self.twist.angular.z = -0.7

		# case 2: in front of wall and need to turn.
		if min_front_dist < wall_distance and min_front_dist!=0:
			print("need to turn")
			self.twist.linear.x = 0
			self.twist.angular.z = -0.6 # choosing to make robot turn right



		self.twist_pub.publish(self.twist)

	def run(self):
		rospy.spin()


if __name__ == '__main__':
	node = FollowWall()
	node.run()

