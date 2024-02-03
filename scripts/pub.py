#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import threading

def publish_compressed_camera_feed(camera_index, publisher, bridge, rate, shutdown_event):
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    while not shutdown_event.is_set():
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, (640, 480))
            # Compress the image using JPEG encoding
            _, compressed_image = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

            # Convert the compressed image to bytes
            compressed_bytes = compressed_image.tobytes()

            # Create CompressedImage message
            compressed_msg = CompressedImage()
            compressed_msg.header.stamp = rospy.Time.now()
            compressed_msg.format = 'jpeg'
            compressed_msg.data = compressed_bytes

            # Publish the compressed image message
            publisher.publish(compressed_msg)
        
        rate.sleep()

    cap.release()

def camera_publisher():
    rospy.init_node('camera_publisher', anonymous=True)
    rate = rospy.Rate(10) 

    image_pub1 = rospy.Publisher('/camera1/image_raw/compressed', CompressedImage, queue_size=10)
    image_pub2 = rospy.Publisher('/camera2/image_raw/compressed', CompressedImage, queue_size=20)
    bridge = CvBridge()

    shutdown_event = threading.Event()

    thread1 = threading.Thread(target=publish_compressed_camera_feed, args=(0, image_pub1, bridge, rate, shutdown_event))
    thread2 = threading.Thread(target=publish_compressed_camera_feed, args=(1, image_pub2, bridge, rate, shutdown_event))

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
