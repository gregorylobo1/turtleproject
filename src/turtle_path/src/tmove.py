#!/usr/bin/env python
#import libraries for rospy and math
import rospy
import math

#import rosmsg data to be used
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3

#define global variabls

global xpos
global ypos
global theta
global xdat
global ydat



##################################################################################################
#Absolute Distance
##################################################################################################
def abs_dist(x,y):

	total=math.sqrt(x*x+y*y)

	return total




##################################################################################################
#Find goal angle
##################################################################################################
def angle_goal(xgoal,ygoal):


	global xpos
	global ypos
	global theta

	thetag=math.atan2((ygoal),(xgoal))/math.pi*180
	print(thetag)
	thetag=theta+thetag

	return thetag


##################################################################################################
#Find Direction to turn
##################################################################################################
def angle_direction(xgoal,ygoal):

	global xpos
	global ypos
	global theta
	angular_speed=1;

	thetag=math.atan2((ygoal),(xgoal))/math.pi*180

	if(thetag<-10):
		return -angular_speed
	elif(thetag>10):
		return angular_speed
	else:
		return 0
##################################################################################################
#updates the data from the sensors
##################################################################################################
def update(data):

	global xpos
	global ypos
	global theta

	#find pose values
	xpos=(data.pose.pose.position.x)
	ypos=(data.pose.pose.position.y)
	z=(data.pose.pose.orientation.z)
	w=(data.pose.pose.orientation.w)
	theta=math.asin(2*w*z)/math.pi*180

	#conversion of angle
	if(abs(z)>abs(w)):
		if(z>0):
			theta=180-theta
		elif(z<=0):
			theta=-180-theta

##################################################################################################
#updates the data from the sensors
##################################################################################################

def valset(data):

	global xdat
	global ydat

	xdat=data.x
	ydat=data.y
##################################################################################################
#Main Function
##################################################################################################
def move():


	global xpos
	global ypos
	global theta
	global xdat
	global ydat

	#defining Variables
	angular_speed=1

	xpos=0
	ypos=0
	theta=0

	#starts new node
	rospy.init_node('followcmds', anonymous=True)

	#velocity publisher for pioneer
	velocity_publisher=rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=1)
	vel_msg = Twist()

	#pose subsciber calls update function
	pose_subs=rospy.Subscriber('/RosAria/pose', Odometry, update, queue_size=1)

	#coordinate Subscriber
	coord_subs=rospy.Subscriber('/vector', Vector3, valset, queue_size=1)

	#get input
	rospy.sleep(1)


	while not rospy.is_shutdown():

		print("Program start....")
		xgoal=xdat
		print(xgoal)
		ygoal=ydat
		print(ygoal)

		#calculate goal angle relative to the robot's pose
		thetag=angle_goal(xgoal,ygoal)
		vel_msg.angular.z=angle_direction(xgoal,ygoal)
		angleflag=0

		distance=abs_dist(xgoal,ygoal)


		#set velocity values
		vel_msg.linear.y=0
		vel_msg.linear.z=0
		vel_msg.angular.x=0
		vel_msg.angular.y=0

		vel_msg.linear.x=0.3
		distance=abs_dist(xgoal,ygoal)
		if(xdat<0):
			vel_msg.linear.x=0
			print "too short"


		#move to correct angle
		r=rospy.Rate(10)
		while(angleflag<3) and not rospy.is_shutdown():
			print(thetag-theta)

			if(abs(thetag-theta)<2):
				vel_msg.angular.z=0

			velocity_publisher.publish(vel_msg)
			angleflag=angleflag+1
			r.sleep()









if __name__ == '__main__':
	try:
		#Testing our function
		move()
	except rospy.ROSInterruptException: pass
