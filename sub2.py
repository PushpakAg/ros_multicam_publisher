#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading

def process_image2(msg):
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

    # Your processing logic for camera2 feed

    # Display the camera2 feed
    cv2.imshow("Camera 2 Feed", frame)
    cv2.waitKey(1)

def camera_subscriber2():
    rospy.init_node('camera_subscriber2', anonymous=True)
    
    rospy.Subscriber('/camera2/image_raw', Image, process_image2)

    rospy.spin()

if __name__ == '__main__':
    try:
        camera_subscriber2()
    except rospy.ROSInterruptException:
        pass
