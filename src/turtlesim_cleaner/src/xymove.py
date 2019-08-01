#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

x_pos=0
y_pos=0

def do(data):
	
	global x_pos
	global y_pos

	x_pos=(data.pose.pose.position.x)
	y_pos=(data.pose.pose.position.y)
	

def move():

	global x_pos
	global y_pos

    # Starts a new node
	rospy.init_node('robot_moving', anonymous=False)
    
	velocity_publisher = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=10)
	
	pose_subscriber = rospy.Subscriber("/RosAria/pose", Odometry, do)
	
	vel_msg = Twist()
		
    #Receiveing the user's input
	rospy.sleep(1)
	print("Current Location:")
	print(x_pos,y_pos)
	print("Let's move your robot")	
	speed = input("Input your speed:")
	distance = input("Type your distance:")
	isForward = input("Foward?: ")#True or False
    
    #Checking if the movement is forward or backwards
	if(isForward):
		vel_msg.linear.x = abs(speed)
	else:
		vel_msg.linear.x = -abs(speed)
    #Since we are moving just in x-axis
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
    
	while not rospy.is_shutdown():

		#Setting the current time for distance calculus
		t0 = rospy.Time.now().to_sec()
		current_distance = 0

        #Loop to move the turtle in an specified distance
		while(current_distance < distance):
            #Publish the velocity
			velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
			t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
			current_distance= speed*(t1-t0)
        #After the loop, stops the robot
		vel_msg.linear.x = 0
        #Force the robot to stop
		velocity_publisher.publish(vel_msg)
		
		print("Current Location:")
		print(x_pos,y_pos)
		rospy.sleep(5)



if __name__ == '__main__':
	try:
        #Testing our function
		move()
	except rospy.ROSInterruptException: pass
