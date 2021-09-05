# -*- coding:utf-8 -*-
# Date: 29 April 2021
# Author：Pingyi Hu a1805597
# Description：The service of tasks

import hashlib
import sqlite3
import json
import uuid
import datetime
import time
import csv

import sys
sys.path.append('..')
from model.TaskDB import TaskDB
from model.LabelDB import LabelDB
from model.Label_infoDB import Label_infoDB

import controller.Util as Util

image_database = LabelDB("../EZlabel.db")
image_info_database = Label_infoDB("../EZlabel.db")
taskDB = TaskDB('../EZlabel.db')

# handle create a csv file and export_info
def create_export(project_id):
    filename = str(time.time()) + "project" + str(project_id) + ".csv"
    url = "http://192.168.0.202:5000/api/v1/export/" + filename
    path = "./export/" + filename
    with open(path,'w') as f:
        csv_write = csv.writer(f)
        csv_head = ["image_id","image_info","label_info","classification","review_state","label_time","dataset_name"]
        csv_write.writerow(csv_head)
    image_rows = image_database.get_all_image(str(project_id))
    for image_row in image_rows:
        image_id = image_row[0]
        image_info = "image_name : " + str(image_row[2]) + " ; url : " + str(image_row[4]) 
        review = image_row[10]
        review_state = ''
        if (review == '0'):
            review_state = 'Not reviewed'
        elif (review == '1'):
            review_state = 'Bad'
        elif (review == '2'):
            review_state = 'Unsure'
        elif (review == '3'):
            review_state = 'Good'
        label_time = 0
        label_time_info = image_info_database.view_label_time_by_id(image_id)
        for l_row in label_time_info:
            start_time = l_row[2]
            end_time=l_row[3]
            dif = Util.calcu_label_time(start_time, end_time)
            label_time = label_time + dif
        l_time = Util.difToTime(label_time)
        # TODO get name by id
        dataset_name = image_row[7]
        bbox = []
        polygon = []
        classes = []
        bbox_rows = image_info_database.view_label_bbox_by_id(image_id)
        polygon_rows = image_info_database.view_label_polygon_by_id(image_id)
        class_rows = image_info_database.view_label_classification_by_id(image_id)
        for b_row in bbox_rows:
            bbox_info = {}
            bbox_info['x'] = b_row[4]
            bbox_info['y'] = b_row[5]
            bbox_info['height'] = b_row[6]
            bbox_info['width'] = b_row[7]
            bbox_info['name'] = b_row[3]
            bbox_info['color'] = b_row[8]
            bbox_info['shape'] = "Bounding Box"
            bbox_info['label_id'] = b_row[2]
            bbox.append(bbox_info)
        for p_row in polygon_rows:
            polygon_info = {}
            polygon_info['name'] = p_row[3]
            polygon_info['shape'] = "Polygon"
            polygon_info['color'] = p_row[4]
            polygon_info['label_id'] = p_row[2]
            polygon_info['points'] = []
            # polygon_info['coord'] = []
            points_rows = image_info_database.view_polygon_points_by_labelID(p_row[2])
            points = []
            coord = []
            for points_row in points_rows:
                points.append(points_row[3])
                points.append(points_row[4])
                # coord.append([points_row[3], points_row[4]])
            polygon_info['points'] = points
            # polygon_info['coord'] = coord
            polygon.append(polygon_info)
        for c_row in class_rows:
            class_info = {}
            class_info['name'] = c_row[2]
            class_info['result'] = c_row[3]
            classes.append(class_info)
        classification = str(classes)
        label_info = "Bounding Box : " + str(bbox) + " ; Polygon : " + str(polygon)
        data_row = [image_id, image_info, label_info, classification, review_state, l_time, dataset_name]
        with open(path,'a+') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(data_row)
    re = {
        'message': "create export successfully",
        'url' : url,
        'filename' : filename,
        'code' : 0,
    }
    return re
