#!/usr/bin/env python

import socket
import rospy
import time
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.1.100'
port = 10001
s.connect((host,port))

rospy.init_node("stop_lead")
client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
client.wait_for_server()
rospy.loginfo("server initialized")

while (not rospy.is_shutdown()):
    try:
        stopmsg = s.recv(4)
        cmd = "{!r}".format(stopmsg)

        if(cmd == "'stop'"):
            rospy.loginfo("stop recieved")
            client.cancel_all_goals()
        else:
            rospy.loginfo_throttle(1, "Follower is OK")

    finally:		
		rospy.loginfo_throttle(2, "continue navigating")
