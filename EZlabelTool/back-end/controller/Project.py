# -*- coding:utf-8 -*-
# Date: 11 April 2021
# Author：Yan Zhou a1807782
# Description：the service of project

import sqlite3
import json
import uuid
import datetime

import sys
sys.path.append('..')
from model.ProjectDB import ProjectDB
from model.MemberDB import MemberDB
from model.UserDB import UserDB
from model.DatasetDB import DatasetDB
from model.LabelDB import LabelDB
from model.EditorDB import EditorDB
from model.Label_infoDB import Label_infoDB

import controller.Util as Util

database = ProjectDB("../EZlabel.db")
memberDB = MemberDB("../EZlabel.db")
userDB = UserDB("../EZlabel.db")
datasetDB = DatasetDB("../EZlabel.db")
labelDB = LabelDB("../EZlabel.db")
editorDB = EditorDB("../EZlabel.db")
label_infoDB = Label_infoDB("../EZlabel.db")

# show the users in the org
def get_project_list(json_search, org_id):
    rows=[]
    results=[]

    if json_search:
        search = json.loads(json_search)
        name = search["name"]
        rows = database.search_project(org_id,name)
    else:
        rows = database.search_project(org_id)

    #columns = ["id", "name", "desc", "status", "creator", "create_date"]
    for row in rows:
            result = {}
            result['id'] = row[0]
            result['name'] = row[1]
            result['desc'] = row[2]
            rows = labelDB.get_labelled_images(str(row[0]))
            label_quantity =  len(rows)
            result['labells'] = label_quantity

            allrows = labelDB.get_all_image(str(row[0]))
            all_quantity =  len(allrows)

            # check if there are some labelled images
            if label_quantity!=all_quantity:
                if (row[3] != '0'):
                    database.update_project_status(row[0],'1')
                    result['status'] = '1'
                else:
                    result['status'] = row[3]
            else:    
                # set status to completed if all the labels were labelled
                if (row[3] == '1'):
                    database.update_project_status(row[0],'2')
                    result['status'] = '2'
                else:
                    result['status'] = row[3]
            result['creator'] = row[4]
            result['create_date'] = Util.last_modify(row[5])
            results.append(result)
    
    # return results
    return json.dumps(results)


#(self, name, desc, org_id, creator_id, creator, create_date, editor_id, editor, edit_date):
def add_project(json_project,org_id,creator):
    try:
        project = json.loads(json_project)
        
        name = project["name"]
        desc = project["desc"]

        ## Duplicate name conditional expressions
        rows = database.find_project(org_id,name)
        if len(rows)>0:
            re = {
                'code': -1,
                'message': "Duplicate project name."
            }
            return json.dumps(re)  

        
        project_id = database.insert_project(name,desc,org_id,"",creator,datetime.datetime.now(),"",creator,datetime.datetime.now())

        ## copy the valid user into the project (members in project) ##
        # get the project id

        # get all the valide users in this orgnization
        users = userDB.search_user(org_id,"")
        for user in users:
            # user_uuid, user_name, role, permission, project_id, creator, create_date, editor, edit_date
            uid = user[1]
            username = user[2]
            org_role = user[3]

            # set role and permission as default
            role = "4"
            permission = ""

            # the person who create the project would be the owner(role=3) and has permission"1,2,3"
            if username == creator:
                role = "3"
                permission = "0,1,2,"
            
            # the person who is the admin of this org should be admin(role=0) and has permission"1,2,3"
            # if this person is also the owner, set the role to admin
            if org_role == "0":
                role = "0"
                permission = "0,1,2,"

            memberDB.insert_member(uid,username,role,permission,project_id,"System",datetime.datetime.now(),"System",datetime.datetime.now()) 


        re = {
            'code': 0,
            'id':project_id,
            'name': name,
            'message': "Added sucessfully, please setup the project."
        }
        return json.dumps(re)  
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)     

# delete project based on the id
# pysically delete all the related data

def delete_project(json_project):
    try: 
        project = json.loads(json_project)
        id = project["id"]
        database.update_project_flag(id)
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

