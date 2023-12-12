import cv2
import time
import numpy as np
import yaml

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

def capture_images():
    camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=0),cv2.CAP_GSTREAMER)
    time.sleep(2)
    global image_files
    image_files = []

    for i in range(10):
        ret, frame = camera.read()
        if ret:
            file_name = str(f'calibration_image_{i}.jpg')
            image_files.append(file_name)
            cv2.imwrite(f'calibration_image_{i}.jpg', frame)

    camera.release()
    cv2.destroyAllWindows()


def calibrate_from_images():

    # Define the size of the checkerboard pattern
    checkerboard_size = (9, 6)  # Adjust according to your checkerboard

    # Arrays to store object points and image points from all calibration images
    obj_points = []  # 3D points in real-world space
    img_points = []  # 2D points in the image plane

    # Prepare object points (coordinates of the checkerboard corners in 3D space)
    objp = np.zeros((np.prod(checkerboard_size), 3), dtype=np.float32)
    objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)


    for image_file in image_files:
        img = cv2.imread(image_file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

        if ret:
            obj_points.append(objp)
            img_points.append(corners)

    # Perform camera calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    # Save calibration parameters to a YAML file
    calibration_data = {
        'camera_matrix': mtx.tolist(),
        'distortion_coefficients': dist.tolist(),
    }
    with open('camera_calibration.yaml', 'w') as yaml_file:
        yaml.dump(calibration_data, yaml_file)

    print("Camera calibration complete. Calibration parameters saved to camera_calibration.yaml.")

def main():
    capture_images()
    calibrate_from_images()

if __name__ == "__main__":
    main()

