#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <stdlib.h>

//angular z is based on unit circle, from 0 to 2pi
double pi1=3.14159; //pi
double pi2=pi1/2; //pi/2
double pi4=pi1/4; //pi/4
double pi3_2=3*pi1/2;
int count=0;
int total=0;
double x[]={0, 0, 2, 0, 2, 0, 2, 0, 2};
double z[]={0, pi2, 0, pi2, 0, pi2, 0, pi2, 0};

//if you give it an angle and a velocity, round curve
//if you give it no angle and just a velocity, straight line
//if you give it an angle and no velocity, it rotates

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

//msg.linear.x = 0;
msg.linear.x = x[count]/4;

//msg.angular.z = 0.0;
msg.angular.z = z[count];

//setting defaults to zero for the other params
msg.linear.y=0;
msg.linear.z=0;
msg.angular.x =0;
msg.angular.y=0;

/*if(count==5||count==9){
	msg.angular.z+=0.00001;
}*/

pub.publish(msg);

ROS_INFO_STREAM("Sending velocity command:"<<" linear x="<<msg.linear.x<<" linear y=:"<<msg.linear.y<<" angular z="<<msg.angular.z<<" count="<<count<<" total iterations="<<total);

count++;
total++;
if(count==9){
	count=0;
}

ros::Duration(2).sleep();
}
}
