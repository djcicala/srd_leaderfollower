#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class MBC():

	def __init__(self):
		rospy.init_node('follower_waypoints')
		rospy.loginfo("starting node...")
		
		self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		self.client.wait_for_server()
		self.dist_to_goal = 0.55
		
		self.current_x = 0
		self.current_y = 0
		self.current_z = 0
		self.current_w = 1

		self.fx = -0.5
		self.fy = 0
		
		self.l_sub = rospy.Subscriber('leader_pose', PoseWithCovarianceStamped, self.lead_callback)
		self.f_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.foll_callback)
		#self.r = rospy.Rate(0.5)		
		rospy.loginfo("node booted!")

		self.goal = MoveBaseGoal()
		self.goal.target_pose.header.frame_id = "map"
		self.goal.target_pose.header.stamp = rospy.Time.now()

		self.goal.target_pose.pose.position.x = self.current_x
		self.goal.target_pose.pose.position.y = self.current_y
		self.goal.target_pose.pose.orientation.z = self.current_z
		self.goal.target_pose.pose.orientation.w = self.current_w

		self.client.send_goal(self.goal)		
		
		while not rospy.is_shutdown():
			#self.r.sleep()
			#rospy.loginfo("comparing distance...")
			self.dist_to_goal = ((self.current_x-self.fx)**2 + (self.current_y-self.fy)**2) ** (0.5)
			if(self.dist_to_goal < 0.10):
				rospy.loginfo("setting new goal...")
				self.goal = MoveBaseGoal()
				self.goal.target_pose.header.frame_id = "map"
				self.goal.target_pose.header.stamp = rospy.Time.now()

				self.goal.target_pose.pose.position.x = self.lx
				self.goal.target_pose.pose.position.y = self.ly
				self.goal.target_pose.pose.orientation.z = self.lz
				self.goal.target_pose.pose.orientation.w = self.lw
			
				self.current_x = self.lx
				self.current_y = self.ly
				self.current_z = self.lz
				self.current_w = self.lw
				
				self.client.send_goal(self.goal)
				
				rospy.loginfo("new goal: x: %f y: %f z: %f w: %f"%(self.current_x, self.current_y, self.current_z, self.current_w))
	
	def lead_callback(self, lPose):
		self.lx = lPose.pose.pose.position.x
		self.ly = lPose.pose.pose.position.y
		self.lz = lPose.pose.pose.orientation.z
		self.lw = lPose.pose.pose.orientation.w
	
	def foll_callback(self, fPose):
		self.fx = fPose.pose.pose.position.x
		self.fy = fPose.pose.pose.position.y

if __name__ == "__main__":
	mbc = MBC()
		
