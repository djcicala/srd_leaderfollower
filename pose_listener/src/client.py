#!/usr/bin/env python
import socket
import time
import rospy 
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.1.99'
port = 10000
s.connect((host, port))

rospy.init_node("pose_recv")
pose_pub = rospy.Publisher('leader_pose', PoseWithCovarianceStamped, queue_size=3)
vel_pub = rospy.Publisher('leader_vel', Twist, queue_size = 3)
#r = rospy.rate(1)

while True:
	try:
		test = s.recv(54)
		pose_str = "{!r}".format(test)
		pose_list = pose_str.split(",")
		rospy.loginfo("received {!r}".format(test))
		pose_obj = PoseWithCovarianceStamped()
		vel_obj = Twist()
		pose_obj.pose.pose.position.x = float(pose_list[0][1:])
		pose_obj.pose.pose.position.y = float(pose_list[1])
		pose_obj.pose.pose.orientation.z = float(pose_list[2])
		pose_obj.pose.pose.orientation.w = float(pose_list[3])
		vel_obj.linear.x = float(pose_list[4])
		vel_obj.angular.z = float(pose_list[5])
		pose_pub.publish(pose_obj)
		vel_pub.publish(vel_obj)
	finally:
		rospy.loginfo("waiting for position")
		time.sleep(1)
	
