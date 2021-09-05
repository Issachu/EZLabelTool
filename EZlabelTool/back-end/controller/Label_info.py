# -*- coding:utf-8 -*-
# Date: 20 Apr 2021
# Author：Pingyi Hu a1805597
# Description：the service of label_info

import sqlite3
import json
import datetime

import sys
sys.path.append('..')
from model.LabelDB import LabelDB
from model.Label_infoDB import Label_infoDB
from model.ProjectDB import ProjectDB
project_database = ProjectDB("../EZlabel.db")
image_database = LabelDB("../EZlabel.db")
image_info_database = Label_infoDB("../EZlabel.db")

# handle choose image
# code 0 : succeed
# code 1 : no image
# code 2 : finish first label
def choose_image(json_info, current_user):
    info = json.loads(json_info)
    project_id = info["project_id"]
    queued_rows = image_database.get_images_in_queue(project_id)
    fisrtFinished = True
    if len(queued_rows) == 0:
        project_database.update_project_status(project_id, "2")
        labelled_rows = image_database.get_labelled_images(project_id)
        if len(labelled_rows) == 0:
            re = {
                'code' : 1,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
            return re
        for l_row in labelled_rows:
            if (str(l_row[17]) == "0"):
                fisrtFinished = False
        if (fisrtFinished):
            re = {
                'code' : 2,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
            image_database.reset_label_time(project_id)
            return re
        labelled_row = labelled_rows[0]
        result = {}
        result['code'] = 0
        result['id'] = labelled_row[0]
        result['uuid'] = labelled_row[1]
        result['filename'] = labelled_row[2]
        result['alias'] = labelled_row[3]
        result['url'] = labelled_row[4]
        result['project_id'] = labelled_row[5]
        result['dataset_id'] = labelled_row[6]
        result['dataset_name'] = labelled_row[7]
        result['status'] = labelled_row[8]
        result['type'] = labelled_row[9]
        result['review'] = labelled_row[10]
        result['editor'] = labelled_row[11]
        result['edit_date'] = labelled_row[12]
        result['creator'] = labelled_row[13]
        result['create_date'] = labelled_row[14]
        result['last_labeller'] = labelled_row[15]
        result['last_reviewer'] = labelled_row[16]
        result['start_time'] = str(datetime.datetime.now())
        result['message'] = "Please label this image"
        bbox = []
        polygon = []
        classes = []
        bbox_rows = image_info_database.view_label_bbox_by_id(result['id'])
        polygon_rows = image_info_database.view_label_polygon_by_id(result['id'])
        class_rows = image_info_database.view_label_classification_by_id(result['id'])
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
            points = []
            coord = []
            points_rows = image_info_database.view_polygon_points_by_labelID(p_row[2])
            for points_row in points_rows:
                points.append(points_row[3])
                points.append(points_row[4])
                coord.append([points_row[3], points_row[4]])
            polygon_info['points'] = points
            polygon_info['coord'] = coord
            polygon.append(polygon_info)
        for c_row in class_rows:
            classify = {}
            classify['name'] = c_row[2]
            if (c_row[3].startswith('[')):
                c=c_row[3].replace('[','')
                c=c.replace(']','')
                c=c.replace('\'','')
                c=c.replace(' ','')
                c=c.split(',')
                classify['class'] = c
            else:
                classify['class'] = c_row[3]
            classes.append(classify)
        result['bbox'] = bbox
        result['polygon'] = polygon
        result['classes'] = classes
        image_database.set_choose_image(result['id'],project_id)
        return result
    else:
        for q_row in queued_rows:
            if (str(q_row[17]) == "0"):
                fisrtFinished = False
        if (fisrtFinished):
            re = {
                'code' : 2,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
            image_database.reset_label_time(project_id)
            return re
        choose_row = queued_rows[0]
        result = {}
        result['code'] = 0
        result['id'] = choose_row[0]
        result['uuid'] = choose_row[1]
        result['filename'] = choose_row[2]
        result['alias'] = choose_row[3]
        result['url'] = choose_row[4]
        result['project_id'] = choose_row[5]
        result['dataset_id'] = choose_row[6]
        result['dataset_name'] = choose_row[7]
        result['status'] = choose_row[8]
        result['type'] = choose_row[9]
        result['review'] = choose_row[10]
        result['editor'] = choose_row[11]
        result['edit_date'] = choose_row[12]
        result['creator'] = choose_row[13]
        result['create_date'] = choose_row[14]
        result['last_labeller'] = choose_row[15]
        result['last_reviewer'] = choose_row[16]
        result['start_time'] = str(datetime.datetime.now())
        result['message'] = "Please label this image"
        result['bbox'] = []
        result['polygon'] = []
        result['classes'] = []
        image_database.set_choose_image(result['id'],project_id)
        return result
# handle choose view labelled image
def choose_view_image(json_info):
    info = json.loads(json_info)
    project_id = info["project_id"]
    image_id = info["image_id"]
    queued_rows = image_database.get_view_image(project_id, image_id)
    if (len(queued_rows) == 0):
        re = {
                'code' : 1,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
        return re
    else:
        labelled_row = queued_rows[0]
        result = {}
        result['code'] = 0
        result['id'] = labelled_row[0]
        result['uuid'] = labelled_row[1]
        result['filename'] = labelled_row[2]
        result['alias'] = labelled_row[3]
        result['url'] = labelled_row[4]
        result['project_id'] = labelled_row[5]
        result['dataset_id'] = labelled_row[6]
        result['dataset_name'] = labelled_row[7]
        result['status'] = labelled_row[8]
        result['type'] = labelled_row[9]
        result['review'] = labelled_row[10]
        result['editor'] = labelled_row[11]
        result['edit_date'] = labelled_row[12]
        result['creator'] = labelled_row[13]
        result['create_date'] = labelled_row[14]
        result['last_labeller'] = labelled_row[15]
        result['last_reviewer'] = labelled_row[16]
        result['start_time'] = str(datetime.datetime.now())
        result['message'] = "Please label this image"
        bbox = []
        polygon = []
        classes = []
        bbox_rows = image_info_database.view_label_bbox_by_id(result['id'])
        polygon_rows = image_info_database.view_label_polygon_by_id(result['id'])
        class_rows = image_info_database.view_label_classification_by_id(result['id'])
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
            points = []
            coord = []
            points_rows = image_info_database.view_polygon_points_by_labelID(p_row[2])
            for points_row in points_rows:
                points.append(points_row[3])
                points.append(points_row[4])
                coord.append([points_row[3], points_row[4]])
            polygon_info['points'] = points
            polygon_info['coord'] = coord
            polygon.append(polygon_info)
        for c_row in class_rows:
            classify = {}
            classify['name'] = c_row[2]
            if (c_row[3].startswith('[')):
                c=c_row[3].replace('[','')
                c=c.replace(']','')
                c=c.replace('\'','')
                c=c.replace(' ','')
                c=c.split(',')
                classify['class'] = c
            else:
                classify['class'] = c_row[3]
            classes.append(classify)
        result['bbox'] = bbox
        result['polygon'] = polygon
        result['classes'] = classes
        image_database.set_choose_image(result['id'],project_id)
        return result

# handle choose view labelled image
def choose_review_view_image(json_info):
    info = json.loads(json_info)
    project_id = info["project_id"]
    image_id = info["image_id"]
    queued_rows = image_database.get_view_image(project_id, image_id)
    if (len(queued_rows) == 0):
        re = {
                'code' : 1,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
        return re
    else:
        labelled_row = queued_rows[0]
        result = {}
        result['code'] = 0
        result['id'] = labelled_row[0]
        result['uuid'] = labelled_row[1]
        result['filename'] = labelled_row[2]
        result['alias'] = labelled_row[3]
        result['url'] = labelled_row[4]
        result['project_id'] = labelled_row[5]
        result['dataset_id'] = labelled_row[6]
        result['dataset_name'] = labelled_row[7]
        result['status'] = labelled_row[8]
        result['type'] = labelled_row[9]
        result['review'] = labelled_row[10]
        result['editor'] = labelled_row[11]
        result['edit_date'] = labelled_row[12]
        result['creator'] = labelled_row[13]
        result['create_date'] = labelled_row[14]
        result['last_labeller'] = labelled_row[15]
        result['last_reviewer'] = labelled_row[16]
        result['start_time'] = str(datetime.datetime.now())
        result['message'] = "Please label this image"
        bbox = []
        polygon = []
        classes = []
        bbox_rows = image_info_database.view_label_bbox_by_id(result['id'])
        polygon_rows = image_info_database.view_label_polygon_by_id(result['id'])
        class_rows = image_info_database.view_label_classification_by_id(result['id'])
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
            points = []
            coord = []
            points_rows = image_info_database.view_polygon_points_by_labelID(p_row[2])
            for points_row in points_rows:
                points.append(points_row[3])
                points.append(points_row[4])
                coord.append([points_row[3], points_row[4]])
            polygon_info['points'] = points
            polygon_info['coord'] = coord
            polygon.append(polygon_info)
        for c_row in class_rows:
            classify = {}
            classify['name'] = c_row[2]
            if (c_row[3].startswith('[')):
                c=c_row[3].replace('[','')
                c=c.replace(']','')
                c=c.replace('\'','')
                c=c.replace(' ','')
                c=c.split(',')
                classify['class'] = c
            else:
                classify['class'] = c_row[3]
            classes.append(classify)
        result['bbox'] = bbox
        result['polygon'] = polygon
        result['classes'] = classes
        image_database.set_choose_review_image(result['id'],project_id)
        return result

# handle choose review images
def choose_review_image(json_info):
    info = json.loads(json_info)
    project_id = info["project_id"]
    queued_rows = image_database.get_review_images_in_queue(project_id)
    fisrtFinished = True
    if len(queued_rows) == 0:
        labelled_rows = image_database.get_reviewed_images(project_id)
        if len(labelled_rows) == 0:
            re = {
                'code' : 1,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
            return re
        for l_row in labelled_rows:
            if (str(l_row[18]) != "1"):
                fisrtFinished = False
        if (fisrtFinished):
            re = {
                'code' : 2,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
            image_database.reset_review_time(project_id)
            return re
        labelled_row = labelled_rows[0]
        result = {}
        result['code'] = 0
        result['id'] = labelled_row[0]
        result['uuid'] = labelled_row[1]
        result['filename'] = labelled_row[2]
        result['alias'] = labelled_row[3]
        result['url'] = labelled_row[4]
        result['project_id'] = labelled_row[5]
        result['dataset_id'] = labelled_row[6]
        result['dataset_name'] = labelled_row[7]
        result['status'] = labelled_row[8]
        result['type'] = labelled_row[9]
        result['review'] = labelled_row[10]
        result['editor'] = labelled_row[11]
        result['edit_date'] = labelled_row[12]
        result['creator'] = labelled_row[13]
        result['create_date'] = labelled_row[14]
        result['last_labeller'] = labelled_row[15]
        result['last_reviewer'] = labelled_row[16]
        result['label_time'] = "unknown"
        result['message'] = "All the images have been reviewed"
        bbox = []
        polygon = []
        classes = []
        bbox_rows = image_info_database.view_label_bbox_by_id(result['id'])
        polygon_rows = image_info_database.view_label_polygon_by_id(result['id'])
        class_rows = image_info_database.view_label_classification_by_id(result['id'])
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
            points = []
            coord = []
            points_rows = image_info_database.view_polygon_points_by_labelID(p_row[2])
            for points_row in points_rows:
                points.append(points_row[3])
                points.append(points_row[4])
                coord.append([points_row[3], points_row[4]])
            polygon_info['points'] = points
            polygon_info['coord'] = coord
            polygon.append(polygon_info)
        for c_row in class_rows:
            classify = {}
            classify['name'] = c_row[2]
            if (c_row[3].startswith('[')):
                c=c_row[3].replace('[','')
                c=c.replace(']','')
                c=c.replace('\'','')
                c=c.replace(' ','')
                c=c.split(',')
                classify['class'] = c
            else:
                classify['class'] = c_row[3]
            classes.append(classify)
        result['bbox'] = bbox
        result['polygon'] = polygon
        result['classes'] = classes
        image_database.set_choose_review_image(result['id'],project_id)
        return result
    else:
        for q_row in queued_rows:
            if (str(q_row[18]) != "1"):
                fisrtFinished = False
        if (fisrtFinished):
            re = {
                'code' : 2,
                'message' : 'no more image available',
                'id' : "",
                'uuid' : "",
                'filename' : "",
                'alias' : "",
                'url' : "",
                'project_id' : "",
                'dataset_id' : "",
                'dataset_name' : "",
                'status' : "",
                'type' : "",
                'review' : "",
                'editor' : "",
                'edit_date' : "",
                'creator' : "",
                'last_labeller' : "",
                'last_reviewer' : "",
            }
            image_database.reset_review_time(project_id)
            return re
        choose_row = queued_rows[0]
        result = {}
        result['code'] = 0
        result['id'] = choose_row[0]
        result['uuid'] = choose_row[1]
        result['filename'] = choose_row[2]
        result['alias'] = choose_row[3]
        result['url'] = choose_row[4]
        result['project_id'] = choose_row[5]
        result['dataset_id'] = choose_row[6]
        result['dataset_name'] = choose_row[7]
        result['status'] = choose_row[8]
        result['type'] = choose_row[9]
        result['review'] = choose_row[10]
        result['editor'] = choose_row[11]
        result['edit_date'] = choose_row[12]
        result['creator'] = choose_row[13]
        result['create_date'] = choose_row[14]
        result['last_labeller'] = choose_row[15]
        result['last_reviewer'] = choose_row[16]
        result['label_time'] = "unknown"
        result['message'] = "Please review this image"
        bbox = []
        polygon = []
        classes = []
        bbox_rows = image_info_database.view_label_bbox_by_id(result['id'])
        polygon_rows = image_info_database.view_label_polygon_by_id(result['id'])
        class_rows = image_info_database.view_label_classification_by_id(result['id'])
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
            points = []
            coord = []
            points_rows = image_info_database.view_polygon_points_by_labelID(p_row[2])
            for points_row in points_rows:
                points.append(points_row[3])
                points.append(points_row[4])
                coord.append([points_row[3], points_row[4]])
            polygon_info['points'] = points
            polygon_info['coord'] = coord
            polygon.append(polygon_info)
        for c_row in class_rows:
            classify = {}
            classify['name'] = c_row[2]
            if (c_row[3].startswith('[')):
                c=c_row[3].replace('[','')
                c=c.replace(']','')
                c=c.replace('\'','')
                c=c.replace(' ','')
                c=c.split(',')
                classify['class'] = c
            else:
                classify['class'] = c_row[3]
            classes.append(classify)
        result['bbox'] = bbox
        result['polygon'] = polygon
        result['classes'] = classes
        image_database.set_choose_review_image(result['id'],project_id)
        return result

# handle submit
def submit_image(json_image, creator):
    image_info = json.loads(json_image)
    image_id = image_info["image_id"]
    project_id = image_info["project_id"]
    bbox_list = image_info["bbox"]
    polygon_list = image_info["polygons"]
    classes = image_info["classResult"]
    start_time = image_info["start_time"]
    image_info_database.insert_label_time(image_id,start_time,datetime.datetime.now(),creator,datetime.datetime.now())
    image_info_database.delete_label_info(image_id)
    for row in bbox_list:
        name = row['name']
        x = row['x']
        y = row['y']
        height = row['height']
        width = row['width']
        label_id = row['label_id']
        color = row['color']
        image_info_database.insert_label_bbox(image_id, label_id, name, x, y, height, width, color, creator, datetime.datetime.now())
    for poly in polygon_list:
        label_id = poly['label_id']
        name = poly['name']
        color = poly['color']
        image_info_database.insert_label_polygon(image_id, label_id, name, color, creator, datetime.datetime.now())
        points = poly['coord']
        for point in points:
            image_info_database.insert_label_polygon_points(image_id, label_id, point[0], point[1])
    for classify in classes:
        name = classify['name']
        classes = str(classify['class'])
        image_info_database.insert_label_classification(image_id, name, classes, creator, datetime.datetime.now())
    image_database.set_submit_image(image_id, project_id, creator)
    image_database.set_label_time_plus(project_id, image_id)
    re = {
        'code' : 0,
        'message' : 'successfully submit',
        'status' : '2'
    }
    return re

# handle review submit
def submit_review(json_image, creator):
    image_info = json.loads(json_image)
    image_id = image_info["image_id"]
    project_id = image_info["project_id"]
    bbox_list = image_info["bbox"]
    polygon_list = image_info["polygons"]
    classes = image_info["classResult"]
    review = image_info["review"]
    image_info_database.delete_label_info(image_id)
    for row in bbox_list:
        name = row['name']
        x = row['x']
        y = row['y']
        height = row['height']
        width = row['width']
        label_id = row['label_id']
        color = row['color']
        image_info_database.insert_label_bbox(image_id, label_id, name, x, y, height, width, color, creator, datetime.datetime.now())
    for poly in polygon_list:
        label_id = poly['label_id']
        name = poly['name']
        color = poly['color']
        image_info_database.insert_label_polygon(image_id, label_id, name, color, creator, datetime.datetime.now())
        points = poly['coord']
        for point in points:
            image_info_database.insert_label_polygon_points(image_id, label_id, point[0], point[1])
    for classify in classes:
        name = classify['name']
        classes = str(classify['class'])
        image_info_database.insert_label_classification(image_id, name, classes, creator, datetime.datetime.now())
    image_database.set_submit_review(image_id, project_id, creator, review)
    image_database.set_review_time_plus(project_id, image_id)
    re = {
        'code' : 0,
        'message' : 'successfully submit',
        'status' : '4'
    }
    return re

# handle skip
def skip_image(json_image, creator):
    image_info = json.loads(json_image)
    image_id = image_info["image_id"]
    project_id = image_info["project_id"]
    image_database.set_skip_image(image_id, project_id, creator)
    image_database.set_label_time_plus(project_id, image_id)
    re = {
        'code' : 0,
        'message' : 'successfully skip',
        'status' : '2'
    }
    return re

# handle back
def back_image(json_image):
    image_info = json.loads(json_image)
    image_id = image_info["image_id"]
    project_id = image_info["project_id"]
    status = image_info["status"]
    image_database.set_back_image(image_id, project_id, status)
    re = {
        'code' : 0,
        'message' : 'leave without saving',
    }
    return re

# handle next label
def next_label_image(json_image):
    image_info = json.loads(json_image)
    image_id = image_info["image_id"]
    project_id = image_info["project_id"]
    status = image_info["status"]
    image_database.set_back_image(image_id, project_id, status)
    image_database.set_label_time_plus(project_id, image_id)
    re = {
        'code' : 0,
        'message' : 'next image',
    }
    return re

# handle next label
def next_review_image(json_image):
    image_info = json.loads(json_image)
    image_id = image_info["image_id"]
    project_id = image_info["project_id"]
    status = image_info["status"]
    image_database.set_back_image(image_id, project_id, status)
    image_database.set_review_time_plus(project_id, image_id)
    re = {
        'code' : 0,
        'message' : 'next image',
    }
    return re