import sys
import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a,_k4atypes
import cv2
import cmapy


# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

# under x86_64 linux please use r'/usr/lib/x86_64-linux-gnu/libk4a.so'
# In Jetson please use r'/usr/lib/aarch64-linux-gnu/libk4a.so'

if __name__ == "__main__":

    # Initialize the library with the path containing the module
    pyK4A = pyKinectAzure(modulePath)

    # Open device
    pyK4A.device_open()

    # Modify camera configuration
    device_config = pyK4A.config
    device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_1080P
    device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
    # Start cameras using modified configuration
    pyK4A.device_start_cameras(device_config)

    
    k = 0
    j=1
    for i in cmapy.cmap('prism'):
        if(j<65 or j>75):
            i[0][0] = 0
            i[0][1] = 0
            i[0][2] = 0
        if(j==65):
            i[0][0] = 66
            i[0][1] = 76
            i[0][2] = 235
        if(j==66):
            i[0][0] = 54
            i[0][1] = 90
            i[0][2] = 255
        if(j==67):
            i[0][0] = 94
            i[0][1] = 111
            i[0][2] = 254
        if(j==68):
            i[0][0] = 0
            i[0][1] = 234
            i[0][2] = 255
        if(j==69):
            i[0][0] = 0
            i[0][1] = 255
            i[0][2] = 223
        if(j==70):
            i[0][0] = 50
            i[0][1] = 205
            i[0][2] = 50
        if(j==71):
            i[0][0] = 255
            i[0][1] = 191
            i[0][2] = 0
        if(j==72):
            i[0][0] = 255
            i[0][1] = 127
            i[0][2] = 0
        if(j==73):
            i[0][0] = 255
            i[0][1] = 112
            i[0][2] = 0
        if(j==74 or j == 75):
            i[0][0] = 198
            i[0][1] = 79
            i[0][2] = 33
        
    
            
            
        j+=1
    
        
            
                
    while True:
        # Get capture
        pyK4A.device_get_capture()

        # Get the color and  depth image from the capture
        color_image_handle = pyK4A.capture_get_color_image()
        depth_image = pyK4A.capture_get_depth_image()
        #color_image_handle = pyK4A.transformation_color_image_to_depth_camera()

        # Check the image has been read correctly
        if color_image_handle:

            # Read and convert the image data to numpy array:
            color_image = pyK4A.image_convert_to_numpy(color_image_handle)
            print(color_image)

            depth_image_= pyK4A.image_convert_to_numpy(depth_image)
            
            #depth = pyK4A.transform_depth_to_color(depth_image,color_image_handle)
            #depth = depth[500:10000,0:10000]
            
            # Plot the image

            #color_image = pyK4A.transform_depth_to_color(depth_image,color_image_handle)
            depth_color_image = cv2.convertScaleAbs (depth_image_, alpha=0.05)
            #alpha is fitted by visual comparison with Azure k4aviewer results  
            depth_color_image = cv2.applyColorMap(depth_color_image[190:305,170:345],cmapy.cmap("prism"))
            
            """gray = cv2.cvtColor(depth_color_image,cv2.COLOR_BGR2GRAY)
            cv2.namedWindow('Color ',cv2.WINDOW_NORMAL)
            cv2.imshow("Color ",gray)
            ret, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_OTSU)
            contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(depth_color_image, contours, 1, (0,0,0), 5)"""


            cv2.namedWindow('Color Image',cv2.WINDOW_NORMAL)
            cv2.imshow("Color Image",depth_color_image)
            k = cv2.waitKey(1)

            # Release the image
            pyK4A.image_release(color_image_handle)

        pyK4A.capture_release()

        if k==27:    # Esc key to stop
            break

    pyK4A.device_stop_cameras()
    pyK4A.device_close()


