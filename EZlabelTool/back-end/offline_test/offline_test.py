# -*- coding: UTF-8 -*-
# Date: 3 May 2021
# Author：Pingyi Hu a1805597
# Description：The repetition of labels

import sys
import csv
import re
import matplotlib.pyplot as plt
import numpy as np
import cv2

# get filename from command line
filename = sys.argv[1]
path = "./" + filename
csv_reader = csv.reader(open(path))
rows = [row for row in csv_reader]
for i in range(1, len(rows)):
    image_name = re.split(r'(?:[;:\s]\s*)',rows[i][1])[2]
    image_path = "./images/" + image_name
    image = cv2.imread(image_path)
    label_info = rows[i][2]
    bbox_info = label_info.split("Bounding Box : ")[1]
    bbox_info = bbox_info.split(" ; Polygon")[0]
    bbox_info = bbox_info.strip("[")
    bbox_info = bbox_info.strip("]")
    bboxs = bbox_info.split("}, {")
    polygon_info = label_info.split("; Polygon : ")[1]
    polygon_info = polygon_info.strip("[")
    polygon_info = polygon_info.strip("]")
    polygons = polygon_info.split("}, {")
    for bbox in bboxs:
        bbox = bbox.strip("{")
        bbox = bbox.strip("}")
        info = re.split(r'(?:[,;:\s{}]\s*)', bbox)
        if len(info) > 1:
            x = int(info[1].split('.')[0])
            y = int(info[3].split('.')[0])
            h = int(info[5].split('.')[0])
            w = int(info[7].split('.')[0])
            ptLeftTop = (x, y)
            ptRightBottom = (x+w, y+h)
            point_color = (0, 0, 255) # BGR red
            thickness = 2
            lineType = 8
            # draw rectangle on image
            cv2.rectangle(image, ptLeftTop, ptRightBottom, point_color, thickness, lineType)
    for polygon in polygons:
        polygon = polygon.strip("{")
        polygon = polygon.strip("}")
        info = re.split(r'(?:[,;:\s{}]\s*)', polygon)
        if len(info) > 1:
            start_index = info.index("'points'") + 1
            end_index = len(info)
            number = end_index - start_index
            a = np.arange(number)
            for i in range(start_index, end_index):
                info[i] = info[i].strip("[")
                info[i] = info[i].strip("]")
                a[i-start_index] = int(info[i].split('.')[0])
            points = a.reshape(int(number/2), 2)
            point_color = (255, 0, 0) # BGR blue
            thickness = 2
            # draw polygons on image
            cv2.polylines(image, pts=[points], isClosed=True, color=point_color, thickness=thickness)
    cv2.imshow("labels", image)
    re_path = "./results/" + image_name
    cv2.imwrite(re_path, image)
    cv2.waitKey(0)
