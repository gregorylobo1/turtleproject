#!/usr/bin/env python
#import libraries for rospy and math
import rospy
import math

#import rosmsg data to be used
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2
from std_msgs.msg import Header



def publishdata(x,y,z):

	pub=rospy.Publisher("mypoints", PointCloud2, queue_size=1)

	pts=[]

	for i in range(len(x)):
		pt=[float(x[i]), float(y[i]), float(z[i])]
		pts.append(pt)
		#print(pt)

	fields = [PointField('x', 0, PointField.FLOAT32, 1),
          PointField('y', 4, PointField.FLOAT32, 1),
          PointField('z', 8, PointField.FLOAT32, 1),
          ]

	header = Header()

	header.frame_id = "map"

	mypc2 = pc2.create_cloud(header, fields, pts)

	mypc2.header.stamp = rospy.Time.now()
	pub.publish(mypc2)
	print "sending..."
	#print(mypc2 )



def update(data):

	x=[]
	y=[]
	z=[]

	for p in pc2.read_points(data, field_names = ("x", "y", "z"), skip_nans=True):
		#print " x : %f  y: %f  z: %f" %(p[0],p[1],p[2])
		#Here p[0] is X p[1] is Y and P[2] is Z for each point
		x.append(p[0])
		y.append(p[1])
		z.append(p[2])


	publishdata(x,y,z)




def find():

	#starts new node
	rospy.init_node('kinect_pos', anonymous=True)


	#pose subsciber calls update function
	pose_subs=rospy.Subscriber('/camera/depth/points', PointCloud2, update, queue_size=1)



	while not rospy.is_shutdown():
		#print("waiting...")
		#rospy.sleep(1)
		rospy.spin()


if __name__ == '__main__':
	try:
		#Testing our function
		find()
	except rospy.ROSInterruptException: pass