# get project setting data: members, datasets and editor
def get_setting(json_project,org_id,cur_user):
    try: 
        project = json.loads(json_project)
        project_id = project["id"]

        ## 0. prepre the objects to store the data
        members = []
        datasets = []
        editor = {}

        ## 1. get the member data
        # id,user_uuid, user_name, role, permission, project_id, creator, create_date, editor, edit_date)
        rows = memberDB.view_member(project_id)
        for row in rows:
            member = {}
            member['id'] = row[0]
            member['uuid'] = row[1]
            member['name'] = row[2]
            member['role'] = row[3]
            member['permission'] = row[4]
            members.append(member)

        ## 2. get the dataset data
        #id,name,desc,rows,creator,create_date
        allDatasets = datasetDB.search_active_dataset(org_id)
        attachedDatasets = labelDB.get_attached_dataset(project_id)
        for x in allDatasets:
            dataset={}
            dataset['id'] = x[0]
            dataset['name'] = x[1]
            dataset['desc'] = x[2]
            dataset['rows'] = x[3]
            dataset['creator'] = x[4]
            dataset['create_date'] = Util.last_modify(x[5])
            dataset['isAttached'] = "0"
            dataset['projectID'] = project_id
            for y in attachedDatasets:
                if x[0] == y[0]:
                    dataset['isAttached'] = "1"
            datasets.append(dataset)

        ## 3. get the editor data
        rows = editorDB.view_editor_copy_in_project(project_id)
        if len(rows) > 0:
            editor = {
                "id": rows[0][0]
            }

        ## 4. get the current user:member
        rows = memberDB.get_member(project_id,cur_user)
        member = {}
        if (len(rows)>0):
            row = rows[0]
            member['id'] = row[0]
            member['uuid'] = row[1]
            member['name'] = row[2]
            member['role'] = row[3]
            member['permission'] = row[4]

        ## 5. combine the data
        detail = {"members":members, "datasets":datasets, "editor":editor, "member":member}
        return json.dumps(detail)
        
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

# get project details: labells, queues(unlabelled images)
def get_details(json_project,cur_user):
    try: 
        project = json.loads(json_project)
        id = project["id"]
        rows = database.view_project(id)
        #1.get the project detail
        project = {}
        if len(rows)>0:
            result = rows[0]
            project['id'] = result[0]
            project['name'] = result[1]
            project['desc'] = result[2]
            project['org_id'] = result[3]
            project['status'] = result[4]

        #2. get the labels in different list by status
        # id , uuid, filename, alias, url, project_id, dataset_id, status, type, review, editor, edit_date, creator, create_date, last_labeller, last_reviewer
        # 0-unlabelled;  1-labelling; 2: labelled; 3-reviewing; 4-reviewed
        queued_rows = labelDB.get_labels_in_queue(id)
        queues = []
        for row in queued_rows:
            result = {}
            result['id'] = row[0]
            result['uuid'] = row[1]
            result['filename'] = row[2]
            result['alias'] = row[3]
            result['url'] = row[4]
            result['project_id'] = row[5]
            result['dataset_id'] = row[6]
            result['dataset_name'] = row[7]
            result['status'] = row[8]
            result['type'] = row[9]
            result['review'] = row[10]
            result['editor'] = row[11]
            result['edit_date'] = Util.last_modify(row[12])
            result['creator'] = row[13]
            result['create_date'] = Util.last_modify(row[14])
            result['last_labeller'] = row[15]
            result['last_reviewer'] = row[16]
            result['label_time'] = "unknown"
            queues.append(result)

        labelled_rows = labelDB.get_labels_in_labelled(id)
        labells = []
        for row in labelled_rows:
            result = {}
            result['id'] = row[0]
            result['uuid'] = row[1]
            result['filename'] = row[2]
            result['alias'] = row[3]
            result['url'] = row[4]
            result['project_id'] = row[5]
            result['dataset_id'] = row[6]
            result['dataset_name'] = row[7]
            result['status'] = row[8]
            result['type'] = row[9]
            result['review'] = row[10]
            result['editor'] = row[11]
            result['edit_date'] = Util.last_modify(row[12])
            result['creator'] = row[13]
            result['create_date'] = Util.last_modify(row[14])
            result['last_labeller'] = row[15]
            result['last_reviewer'] = row[16]
            label_time_rows = label_infoDB.view_label_time_by_id(result['id'])
            label_time = 0
            label_time_detail = []
            for l_row in label_time_rows:
                label_time_info = {}
                label_time_info['editor'] = l_row[4]
                label_time_info['id'] = l_row[0]
                start_time = l_row[2]
                end_time=l_row[3]
                dif = Util.calcu_label_time(start_time, end_time)
                label_time = label_time + dif
                label_time_info['label_time'] = Util.difToTime(dif)
                label_time_info['edit_date'] = Util.last_modify(l_row[5])
                label_time_detail.append(label_time_info)
            result['label_time_info'] = label_time_detail
            result['label_time'] = Util.difToTime(label_time)
            labells.append(result)
        
        reviewed_rows = labelDB.get_labels_in_reviewed(id)
        reviews = []
        for row in reviewed_rows:
            result = {}
            result['id'] = row[0]
            result['uuid'] = row[1]
            result['filename'] = row[2]
            result['alias'] = row[3]
            result['url'] = row[4]
            result['project_id'] = row[5]
            result['dataset_id'] = row[6]
            result['dataset_name'] = row[7]
            result['status'] = row[8]
            result['type'] = row[9]
            result['review'] = row[10]
            result['editor'] = row[11]
            result['edit_date'] = Util.last_modify(row[12])
            result['creator'] = row[13]
            result['create_date'] = Util.last_modify(row[14])
            result['last_labeller'] = row[15]
            result['last_reviewer'] = row[16]
            label_time_rows = label_infoDB.view_label_time_by_id(result['id'])
            label_time = 0
            label_time_detail = []
            for l_row in label_time_rows:
                label_time_info = {}
                label_time_info['editor'] = l_row[4]
                label_time_info['id'] = l_row[0]
                start_time = l_row[2]
                end_time=l_row[3]
                dif = Util.calcu_label_time(start_time, end_time)
                label_time = label_time + dif
                label_time_info['label_time'] = Util.difToTime(dif)
                label_time_info['edit_date'] = Util.last_modify(l_row[5])
                label_time_detail.append(label_time_info)
            result['label_time_info'] = label_time_detail
            result['label_time'] = Util.difToTime(label_time)
            reviews.append(result)

        #3. add the statistics into project detail
        project['totalLabels'] = len(labells) + len(queues) + len(reviews)
        project['labelledLabels'] = len(labells) + len(reviews)
        project['reviewedLabels'] = len(reviews)

        #4. get the current member
        rows = memberDB.get_member(id,cur_user)
        member = {}
        if (len(rows)>0):
            row = rows[0]
            member['id'] = row[0]
            member['uuid'] = row[1]
            member['name'] = row[2]
            member['role'] = row[3]
            member['permission'] = row[4]

        #5.combine the result and return
        detail = {"project":project, "reviews":reviews, "labells":labells, "queues":queues, "member":member}
        return json.dumps(detail)
        
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        print(e)
        return json.dumps(re)

