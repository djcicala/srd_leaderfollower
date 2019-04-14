#!/usr/bin/env python

import socket 
from rosgraph_msgs.msg import Log
import rospy


class SC:
	
	def __init__(self):
		rospy.loginfo("starting node...")
		rospy.init_node('stop_client', anonymous=True)

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_addr = ('192.168.1.100', 10001)
		self.s.bind(self.server_addr)
		
		rospy.loginfo("server successfully booted")
		self.s.listen(1)

		self.c,self.addr = self.s.accept()
		self.rosout_sub = rospy.Subscriber('/rosout', Log, self.log_callback)
		rospy.loginfo("node booted!")
		rospy.spin()
		

	def log_callback(self, msg):
		message = msg.msg
		if(message.find("DWA planner failed to produce path") > -1 or message.find("Rotate recovery behavior started")> -1):
			rospy.loginfo("Follower is stuck, sending stop to leader")
			self.c.send("stop".encode())
		#else:
			#self.c.send("cont".encode())	

if(__name__ == "__main__"):
	sc = SC()
