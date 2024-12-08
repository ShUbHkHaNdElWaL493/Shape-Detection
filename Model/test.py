#   Shubh Khandelwal

import cv2
import math
import matplotlib.pyplot as plt
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

def distance(a, b):
    dist = 0
    for i in a.index:
        dist += (a.loc[i] - b.loc[i]) * (a.loc[i] - b.loc[i]) / (b.loc[i] * b.loc[i])
    return (math.sqrt(dist))

folders = ["circle", "square", "triangle"]
sample_mean = pd.read_csv("mean.csv", index_col = "Index")

confusion_matrix = pd.DataFrame(columns = folders, index = folders)
for i in confusion_matrix.index:
    for j in confusion_matrix.columns:
        confusion_matrix.loc[i, j] = 0

print("Error Cases:")

for folder_name in folders:

    for file_name in os.listdir("dataset/test/" + folder_name):

        file_path = "dataset/test/" + folder_name + "/" + file_name
        f = cv2.imread(file_path)
        f_gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        f_processed = preprocessing(f_gray)
        f_values = []

        f_processed = np.uint8(f_processed)
        f_contours, f_hierarchy = cv2.findContours(f_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        f_contour = []
        index = -1
        for i in range(len(f_contours)):
            if len(f_contours[i]) > len(f_contour):
                f_contour = f_contours[i]
                index = i

        f_perimeter = cv2.arcLength(f_contour, True)
        f_epsilon = 0.03 * f_perimeter
        f_corners = cv2.approxPolyDP(f_contour, f_epsilon, True)
        f_values.append(len(f_corners))

        f_circularity = 4 * np.pi * (cv2.contourArea(f_contour) / (cv2.arcLength(f_contour, True) * cv2.arcLength(f_contour, True)))
        f_values.append(f_circularity)

        f_moments = cv2.moments(f_contour)
        f_hu = cv2.HuMoments(f_moments)
        for i in range(len(f_hu)):
            f_hu[i] = math.log10(abs(f_hu[i]))
            f_values.append(f_hu[i])

        f_values = pd.Series(data = f_values, index = ["Corners", "Circularity", "H0", "H1", "H2", "H3", "H4", "H5", "H6"])

        distances = []
        shape = "nothing"
        for i in folders:
            k = distance(f_values, sample_mean.loc[i])
            distances.append(k)
            if (k == np.min(distances)) & (k < 1):
                shape = i

        if shape != folder_name:
            print((file_path + " : " + shape))
        
        confusion_matrix.loc[folder_name, shape] += 1
        
positive = 0
negative = 0
for i in confusion_matrix.index:
    positive += confusion_matrix.loc[i, i]
for i in confusion_matrix.index:
    for j in confusion_matrix.columns:
        if i == j:
            continue
        negative += confusion_matrix.loc[i, j]

print("\nAccuracy:", 100 * positive / (positive + negative))
print("\nConfusion Matrix:")
print(confusion_matrix.to_string())
print("\nCorrelation Analysis:")

values_x = list([])
values_y = list([])
means_x = list([])
means_y = list([])

for folder_name in folders:

    sample = pd.read_csv(folder_name + ".csv")

    correlation_analysis = pd.DataFrame(columns = ["Corners", "Circularity", "H0", "H1", "H2", "H3", "H4", "H5", "H6"], index = ["Corners", "Circularity", "H0", "H1", "H2", "H3", "H4", "H5", "H6"])
    for i in correlation_analysis.index:
        for j in correlation_analysis.columns:
            numerator = 0
            denominator1 = 0
            denominator2 = 0
            for k in sample.index:
                x = sample.loc[k, i] - sample_mean.loc[folder_name, i]
                y = sample.loc[k, j] - sample_mean.loc[folder_name, j]
                numerator += x * y
                denominator1 += x * x
                denominator2 += y * y
            denominator = math.sqrt(denominator1 * denominator2)
            if (numerator == 0) & (denominator == 0):
                if i == j:
                    correlation_analysis.loc[i, j] = 1.0
                else:
                    correlation_analysis.loc[i, j] = 0.0
            else:
                correlation_analysis.loc[i, j] = numerator / denominator
    
    values_x.append(list(sample.loc[:, 'Corners'].astype(float)))
    values_y.append(list(sample.loc[:, 'Circularity']))
    means_x.append(sample_mean.loc[folder_name, "Corners"])
    means_y.append(sample_mean.loc[folder_name, "Circularity"])

    print("\n" + folder_name.upper() + ":")
    print(correlation_analysis.to_string())

print("Scatter Plot:\n")
plt.scatter(values_x[0], values_y[0], color = "red", label = folders[0])
plt.scatter(values_x[1], values_y[1], color = "blue", label = folders[1])
plt.scatter(values_x[2], values_y[2], color = "green", label = folders[2])
plt.scatter(means_x, means_y, color = "black", label = 'means')
plt.xlabel("Corners")
plt.ylabel("Circularity")
plt.legend()
plt.show()