# get project details: labells, queues(unlabelled images)
def get_details_search(json_project,cur_user):
    try: 
        project = json.loads(json_project)
        id = project["id"]
        
        # search params
        uuid = project["uuid"]
        dataset = project["dataset"]
        comment = project["comment"]
        labeler = project["labeler"]
        reviewer = project["reviewer"]

        rows = database.view_project(id)
        #1.get the project detail
        project = {}
        if len(rows)>0:
            result = rows[0]
            project['id'] = result[0]
            project['name'] = result[1]
            project['desc'] = result[2]
            project['org_id'] = result[3]
            project['status'] = result[4]

        #2. get the labels in different list by status
        # id , uuid, filename, alias, url, project_id, dataset_id, status, type, review, editor, edit_date, creator, create_date, last_labeller, last_reviewer
        # 0-unlabelled;  1-labelling; 2: labelled; 3-reviewing; 4-reviewed
        queued_rows = labelDB.get_labels_in_queue_search(id,uuid,dataset,comment,labeler,reviewer)
        queues = []
        for row in queued_rows:
            result = {}
            result['id'] = row[0]
            result['uuid'] = row[1]
            result['filename'] = row[2]
            result['alias'] = row[3]
            result['url'] = row[4]
            result['project_id'] = row[5]
            result['dataset_id'] = row[6]
            result['dataset_name'] = row[7]
            result['status'] = row[8]
            result['type'] = row[9]
            result['review'] = row[10]
            result['editor'] = row[11]
            result['edit_date'] = Util.last_modify(row[12])
            result['creator'] = row[13]
            result['create_date'] = Util.last_modify(row[14])
            result['last_labeller'] = row[15]
            result['last_reviewer'] = row[16]
            result['label_time'] = "unknown"
            queues.append(result)

        labelled_rows = labelDB.get_labels_in_labelled_search(id,uuid,dataset,comment,labeler,reviewer)
        labells = []
        for row in labelled_rows:
            result = {}
            result['id'] = row[0]
            result['uuid'] = row[1]
            result['filename'] = row[2]
            result['alias'] = row[3]
            result['url'] = row[4]
            result['project_id'] = row[5]
            result['dataset_id'] = row[6]
            result['dataset_name'] = row[7]
            result['status'] = row[8]
            result['type'] = row[9]
            result['review'] = row[10]
            result['editor'] = row[11]
            result['edit_date'] = Util.last_modify(row[12])
            result['creator'] = row[13]
            result['create_date'] = Util.last_modify(row[14])
            result['last_labeller'] = row[15]
            result['last_reviewer'] = row[16]
            label_time_rows = label_infoDB.view_label_time_by_id(result['id'])
            label_time = 0
            label_time_detail = []
            for l_row in label_time_rows:
                label_time_info = {}
                label_time_info['editor'] = l_row[4]
                label_time_info['id'] = l_row[0]
                start_time = l_row[2]
                end_time=l_row[3]
                dif = Util.calcu_label_time(start_time, end_time)
                label_time = label_time + dif
                label_time_info['label_time'] = Util.difToTime(dif)
                label_time_info['edit_date'] = Util.last_modify(l_row[5])
                label_time_detail.append(label_time_info)
            result['label_time_info'] = label_time_detail
            result['label_time'] = Util.difToTime(label_time)
            labells.append(result)
        
        reviewed_rows = labelDB.get_labels_in_reviewed_search(id,uuid,dataset,comment,labeler,reviewer)
        reviews = []
        for row in reviewed_rows:
            result = {}
            result['id'] = row[0]
            result['uuid'] = row[1]
            result['filename'] = row[2]
            result['alias'] = row[3]
            result['url'] = row[4]
            result['project_id'] = row[5]
            result['dataset_id'] = row[6]
            result['dataset_name'] = row[7]
            result['status'] = row[8]
            result['type'] = row[9]
            result['review'] = row[10]
            result['editor'] = row[11]
            result['edit_date'] = Util.last_modify(row[12])
            result['creator'] = row[13]
            result['create_date'] = Util.last_modify(row[14])
            result['last_labeller'] = row[15]
            result['last_reviewer'] = row[16]
            label_time_rows = label_infoDB.view_label_time_by_id(result['id'])
            label_time = 0
            label_time_detail = []
            for l_row in label_time_rows:
                label_time_info = {}
                label_time_info['editor'] = l_row[4]
                label_time_info['id'] = l_row[0]
                start_time = l_row[2]
                end_time=l_row[3]
                dif = Util.calcu_label_time(start_time, end_time)
                label_time = label_time + dif
                label_time_info['label_time'] = Util.difToTime(dif)
                label_time_info['edit_date'] = Util.last_modify(l_row[5])
                label_time_detail.append(label_time_info)
            result['label_time_info'] = label_time_detail
            result['label_time'] = Util.difToTime(label_time)
            reviews.append(result)

        #3. add the statistics into project detail
        project['totalLabels'] = len(labells) + len(queues) + len(reviews)
        project['labelledLabels'] = len(labells) + len(reviews)
        project['reviewedLabels'] = len(reviews)

        #4. get the current member
        rows = memberDB.get_member(id,cur_user)
        member = {}
        if (len(rows)>0):
            row = rows[0]
            member['id'] = row[0]
            member['uuid'] = row[1]
            member['name'] = row[2]
            member['role'] = row[3]
            member['permission'] = row[4]

        #5.combine the result and return
        detail = {"project":project, "reviews":reviews, "labells":labells, "queues":queues, "member":member}
        return json.dumps(detail)
        
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        print(e)
        return json.dumps(re)


