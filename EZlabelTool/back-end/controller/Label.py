# -*- coding:utf-8 -*-
# Date: 20 Apr 2021
# Author：Pingyi Hu a1805597
# Description：the service of label

import sqlite3
import json
import datetime
import os

import sys
sys.path.append('..')
from model.LabelDB import LabelDB
database = LabelDB("../EZlabel.db")

# choose image
def chooose_image(json_image):
    image_info = json.loads(json_image)
    image_id = image_info("image_id")
    project_id = image_info("project_id")
    re = {
        'code' : 0,
        'message' : 'choose image'
    }
    return json.dumps(re)

# delete image from dataset
def delete_image(image_url):
    database.delete_image_byurl(image_url)

# delete the image from image folder
def delete_image_alias(alias):
    path = './image/' + alias
    print(path)
    os.remove(path)
    re = {
        'code': 0,
        'message': 'successfully delete',
    }
    return json.dumps(re)



###########################  TEST with JSON  #################################################

# imagetest = {
#     "filename":"Tom",
#     "url":"123456",
# }

# imagejson = json.dumps(imagetest)
# # insert_image(imagejson, "3", "2")
# re = get_all("3", "2")
# print(re)