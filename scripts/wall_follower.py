#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

from geometry_msgs.msg import Twist

from geometry_msgs.msg import Vector3

# set sleep toggle to determine when robot turns 90 degrees

class FollowWall(object):
	"""This node makes the robot follow a wall"""
	def __init__(self):
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
		# initialize variables to keep track of distances to and
		# angles of the closest objects to  front & left of the robot
		min_front_dist = 0
		min_front_angle = 0
		left_dist = 0
		left_angle = 0

		# find first non-zero values (if any) to set the 'min_front_dist'
		# and 'left_dist' variables to

		for a in range(0, 359):
			if (a <= 10 or a>=349) and data.ranges[a] != 0:
				min_front_dist=data.ranges[a]
			if(a > 45 and a <= 135) and data.ranges[a] != 0:
				left_dist = data.ranges[a]

		# finding the distance to nearest object to the front of robot
		# and saving the distance and angle it is at to robot
		for a in range(0, 10):
			if data.ranges[a] <= min_front_dist and data.ranges[a] != 0:
				min_front_dist = data.ranges[a]
				min_front_angle = a
		for a in range (349, 359):
			if data.ranges[a] <= min_front_dist and data.ranges[a] != 0:
				min_front_dist = data.ranges[a]
				min_front_angle = a

		# finding distance to nearest object to the left of robot
		# and saving nearest left distance and angle it is at to robot
		for a in range(35, 145):
			if data.ranges[a] <= left_dist  and data.ranges[a] != 0:
				left_dist = data.ranges[a]
				left_angle = a

		# default robot to just move forward if there is not left wall nearby or
		# any wall coming up in front
		if min_front_dist > 0.6:
			self.twist.linear.x = 0.1
			self.twist.angular.z = 0
		# case 1: wall on LHS and you are too far from it
		if (left_dist  > 0.5 and left_dist != float('inf')):
			self.twist.linear.x = 0.05
			self.twist.angular.z = 0.65 # turn towards wall to get closer
		if .35 <= left_dist <= 0.55:
			# adjust slightly into the wall to become more perpendicular
			if left_angle > 95:
				self.twist.linear.x = 0.08
				self.twist.angular.z = 0.7
			# else if too close, adjust slightly away from wall to become
			# more perpendicular
			elif left_angle < 85:
				self.twist.linear.x = 0.09
				self.twist.angular.z = -0.7
			# else if perpendicular to wall already, keep straight!
			else:
				self.twist.linear.x = 0.1
				self.twist.angular.z = 0
		# case 2: wall on LHS and you are too close to it
		elif left_dist < 0.25  and left_dist != 0:
			# turn away from wall to maintain distance b/w wall & robot
			self.twist.linear.x = 0.1
			self.twist.angular.z = -0.55

		# case 3: arrived front of wall and robot needs to turn some way
		if min_front_dist <= 0.6 and min_front_dist!=0:
			self.twist.linear.x = 0
			self.twist.angular.z = -0.65 # choosing to make robot turn right

		# publish the message
		self.twist_pub.publish(self.twist)

	def run(self):
		# keep the program alive
		rospy.spin()


if __name__ == '__main__':
	# declare a node and run it
	node = FollowWall()
	node.run()

