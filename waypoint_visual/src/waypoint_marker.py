#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from visualization_msgs.msg import Marker


class Markers():
    def __init__(self):
        rospy.init_node('markerz',anonymous=True)
        self.markerPub = rospy.Publisher('waypointMarker', Marker, queue_size=50)
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped,self.pose_callback)

        rospy.spin()



    def pose_callback(self, message):
      
        
        x = message.pose.pose.position.x
        y = message.pose.pose.position.y
        z = message.pose.pose.orientation.z
        w = message.pose.pose.orientation.w

        self.waypointMarker = Marker()

        self.waypointMarker = Marker()
        self.waypointMarker.header.frame_id = "/map"
        self.waypointMarker.header.stamp    = rospy.get_rostime()

        self.waypointMarker.id = i
        self.waypointMarker.type = 0 # arrow
        self.waypointMarker.action = 0
        self.waypointMarker.scale.x = .25
        self.waypointMarker.scale.y = .25
        self.waypointMarker.scale.z = .10

        self.waypointMarker.color.r = 0/255
        self.waypointMarker.color.g = 0/255
        self.waypointMarker.color.b = 255/255
        self.waypointMarker.color.a = 1.0

        self.waypointMarker.pose.position.x = x
        self.waypointMarker.pose.position.y = y
        self.waypointMarker.pose.orientation.z = z
        self.waypointMarker.pose.orientation.w = w

        rospy.loginfo("printing")
        self.markerPub.publish(self.waypointMarker)

if (__name__ == "__main__"):
    visWay = Markers()
