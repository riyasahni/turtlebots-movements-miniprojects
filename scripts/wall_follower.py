#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

from geometry_msgs.msg import Twist

from geometry_msgs.msg import Vector3

# how close robot will get to wall
wall_distance = 0.55

class FollowWall(object):
	"""This node makes the robot follow a wall"""
	def __init__(self):

		# start rospy node
		rospy.init_node("follow_wall")

		# declare node as a subscriber to scan topic
		rospy.Subscriber("/scan", LaserScan, self.process_scan)

		# get a publisher to the cmd_vel topic
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

		# create a default twist msg (all vals 0)
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin, angular=ang)

	def process_scan(self, data):

		# case 1: only senses something in front (data.ranges <= 40, >=339)
			# go forward until you are set_dist away from wall
		# case 2: you are in front of the wall at set dist_away
			# turn robot 90 degrees so that (data.ranges > 40, <  
