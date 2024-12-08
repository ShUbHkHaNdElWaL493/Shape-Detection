#!/usr/bin/env python3

#   Shubh Khandelwal

import cv2
from cv_bridge import CvBridge
import math
import numpy as np
import pandas as pd
import rospy
from sensor_msgs.msg import Image

def preprocessing(image_gray):
    image_canny = cv2.Canny(image_gray, 0.05 * image_gray.max(), 0.09 * image_gray.max())
    image_gauss1 = cv2.GaussianBlur(image_canny, (0, 0), 3)
    image_gauss2 = cv2.GaussianBlur(image_canny, (0, 0), 4)
    image_dog = cv2.subtract(image_gauss1, image_gauss2)
    image_dog[image_dog > 0] = 255
    return image_dog

def distance(a, b):
    dist = 0
    for i in b.index:
        dist += (a.loc[i] - b.loc[i]) * (a.loc[i] - b.loc[i]) / (b.loc[i] * b.loc[i])
    return (math.sqrt(dist))

def process_image(msg):
    
    bridge = CvBridge()

    try:
    
        f = bridge.imgmsg_to_cv2(msg, "bgr8")
        f_gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        f_processed = preprocessing(f_gray)

        f_processed = np.uint8(f_processed)
        f_contours, f_hierarchy = cv2.findContours(f_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        index = -1
        f_contour = 0
        for i in range(len(f_contours)):
            if len(f_contours[i]) > f_contour:
                index = i
                f_contour = len(f_contours[i])

        f_values = []

        f_perimeter = cv2.arcLength(f_contours[index], True)
        f_epsilon = 0.03 * f_perimeter
        f_corners = cv2.approxPolyDP(f_contours[index], f_epsilon, True)
        f_values.append(len(f_corners))

        f_circularity = 4 * np.pi * (cv2.contourArea(f_contours[index]) / (cv2.arcLength(f_contours[index], True) * cv2.arcLength(f_contours[index], True)))
        f_values.append(f_circularity)

        f_moments = cv2.moments(f_contours[index])
        f_hu = cv2.HuMoments(f_moments)
        for j in range(len(f_hu)):
            f_hu[j] = math.log10(abs(f_hu[j]))
            f_values.append(f_hu[j])

        f_values = pd.Series(data = f_values, index = ["Corners", "Circularity", "H0", "H1", "H2", "H3", "H4", "H5", "H6"])
        distances = []
        shape = "nothing"
        folders = ["circle", "square", "triangle"]
        for j in folders:
            k = distance(f_values, sample_mean.loc[j])
            distances.append(k)
            if (k == np.min(distances)) & (k < 1):
                shape = j.upper()
        
        if shape != "nothing":
            cv2.drawContours(image = f, contours = f_contours, contourIdx = index, color = (0, 0, 255), thickness = 5, lineType = cv2.LINE_8, hierarchy = f_hierarchy)
            cX = int(f_moments["m10"] / f_moments["m00"])
            cY = int(f_moments["m01"] / f_moments["m00"])
            cv2.putText(f, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            rospy.loginfo(shape + " DETECTED")

        f_ros = bridge.cv2_to_imgmsg(f, "bgr8")
        image_publisher.publish(f_ros)
    
    except Exception as e:
        rospy.logerr("Error: %s", str(e))

def main():

    global sample_mean
    sample_mean = pd.read_csv("~/Documents/IIITDM Kancheepuram/Data Science/Project/Implementation/src/image_processor/include/mean.csv", index_col = "Index")

    rospy.init_node('image_processor_node', anonymous=True)

    global image_publisher
    image_publisher = rospy.Publisher('/camera/image', Image, queue_size=10)
    image_subscriber = rospy.Subscriber("/feed", Image, process_image)

    rospy.spin()

if __name__ == '__main__':
    main()
