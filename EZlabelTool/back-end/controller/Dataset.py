# -*- coding:utf-8 -*-
# Date: 11 Mar 2021
# Author：Yan Zhou a1807782
# Description：the service of dataset

import sqlite3
import json
import uuid
import datetime
import os

import sys
sys.path.append('..')
from  model.DatasetDB import DatasetDB
import controller.Util as Util

database = DatasetDB("../EZlabel.db")

# show the users in the org
def get_dataset_list(json_search, org_id):
    rows=[]
    results=[]

    if json_search:
        search = json.loads(json_search)
        name = search["name"]
        rows = database.search_dataset(org_id,name)
    else:
        rows = database.search_dataset(org_id)
        
    # columns = ["id", "name", "rows", "creator", "create_date"]
    for row in rows:
            result = {}
            result['id'] = row[0]
            result['name'] = row[1]
            result['desc'] = row[2]
            result['rows'] = row[3]
            res = database.get_project_quantity(row[0])
            quantity = len(res)
            result['project'] = quantity
            details=""

            if quantity != 0:
                for re in res:
                    details = details + re[0]+","
                details = details[0:-1]

            result['detail'] = details
            result['creator'] = row[4]
            result['create_date'] = Util.last_modify(row[5])
            result['flag'] = row[6]
            results.append(result)
    
    # return results
    return json.dumps(results)

#(self, name, org_id, creator_id, creator, create_date, editor_id, editor, edit_date)
def add_dataset(json_dataset,org_id,creator):
    try:
        dataset = json.loads(json_dataset)
        name = dataset["name"]
        desc = dataset["desc"]

        ## Duplicate name conditional expressions
        rows = database.search_dataset(org_id,name)
        if len(rows)>0:
            re = {
                'code': -1,
                'message': "Duplicate dataset name."
            }
            return json.dumps(re)  
        
        database.insert_dataset(name,desc,org_id,"",creator,datetime.datetime.now(),"",creator,datetime.datetime.now())
        re = {
            'code': 0,
            'message': "Added sucessfully, please upload the images."
        }
        return json.dumps(re)  
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)     

# physically delete dataset and images in dataset based on the id
def delete_dataset(json_dataset):
    try: 
        dataset = json.loads(json_dataset)
        id = dataset["id"]
        # delete the images on server
        rows = database.search_image_in_dataset(str(id))
            
        # columns = [id, name, alias, url, dataset_id, creator, create_date]
        for row in rows:
            alias = row[2]
            path = './image/' + alias
            os.remove(path)
        
        # delete the image info in database 
        database.delete_images_in_dataset(str(id))
        # delete the dataset
        database.delete_dataset(id)
        re = {
            'code':0,
            'message':'Deleted Successfully',
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

# physically delete image in dataset
def delete_image(json_dataset):
    try: 
        dataset = json.loads(json_dataset)
        alias = dataset["alias"]

        # delete the images on server
        path = './image/' + alias
        os.remove(path)
        
        # delete the image info in database 
        database.delete_image_by_alias(alias)

        re = {
            'code':0,
            'message':'Deleted Successfully',
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

# active dataset based on the id
def active_dataset(json_dataset):
    try: 
        dataset = json.loads(json_dataset)
        id = dataset["id"]
        database.update_dataset_flag(id)
        re = {
            'code':0,
            'message':'Activated successfully, you can attach the dataset to any project for annotating. ',
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

################# image in dataset handle #########################
# insert an image in dataset
def insert_image(url, name, alias, dataset_id, creator):
    try:
        # insert to database: self, name, alias, url, dataset_id, creator, create_date
        database.insert_image_in_dataset(name, alias, url, dataset_id, creator, datetime.datetime.now())
        re = {
            'ok': 'true',
            'message' : "Uploaded successfully",
            'filename': name,
            'alias': alias,
            'url': url
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

# return the images list in the dataset
def get_image_list(json_search):
    search = json.loads(json_search)
    dataset_id = search["dataset_id"]
    rows=[]
    results=[]
    rows = database.search_image_in_dataset(dataset_id)
        
    # columns = [id, name, alias, url, dataset_id, creator, create_date]
    for row in rows:
            result = {}
            result['id'] = row[0]
            result['filename'] = row[1]
            result['alias'] = row[2]
            result['url'] = row[3]
            result['creator'] = row[5]
            result['create_date'] = Util.last_modify(row[6])
            results.append(result)
    # return results
    return json.dumps(results)