# attach or dettach dataset
def attach_or_dettach_dataset(json_dataset, creator):
    try: 
        dataset = json.loads(json_dataset)
        dataset_id = dataset['id']
        dataset_name = dataset['name']
        isAttached = dataset['isAttached']
        project_id = dataset['projectID']

        # **need to attach the dataset when the dataset is not attached
        if isAttached == "0":
            # 1. get all the image in the dataset
            # id, name, alias, url, dataset_id, creator, create_date
            rows = datasetDB.search_image_in_dataset(str(dataset_id))
            # 2. copy these images into the t_label_image
            for row in rows:
                # uuid, filename, alias, url, project_id, dataset_id, dataset_name, status, type, review, editor, edit_date, creator, create_date, last_labeller, last_reviewer
                uid = uuid.uuid1().hex
                labelDB.insert_label_image(uid,row[1],row[2],row[3],project_id,dataset_id,dataset_name,"0","","0",creator,datetime.datetime.now(),creator,datetime.datetime.now(),"","")

            re = {
                'code':0,
                'message':'Attached successfully.',
            }
            return json.dumps(re)
        # **need to dettach the dataset when the dataset is attached
        else:
            # 1 if there one of the image has been labelled, can not delete, cannot dettach
            rows = labelDB.get_labels_edited(dataset_id,project_id)
            if len(rows) != 0:
                re = {
                    'code':-1,
                    'message':'Cannot detach, the images in this dataset have been labelled.',
                }
                return json.dumps(re)
                        
            # 2 else delete all the label/image in t_label_image, dataset_id = dataset_id and project_id = project_id
            else:
                labelDB.delete_labels(dataset_id, project_id)
                re = {
                    'code':0,
                    'message':'Detached successfully.',
                }
                return json.dumps(re)

    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

def change_user_authority(json_member,editor):
    try: 
        member = json.loads(json_member)
        id = member["id"]
        role = member["role"]
        permission = member["permission"]
        memberDB.update_member(id, role, permission, editor, datetime.datetime.now())
        re = {
            'code':0,
            'message':'Saved sucessfully',
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re) 
