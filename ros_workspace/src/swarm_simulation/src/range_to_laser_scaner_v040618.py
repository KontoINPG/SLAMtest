#!/usr/bin/env python

import rospy 
import math
import tf


from sensor_msgs.msg import LaserScan, Range
from sensor_msgs.msg import Range

Scan_msg = LaserScan()
Range_msg = Range()

LaserFrequency = 5 # frequency of scanning by range sensors.

pub = rospy.Publisher('laser/laser_scan', LaserScan, queue_size=10)

Scan_msg.header.frame_id = 'RangeLaserFrame'
Scan_msg.angle_min = 0
Scan_msg.angle_max = 2*math.pi
Scan_msg.angle_increment = 2*math.pi/6

#Scan_msg.scan_time = 0.5
Scan_msg.range_min = 0.10000000149
Scan_msg.range_max = 30
Scan_msg.intensities = []



RangesTable = []
for lA in range(0,8):
	RangesTable.append(0)


RangesBL = 0
RangesBR = 0
RangesCB = 0
RangesCF = 0
RangesCL = 0
RangesCR = 0
RangesFL = 0
RangesFR = 0

def scanRangeSensors():
	rospy.init_node('RangesToLaserScan')

	rospy.Subscriber('laser/scan/bl', Range, readBL)
	rospy.Subscriber('laser/scan/br', Range, readBR)

	rospy.Subscriber('laser/scan/cb', Range, readCB)
	rospy.Subscriber('laser/scan/cf', Range, readCF)

	rospy.Subscriber('laser/scan/cl', Range, readCL)
	rospy.Subscriber('laser/scan/cr', Range, readCR)

	rospy.Subscriber('laser/scan/fl', Range, readFL)
	rospy.Subscriber('laser/scan/fr', Range, readFR)

	

	rospy.spin()

def readBL(data):
	global RangesBL
	RangesBL = data.range
	

def readBR(data):
	global RangesBR
	RangesBR = data.range

def readCB(data):
	global RangesCB
	RangesCB = data.range

def readCF(data):
	global RangesCF
	RangesCF = data.range

def readCL(data):
	global RangesCL
	RangesCL = data.range

def readCR(data):
	global RangesCR
	RangesCR = data.range

def readFL(data):
	global RangesFL
	RangesFL = data.range

def readFR(data):
	global RangesFR
	RangesFR = data.range
	sendFrame() # sending frame after reading last range sensor.


    









def sendFrame():

	RangesTable[0] = RangesCF
	RangesTable[1] = RangesFL
	RangesTable[2] = RangesCL
	RangesTable[3] = RangesBL
	RangesTable[4] = RangesCB
	RangesTable[5] = RangesBR
	RangesTable[6] = RangesCR
	RangesTable[7] = RangesFR


	Scan_msg.header.stamp = rospy.Time.now()
	Scan_msg.ranges = RangesTable
	Scan_msg.time_increment = (1.0/LaserFrequency)/6
	pub.publish(Scan_msg)


if __name__ == '__main__':
    scanRangeSensors()
