#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading

def publish_camera_feed(camera_index, publisher, bridge, rate, shutdown_event):
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    while not shutdown_event.is_set():
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame,(640,480))
            image_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            publisher.publish(image_msg)
        rate.sleep()
    cap.release()

def camera_publisher():
    rospy.init_node('camera_publisher', anonymous=True)
    rate = rospy.Rate(10) 

    image_pub1 = rospy.Publisher('/camera1/image_raw', Image, queue_size=10)
    image_pub2 = rospy.Publisher('/camera2/image_raw', Image, queue_size=20)
    bridge = CvBridge()

    shutdown_event = threading.Event()

    thread1 = threading.Thread(target=publish_camera_feed, args=(0, image_pub1, bridge, rate, shutdown_event))
    thread2 = threading.Thread(target=publish_camera_feed, args=(1, image_pub2, bridge, rate, shutdown_event))

    thread1.start()
    thread2.start()

    rospy.spin()

    shutdown_event.set()
    thread1.join()
    thread2.join()

if __name__ == '__main__':
    try:
        camera_publisher()
    except rospy.ROSInterruptException:
        pass
