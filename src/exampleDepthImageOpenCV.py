import sys

import ctypes
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a, _k4atypes
import cv2
import cmapy
from matplotlib import cm
from matplotlib import pyplot as plt

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
	device_config.depth_mode = _k4a.K4A_DEPTH_MODE_NFOV_UNBINNED
	# Start cameras using modified configuration
	pyK4A.device_start_cameras(device_config)
	'''calib = _k4atypes.k4a_calibration_t()
	calib_res = pyK4A.device_get_calibration(device_config.depth_mode,device_config.color_resolution,calib)
	calib_dep = calib.depth_camera_calibration.extrinsics
	calib_dep1 = calib.depth_mode.bit_length;
	print("height: ",calib.depth_camera_calibration.resolution_height)
	print("width : ", calib.depth_camera_calibration.resolution_width)
	print("metric radius: ",calib.depth_camera_calibration.metric_radius)
	print("metric radius: ",calib.depth_camera_calibration.metric_radius)
	print("imag",calib.depth_camera_calibration.intrinsics.parameter_count.imag)
	print("cx",calib.depth_camera_calibration.intrinsics.parameters.param.cx)
	print("cx",calib.depth_camera_calibration.intrinsics.parameters.param.cx)
	
	print("cy",calib.depth_camera_calibration.intrinsics.parameters.param.cy)
	print("fx",calib.depth_camera_calibration.intrinsics.parameters.param.fx)
	print("fy",calib.depth_camera_calibration.intrinsics.parameters.param.fy)
	CDCCIPP = calib.depth_camera_calibration.intrinsics.parameters.param
	print("k1",CDCCIPP.k1)
	print("k2",CDCCIPP.k2)
	print("k2",CDCCIPP.k3)
	print("k2",CDCCIPP.k4)
	print("k2",CDCCIPP.k5)
	V= [i for i in calib.color_camera_calibration.intrinsics.parameters.v]
	print(V)
	
	V= [i for i in calib.color_camera_calibration.intrinsics.parameters.v]
	print(V)
	
	
	




	rotation = [x for x in calib_dep.rotation]
	translation = [x for x in calib_dep.translation]
	#bitlen = [x for x in calib_dep1]
	
	print(rotation)
	print(translation)'''
	k=1
	#print(bitlen)
	while True:
		# Get capture
		pyK4A.device_get_capture()

		# Get the depth image from the capture
		depth_image_handle = pyK4A.capture_get_depth_image()
		color_image_handle=pyK4A.capture_get_color_image()
		

		# Check the image has been read correctly
		if depth_image_handle:

			# Read and convert the image data to numpy array:
			depth_image= pyK4A.image_convert_to_numpy(depth_image_handle)
			
			#print(depth_color_image)
			#ret,thresh = cv2.threshold(depth_color_image,127,255,0)
			#im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
			depth_color_image = cv2.convertScaleAbs (depth_image, alpha=0.05)
			#alpha is fitted by visual comparison with Azure k4aviewer results  
			depth_color_image = cv2.applyColorMap(depth_color_image,cmapy.cmap("prism"))
			
			cv2.namedWindow('Controus',cv2.WINDOW_NORMAL)
			cv2.imshow('Contours',depth_color_image)
			k = cv2.waitKey(1)

			# Release the image
			pyK4A.image_release(depth_image_handle)

		pyK4A.capture_release()

		if k==27:    # Esc key to stop
			break
		

	pyK4A.device_stop_cameras()
	pyK4A.device_close()
