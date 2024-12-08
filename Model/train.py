#   Shubh Khandelwal

import cv2
import math
import numpy as np
import os
import pandas as pd

def preprocessing(image_gray):
    image_canny = cv2.Canny(image_gray, 0.05 * image_gray.max(), 0.09 * image_gray.max())
    image_gauss1 = cv2.GaussianBlur(image_canny, (0, 0), 3)
    image_gauss2 = cv2.GaussianBlur(image_canny, (0, 0), 4)
    image_dog = cv2.subtract(image_gauss1, image_gauss2)
    image_dog[image_dog > 0] = 255
    return image_dog


folders = ["circle", "square", "triangle"]
sample_mean = pd.DataFrame(columns = ["Corners", "Circularity", "H0", "H1", "H2", "H3", "H4", "H5", "H6"], index = folders)

for folder_name in folders:

    sample = pd.DataFrame(columns = ["File", "Corners", "Circularity", "H0", "H1", "H2", "H3", "H4", "H5", "H6"])

    for file_name in os.listdir("dataset/train/" + folder_name):

        print(folder_name + ": " + file_name)

        file_path = "dataset/train/" + folder_name + "/" + file_name
        f = cv2.imread(file_path)
        f_gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        f_processed = preprocessing(f_gray)

        f_processed = np.uint8(f_processed)
        f_contours, f_hierarchy = cv2.findContours(f_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        f_contour = []
        for i in f_contours:
            if len(i) > len(f_contour):
                f_contour = i

        f_perimeter = cv2.arcLength(f_contour, True)
        f_epsilon = 0.03 * f_perimeter
        f_corners = cv2.approxPolyDP(f_contour, f_epsilon, True)

        f_circularity = 4 * np.pi * (cv2.contourArea(f_contour) / (cv2.arcLength(f_contour, True) * cv2.arcLength(f_contour, True)))

        f_moments = cv2.moments(f_contour)
        f_hu = cv2.HuMoments(f_moments)
        for i in range(len(f_hu)):
            f_hu[i] = math.log10(abs(f_hu[i]))

        concat_df = pd.DataFrame({"File" : [file_name], "Corners" : [len(f_corners)], "Circularity" : [f_circularity], "H0" : f_hu[0], "H1" : f_hu[1], "H2" : f_hu[2], "H3" : f_hu[3], "H4" : f_hu[4], "H5" : f_hu[5], "H6" : f_hu[6]})
        sample = pd.concat([sample, concat_df], ignore_index=True)

    sample.to_csv(folder_name + ".csv", index = False)
    sample_mean.loc[folder_name] = (sample.drop(["File"], axis = 1)).mean()

    print()

sample_mean.to_csv("mean.csv", index_label = "Index")

print("Training complete!")