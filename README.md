# Anomaly-Detection-Backend

## Image Pipeline
![pipeline (2)](https://github.com/mkovelamudi/Anomaly-Detection-Frontend/assets/99615170/bb780d2e-6643-4b21-ae8a-43126b955877)

# Setup (On Jetson)
Tested on Jetson Orin Nano Developer kit with Raspberry Pi V2 camera

Make sure Jetson Orin Nano Developer Kit is flashed and all the dependencies installed on it. Follow https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit for setup. You can also use any cuda environment, but make sure Nvidia Isaac ROS dependent libraries are installed.

## Object Detection pipeline Setup
1. Following the development environment setup above, you should have a ROS2 workspace named ```workspaces/isaac_ros-dev```. Clone this repository and its dependencies under ```workspaces/isaac_ros-dev/src```:
```
cd ~/workspaces/isaac_ros-dev/src
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nitros.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_dnn_inference.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_pipeline
git clone https://github.com/mkovelamudi/Anomaly-Detection-Backend.git
```

## Model preparation
In this project, model is directly trained in Ultralytics website and the trained model is exported to ONNX format provided by Ultralytics.
Copy this model into S3 bucket and the provide S3 bucket URL in the frontend application when prompted, this will automatically copy the model into Jetson device.
