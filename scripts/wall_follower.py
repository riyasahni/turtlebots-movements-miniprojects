#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

from geometry_msgs.msg import Twist

from geometry_msgs.msg import Vector3

# How close robot will get to human
stopping_distance = 0.4

class FollowPerson(object):
	"""This node makes the robot follow a person  """
	def __init__(self):

		# start rospy node
		rospy.init_node("follow_person")

		# declare node as a subscriber to scan topic
		rospy.Subscriber("/scan", LaserScan, self.process_scan)

		# get a publisher to the cmd_vel topic
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

		# create a default twist msg (all vals 0)
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin, angular=ang)

	def process_scan(self, data):

		# preset current distance from closest object and the angle it's at
		min_dist_from_object= 0
		min_angle = 0

		# loop through angles and find one where min_dist !=0
		for a in range(0, 359):
			if data.ranges[a] !=0:
				min_dist_from_object = data.ranges[a]
				min_angle = a
				break
		# scan full 360 and scope closest object from robot & angle it's at
		for a in range(0, 359):
			if(data.ranges[a]<=min_dist_from_object and data.ranges[a] !=0):
				min_dist_from_object = data.ranges[a]
				min_angle = a

		print("min angle", min_angle)
		print("min distance", min_dist_from_object)

		# check if robot is already within/at the set distance from the human
		if min_dist_from_object == 0 or min_dist_from_object <= stopping_distance:
		# if robot is facing human directly then stop
			if min_angle == 0 or min_dist_from_object == 0:
				self.twist.linear.x = 0
				self.twist.angular.z = 0
		# else turn robot until it faces human direcly
			else:
				self.twist.linear.x = 0
				self.twist.angular.z = 0.4

		# if robot is facing closest object, then move straight
		elif min_angle <=45 or min_angle >= 315:
			self.twist.linear.x = 0.1
			self.twist.angular.z = 0
		# else if closest object is directly behind then flip robot until it faces backwards
		elif (min_angle > 135 and min_angle <= 225):
			self.twist.linear.x = 0
			self.twist.angular.z = 0.5
		#  else if closest object is towards left of robot then turn robot left
		elif (min_angle > 45 and min_angle <= 135):
			self.twist.linear.x=0.1
			self.twist.angular.z = 0.3
		# else if closes object is towards right of robot  then turn robot right
		elif (min_angle > 225 and min_angle <= 315):
			self.twist.linear.x = 0.1
			self.twist.angular.z = -0.3

		# publish message to cmd_vel
		self.twist_pub.publish(self.twist)

	def run(self):
		# keep the program alive
		rospy.spin()

if __name__ == '__main__':
	# declare a node and run it
	node = FollowPerson()
	node.run()

