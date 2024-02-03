#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np

def process_compressed_image(msg):
    bridge = CvBridge()
    
    np_arr = np.frombuffer(msg.data, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    cv2.imshow("Decompressed Image", frame)
    cv2.waitKey(1)

def camera_subscriber():
    rospy.init_node('camera_subscriber2', anonymous=True)
    rospy.Subscriber('/camera2/image_raw/compressed', CompressedImage, process_compressed_image)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        camera_subscriber()
    except rospy.ROSInterruptException:
        pass
