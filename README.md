# ros_multicam_publisher
This project has one publisher which captures two video feeds and publish it using multithreading concept. So two threads are simultaneously publishing the video feed. Now there are two subsriber to this publisher which subscribes to the camera respectively. Each subscriber can now be used to perform different functions. 

Two threads are created, each calling publish_camera_feed() with different camera indices and publishers. These threads will run concurrently.
