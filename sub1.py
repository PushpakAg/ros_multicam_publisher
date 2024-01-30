#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading

def process_image1(msg):
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

    # Your processing logic for camera1 feed

    # Display the camera1 feed
    cv2.imshow("Camera 1 Feed", frame)
    cv2.waitKey(1)

def camera_subscriber1():
    rospy.init_node('camera_subscriber1', anonymous=True)
    
    rospy.Subscriber('/camera1/image_raw', Image, process_image1)

    rospy.spin()

if __name__ == '__main__':
    try:
        camera_subscriber1()
    except rospy.ROSInterruptException:
        pass
