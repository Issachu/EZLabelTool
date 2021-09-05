# -*- coding:utf-8 -*-
# Date: 13 Apr 2021
# Author：Pingyi Hu a1805597
# Description：the service of editor

import hashlib
import sqlite3
import json
import datetime

import sys
sys.path.append('..')
from model.EditorDB import EditorDB
from model.ProjectDB import ProjectDB

database = EditorDB("../EZlabel.db")
projectDB = ProjectDB("../EZlabel.db")

# show the list of exsiting editors
def editor_list(org_id):
    results = []
    rows = database.view_editor_in_org(org_id)
    for row in rows:
            result = {}
            result['id'] = row[0]
            quantity = len(database.get_project_quantity(str(row[0])))
            result['project'] = quantity
            result['name'] = row[1]
            result['desc'] = row[3]
            results.append(result)
    return json.dumps(results)

# show objects in an editor
def object_list(editor_id):
    rows = database.view_object(editor_id)
    return rows

# show classes in an editor
def classification_list(editor_id):
    rows = database.view_classification(editor_id)
    return rows

#################### new editor ##########################
# create a new editor
def create_editor(json_editor,org_id,creator):
    try:
        # transfer json to dict
        editor = json.loads(json_editor)
        name = editor["name"]
        description = editor["desc"]

        rows = database.search_editor(name, org_id)
        if len(rows)>0:
            re = {
                'code': -1,
                'message': "This name is used"
            }
            print("adding editor failed")
        else:
            #(self, name, org_id, description, creator, create_date, editor, edit_date)
            database.insert_editor(name,org_id,description,creator,datetime.datetime.now(),creator,datetime.datetime.now())
            
            re = {
                'code': 0,
                'message': "Adding sucessfully",
            }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

