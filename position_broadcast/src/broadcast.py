#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import socket
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Twist

class BC():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = ('192.168.1.99',10000)
        self.sock.bind(self.server_addr)
        rospy.loginfo("Server successfully booted")
        self.sock.listen(1)
        self.xV_str="0.000000"
        self.zA_str="0.000000"
        self.first_send = False
        self.c,self.addr = self.sock.accept()
        rospy.init_node('pose_broadcast', anonymous=True)
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.pose_callback)
        rospy.Subscriber('/cmd_vel', Twist, self.velocity_callback)
        rospy.spin()

    def pose_callback(self, message):
        x = message.pose.pose.position.x
        y = message.pose.pose.position.y
        z = message.pose.pose.orientation.z
        w = message.pose.pose.orientation.w
        self.x_str = str(x)[:8]
        self.y_str = str(y)[:8]
        self.z_str = str(z)[:8]
        self.w_str = str(w)[:8]
        str_out = (self.x_str + "," + self.y_str + "," + self.z_str + "," + self.w_str + "," + self.xV_str + "," + self.zA_str + ",")
        self.c.send(str_out.encode())
        rospy.loginfo("We got: %f %f %f %f %s %s"%(x,y,z,w,self.xV_str,self.zA_str))

    def velocity_callback(self, message):
        xV = message.linear.x
        zA = message.angular.z
        if(xV > 0 or zA > 0):
            self.first_send = False
        if(xV >= 0):
            self.xV_str = "{:.6f}".format(xV)
        else:
            self.xV_str = "{:.5f}".format(xV)

        if(self.xV_str.find("-") > -1 and not (xV < -0.005)):
            self.xV_str = self.xV_str[1:]
        if(zA >= 0):
            self.zA_str = "{:.6f}".format(zA)
        else:
            self.zA_str = "{:.5f}".format(zA)

        if(self.zA_str.find("-") > -1 and not (zA < -0.005)):
            self.zA_str = self.zA_str[1:]
        if(xV == 0 and zA == 0 and self.first_send == False):
            str_out = (self.x_str + "," + self.y_str + "," + self.z_str + "," + self.w_str + "," + self.xV_str + "," + self.zA_str + ",")
            self.c.send(str_out.encode())
            self.first_send = True

if __name__ == '__main__':
    bc = BC()
