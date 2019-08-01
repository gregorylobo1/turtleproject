#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose

def reset():
	

	#starts new node
	rospy.init_node('turt_reset', anonymous=True)
	pose_publisher=rospy.Publisher('/turtle1/pose', Pose, queue_size=10)
	
	pos_msg = Pose()
	
	print("Hello World")
	
	rospy.sleep(1)
	
	pos_msg.x=3
	pos_msg.y=3
	pos_msg.theta=1.7
	pos_msg.linear_velocity=0
	pos_msg.angular_velocity=0
	
	pose_publisher.publish(pos_msg)


if __name__ == '__main__':
	try:
		#Testing our function
		reset()
	except rospy.ROSInterruptException: pass
