#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <stdlib.h>

//angular z is based on unit circle, from 0 to 2pi
double pi1=3.14159;
double pi2=pi1/2;
double pi4=pi1/4;
int count=0;
int x[]={2, 2, 2, 2, 2};
double z[]={0, pi4, pi4, 0, pi2};

int main(int argc, char**argv){
ros::init(argc, argv, "publish_velocity");
ros::NodeHandle nh;

ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("turtle1/cmd_vel", 1000);

srand(time(0));

ros::Rate rate(2);
while(ros::ok()){
geometry_msgs::Twist msg;

//msg.linear.x = double(rand())/double(RAND_MAX);
//msg.angular.z = 2*double(rand())/double(RAND_MAX) - 1;

//msg.linear.x = 0.5;
msg.linear.x = x[count];
msg.linear.y=msg.linear.x;

//msg.angular.z = 0.0;
msg.angular.z = z[count];

count++;
if(count==5){
	count=0;
}

pub.publish(msg);

ROS_INFO_STREAM("Sending velocity command:"<<" linear x="<<msg.linear.x<<" linear y=:"<<msg.linear.y<<" angular z="<<msg.angular.z<<" count="<<count);

ros::Duration(2).sleep();
}
}