# add objects and classifications by combined input
def add_combination(input_json):
    try:
        # json to dict
        conb = json.loads(input_json)
        editor_id = conb['id']
        # editor_copy_id = conb['editor_copy_id']
        objects = conb['objects']
        classifications = conb['classifications']

        database.delete_editor_objects(editor_id)
        database.delete_editor_classifications(editor_id)

        for o_row in objects:
            name = o_row["name"]
            shape = o_row["shape"]
            color = o_row["color"]
            database.insert_object(editor_id, name, shape, color)
            # database.insert_object_copy(editor_copy_id, name, shape, color)
        for c_row in classifications:
            name = c_row["name"]
            c_type = c_row["type"]
            classes = c_row["classes"]
            options = ','.join([str(x) for x in classes])
            database.insert_classification(editor_id, name, c_type, options)
            # database.insert_classification_copy(editor_copy_id, name,c_type, options)
        re = {
            'code' : 0,
            'message' : "add successfully"
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        print(e)
        print("adding failed")
        return json.dumps(re)

# loading objects and classifications for editor
def load_list(editor_id):
    objects = []
    classifications = []
    
    object_rows = object_list(editor_id)
    classification_rows = classification_list(editor_id)
    for o_row in object_rows:
        result = {}
        result["name"] = o_row[2]
        result["shape"] = o_row[3]
        result["color"] = o_row[4]
        objects.append(result)
    for c_row in classification_rows:
        result = {}
        result["name"] = c_row[2]
        result["type"] = c_row[3]
        result["classes"] = c_row[4]
        classifications.append(result)
    results = {
        'objects': objects,
        'classifications': classifications
    }
    return json.dumps(results)

# TODO delete_editor_setting
def delete_editor_setting(editor_id):
    try: 
        editor=json.loads(editor_id)
        # delete the editor
        database.delete_editor_setting(editor_id)

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

#################### choose from existing editors ##########################

def choose_editor(json_editor):
    try:
        # transfer json to dict
        editor = json.loads(json_editor)
        editor_id = str(editor["editor_id"])
        project_id = editor["project_id"]
        object_rows = database.view_object(editor_id)
        classification_rows = database.view_classification(editor_id)
        if (len(object_rows) == 0 and len(classification_rows) == 0):
            re = {
                'code': -1,
                'message': "This template hasn't been set up! Please set up before using it.",
            }
            return json.dumps(re)
        editor_copy_id = str(database.copy_editor(editor_id,project_id))
        database.copy_object(editor_id, editor_copy_id)
        database.copy_classification(editor_id, editor_copy_id)        

        # update the status of the project to processing
        projectDB.update_project_status(project_id,"1")
        re = {
            'code': 0,
            'message': "Select sucessfully",
            'editor_copy_id': editor_copy_id
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        print(e)
        print("adding failed")
        return json.dumps(re)

# loading objects and classifications in editor_copy
def load_list_copy(editor_copy_id):
    editor_copy_id = str(editor_copy_id)
    objects = []
    classifications = []
    
    object_rows = database.view_object_copy(editor_copy_id)
    classification_rows = database.view_classification_copy(editor_copy_id)
    
    for o_row in object_rows:
        result = {}
        result["name"] = o_row[2]
        result["shape"] = o_row[3]
        result["color"] = o_row[4]
        objects.append(result)
    for c_row in classification_rows:
        result = {}
        result["name"] = c_row[2]
        result["type"] = c_row[3]
        result["classes"] = c_row[4]
        classifications.append(result)
    results = {
        'objects': objects,
        'classifications': classifications
    }
    return json.dumps(results)

# loading objects and classifications in editor_copy by project id
def load_list_copy_by_project_id(project_id):
    editor_copy_id = str(database.view_editor_copy_in_project(project_id)[0][0])
    objects = []
    classifications = []
    
    object_rows = database.view_object_copy(editor_copy_id)
    classification_rows = database.view_classification_copy(editor_copy_id)
    if (len(object_rows)!=0 or len(classification_rows)!=0):
        for o_row in object_rows:
            result = {}
            result["name"] = o_row[2]
            result["shape"] = o_row[3]
            result["color"] = o_row[4]
            objects.append(result)
        for c_row in classification_rows:
            result = {}
            result["name"] = c_row[2]
            result["type"] = c_row[3]
            result["classes"] = c_row[4]
            classifications.append(result)
    results = {
        'objects': objects,
        'classifications': classifications
    }
    return json.dumps(results)

# editing objects and classifications in editor_copy
def add_combination_copy(input_json):
    try:
        # json to dict
        conb = json.loads(input_json)
        editor_copy_id = str(conb['id'])
        objects = conb['objects']
        classifications = conb['classifications']
        database.delete_object_copy(editor_copy_id)
        database.delete_classification_copy(editor_copy_id)
        for o_row in objects:
            name = o_row["name"]
            shape = o_row["shape"]
            color = o_row["color"]
            database.insert_object_copy(editor_copy_id, name, shape, color)
            
        for c_row in classifications:
            name = c_row["name"]
            c_type = c_row["type"]
            classes = c_row["classes"]
            options = ','.join([str(x) for x in classes])
            database.insert_classification_copy(editor_copy_id, name, c_type, options)
            
        re = {
            'code' : 0,
            'message' : "Submit successfully"
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        print(e)
        print("adding failed")
        return json.dumps(re)
###########################  TEST with JSON  #################################################

# input_json = {
#     'editor_id':'3',
#     'editor_copy_id':'7',
#     'object':
#     [{
#         "editor_id":"3",
#         "editor_copy_id":"7",
#         "name":"people",
#         "color": "blue",
#         "shape": "1"
#     },
#     {
#         "editor_id":"3",
#         "editor_copy_id":"7",
#         "name":"people",
#         "color": "blue",
#         "shape": "1"
#     }],
#     'classification':
#     [{
#         "editor_id":"3",
#         "editor_copy_id":"7",
#         "name":"people",
#         "type":"List",
#         "classes": "blue, red",
#     }]
# }

# j = json.dumps(input_json)
# objects = input_json['object']
# re = add_combination(j)
# print(re)
# test = json.loads(j)
# for row in test:
#     print(row["key"] == 1)

# editor_json = json.dumps(editor_test)
# object_json_1 = json.dumps(object_test_1)
# object_json_2 = json.dumps(object_test_2)
# classification_json = json.dumps(classification_test)
# create_editor(editor_json)
# add_object(object_json_1)
# add_object(object_json_2)
# add_classification(classification_json)
# re = load_list_copy("6")
# print(re)
# print(editor_list("2"))
# print(object_list("1"))
# print(classification_list("1"))
# t = Util.last_modify("2021-04-02 17:21:01.898526")
# print (t)