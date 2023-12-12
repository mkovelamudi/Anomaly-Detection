import torch
import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
#import image_transport

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

class CameraPublisher(Node):

       def __init__(self):
           super().__init__('camera_publisher')
           self.publisher = self.create_publisher(Image, 'camera/image_raw', 10)
           self.info_publisher = self.create_publisher(Image, 'camera/image_info', 10)
           self.bridge = CvBridge()
           self.timer = self.create_timer(0.1, self.publish_image)
           #self.image_transport = image_transport.ImageTransport(self)

       def publish_image(self):
           # Capture video from the camera (adjust the camera index as needed)
           cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

           ret, frame = cap.read()
           if ret:
               # Convert the OpenCV image to a ROS Image message
               ros_image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
               self.publisher.publish(ros_image_msg)
               self.get_logger().info('Published camera image.')

def main(args=None):
       try:
        rclpy.init(args=args)
        camera_publisher = CameraPublisher()
        rclpy.spin(camera_publisher)
       finally:
        camera_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
