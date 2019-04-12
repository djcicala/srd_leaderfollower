#!/usr/bin/env python

from geometry_msgs.msg import PoseWithCovarianceStamped
import rospy
from std_msgs.msg import Float32

class distCalc:
	
	def __init__(self):
		rospy.init_node('dist_calculator')
		rospy.loginfo("starting node...")
		self.dist_pub = rospy.Publisher('sep_dist', Float32, queue_size = 10)
	
		self.l_sub = rospy.Subscriber('leader_pose', PoseWithCovarianceStamped, self.lead_callback)
		self.f_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.foll_callback)
	
		self.r = rospy.Rate(1)
		rospy.loginfo("node booted!")
		self.lx = 0
		self.ly = 0
		
		self.fx = -0.5
		self.fy = 0

		self.lead_pose_flag = False
		self.foll_pose_flag = False

		while not rospy.is_shutdown():
			rospy.loginfo("checking for new positions...")
			if self.lead_pose_flag and self.foll_pose_flag:		
				dist_msg = Float32()	
				self.dist = ((self.lx-self.fx)**2 + (self.ly-self.fy)**2) ** (0.5)
				dist_msg.data = self.dist
				self.dist_pub.publish(dist_msg)
				rospy.loginfo("Current distance: %f"%(self.dist))
				self.lead_pose_flag = False
				self.foll_pose_flag = False
			self.r.sleep()
			
	
	def lead_callback(self, lPose):
		self.lx = lPose.pose.pose.position.x
		self.ly = lPose.pose.pose.position.y
		self.lead_pose_flag = True

	def foll_callback(self, fPose):
		self.fx = fPose.pose.pose.position.x
		self.fy = fPose.pose.pose.position.y
		self.foll_pose_flag = True

if(__name__ == "__main__"):
	dc = distCalc()
