#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import socket
from geometry_msgs.msg import PoseWithCovarianceStamped

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('192.168.1.99',10000)
sock.bind(server_addr)
rospy.loginfo("Server successfully booted")
sock.listen(1)
c,addr = sock.accept()

def pose_callback( message):
    x = message.pose.pose.position.x
    y = message.pose.pose.position.y
    z = message.pose.pose.orientation.z
    w = message.pose.pose.orientation.w
    x_str = str(x)[:8]
    y_str = str(y)[:8]
    z_str = str(z)[:8]
    w_str = str(w)[:8]
    str_out = (x_str + "," + y_str + "," + z_str + "," + w_str + ",")
    c.send(str_out.encode())
    rospy.loginfo("We got: %f %f %f %f"%(x,y,z,w))
    

def main():
    rospy.init_node('pose_broadcast', anonymous=True)
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
