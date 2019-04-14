#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Float32
import Queue

class MBC():

	def __init__(self):
		rospy.init_node('follower_waypoints')
		rospy.loginfo("starting node...")
		
		# start the movebaseaction client
		self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		self.client.wait_for_server()

		# initial conditions		
		self.dist_to_goal = 0.55
		self.current_x = 0
		self.current_y = 0
		self.current_z = 0
		self.current_w = 1
		self.dist_to_leader = 0

		self.fx = -0.5
		self.fy = 0

		self.lead_vel_x = 0
		self.lead_vel_z = 0

		self.pose_list = Queue.Queue()

		
		# create subscriber objects
		self.l_sub = rospy.Subscriber('leader_pose', PoseWithCovarianceStamped, self.lead_callback)
		self.f_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.foll_callback)
		self.vel_sub = rospy.Subscriber('leader_vel', Twist, self.vel_callback)
		self.d_sub = rospy.Subscriber('sep_dist', Float32, self.dist_callback)		
		rospy.loginfo("node booted!")

		# header information for the goal
		self.goal = MoveBaseGoal()
		#self.goal.target_pose.header.frame_id = "map"
		#self.goal.target_pose.header.stamp = rospy.Time.now()
		
		# positional/rotational information for the goal
		#self.goal.target_pose.pose.position.x = self.current_x
		#self.goal.target_pose.pose.position.y = self.current_y
		

		# fifo manipulation
		#self.pose_list.put(self.goal)
		
		# send the initial goal to the server
		#self.client.send_goal(self.goal)		
		
		while not rospy.is_shutdown():
	
			self.dist_to_goal = ((self.current_x-self.fx)**2 + (self.current_y-self.fy)**2) ** (0.5)
			
			# case where robot is sufficiently close to the next goal, so advance to the next point			
			if(self.dist_to_goal < 0.10 and (self.lead_vel_x > 0 or self.lead_vel_z > 0)):
				rospy.loginfo("setting new goal...")
				self.goal = MoveBaseGoal()
				self.goal.target_pose.header.frame_id = "map"
				self.goal.target_pose.header.stamp = rospy.Time.now()

				self.goal = self.pose_list.get()
			
				self.current_x = self.goal.target_pose.pose.position.x
				self.current_y = self.goal.target_pose.pose.position.y
				self.client.cancel_goal()
				self.client.send_goal(self.goal)
				
				rospy.loginfo("new goal: x: %f y: %f z: %f w: %f"%(self.current_x, self.current_y, self.current_z, self.current_w))
			
			# case where leader is stopped and we're too close to it			
			elif(self.dist_to_leader < 0.5 and (self.lead_vel_x == 0 and self.lead_vel_z == 0)):
				self.client.cancel_all_goals()			
				self.pose_list.queue.clear()
				rospy.loginfo_throttle(1, "Leader stopped. Idly waiting for new movement...")
			
			# case where the follower has no points in its queue but the leader is moving
			elif(self.pose_list.qsize() >= 0 and (self.lead_vel_x > 0 or self.lead_vel_z > 0)):
				self.goal = MoveBaseGoal()
				self.goal.target_pose.header.frame_id = "map"
				self.goal.target_pose.header.stamp = rospy.Time.now()

				self.goal = self.pose_list.get()
			
				self.current_x = self.goal.target_pose.pose.position.x
				self.current_y = self.goal.target_pose.pose.position.y
				
				self.client.send_goal(self.goal)	

		# case where the follower is idly navigating but not too close to the next target (todo: vel control)
			else:
				rospy.loginfo_throttle(1, "navigating to current goal: x: %f y: %f"%(self.current_x, self.current_y))

	def lead_callback(self, lPose):
		new_waypoint = MoveBaseGoal()
		new_waypoint.target_pose.header.frame_id = "map"
		new_waypoint.target_pose.header.stamp = rospy.Time.now()
		new_waypoint.target_pose.pose.position.x = lPose.pose.pose.position.x
		new_waypoint.target_pose.pose.position.y = lPose.pose.pose.position.y
		new_waypoint.target_pose.pose.orientation.z = lPose.pose.pose.orientation.z
		new_waypoint.target_pose.pose.orientation.w = lPose.pose.pose.orientation.w
		rospy.loginfo("waypoint received! destination: %f %f"%(new_waypoint.target_pose.pose.position.x, new_waypoint.target_pose.pose.position.y))
		self.pose_list.put(new_waypoint)	

	def foll_callback(self, fPose):
		self.fx = fPose.pose.pose.position.x
		self.fy = fPose.pose.pose.position.y

	def vel_callback(self, lVel):
		self.lead_vel_x = lVel.linear.x
		self.lead_vel_z = lVel.angular.z


	def dist_callback(self, dist):
		self.dist_to_leader = dist.data

if __name__ == "__main__":
	mbc = MBC()
		
