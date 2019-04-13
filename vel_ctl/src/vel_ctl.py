#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class VC():
	
	def __init__(self):
		rospy.init_node("vel_ctl")
		rospy.loginfo("starting node...")

		self.current_dist = 0.5

		self.current_vel = Twist()
		self.current_vel.linear.x = 0
		self.current_vel.angular.z = 0

		self.vel_sub = rospy.Subscriber('move_base_cmd_vel', Twist, self.vel_callback)
		self.d_sub = rospy.Subscriber('sep_dist', Float32, self.dist_callback)	
		self.cv_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
		
		rospy.loginfo("node booted!")
		rospy.spin()

	def vel_callback(self, cmdVel):
		self.current_vel = cmdVel
		self.x = self.current_vel.linear.x
		self.z = self.current_vel.angular.z
		if(self.current_dist > 0.6 and self.x > 0):
			self.current_vel.linear.x = 0.11
			self.cv_pub.publish(self.current_vel)
			rospy.loginfo("increasing speed")
		elif(self.current_dist < 0.4 and self.x > 0):
			self.current_vel.linear.x = 0.07
			self.cv_pub.publish(self.current_vel)
			rospy.loginfo("decreasing speed")
		else:
			self.cv_pub.publish(self.current_vel)
			rospy.loginfo("maintaining current speed of x: %f z: %f"%(self.x, self.z))

	def dist_callback(self, dist):
		self.current_dist = dist.dat


if( __name__ == "__main__"):
	vc = VC()
