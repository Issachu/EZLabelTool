# -*- coding:utf-8 -*-
# Date: 04 April 2021
# Author：Yan Zhou a1807782
# Description：The service of user and organization

import controller.Util as Util
from model.ProjectDB import ProjectDB
from model.MemberDB import MemberDB
from model.UserDB import UserDB
import hashlib
import sqlite3
import json
import uuid
import datetime
import random

import sys
sys.path.append('..')


database = UserDB("../EZlabel.db")
memberDB = MemberDB("../EZlabel.db")
projectDB = ProjectDB("../EZlabel.db")

# adapt MD5 to encrypt the password
def toMd5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

# randomly get the code of 6 chars-> generate org code
def randomCode():
    ret = ""
    for i in range(6):
        num = random.randint(0, 9)
        num = chr(random.randint(48,57))
        Letter = chr(random.randint(65, 90))
        s = str(random.choice([num,Letter]))
        ret += s
    return ret

# get_all_user, login usage
def get_all_user():
    rows = []
    results = []

    rows = database.search_all_user()
    # columns = ["id", "username", "org_id", "password"]
    for row in rows:
        result = {}
        result['id'] = row[0]
        result['username'] = row[1]
        result['org_id'] = row[2]
        result['password'] = row[3]
        results.append(result)
    # return results
    return results

# show the users in the org
def get_user_list(json_search, org_id):
    rows = []
    results = []

    if json_search:
        search = json.loads(json_search)
        name = search["name"]
        rows = database.search_user(org_id, name)
    else:
        rows = database.search_user(org_id)

    # columns = ["id", "uuid" "name", "org_role" "create_date"]
    for row in rows:
        result = {}
        result['id'] = row[0]
        result['uuid'] = row[1]
        result['name'] = row[2]
        res = memberDB.get_project_quantity(row[1])
        quantity = len(res)
        result['project'] = quantity
        details=""
        
        if quantity != 0:
            for re in res:
                details = details + re[0]+","
            details = details[0:-1]

        result['detail'] = details
        result['org_role'] = row[3]
        result['create_date'] = Util.last_modify(row[4])
        results.append(result)
    # return results
    return json.dumps(results)

# signup
def signup(json_user):

    # get the uuid
    uid = uuid.uuid1().hex

    # transfer json to dict
    user = json.loads(json_user)
    name = user["name"]
    password = toMd5(user["password"])
    org_code = user["org_code"]
    org_name = user["org_name"]
    org_id = ""    

    # add an orgnization if the user choose to create a new org and return the id of org
    # org_role, 0 admin,1 member
    org_role = "1"
    if org_code == "":
        org_role = "0"
        # insert_org (self, name, creator, create_date, code, edit_date):
        not_unique = True

        # get the unique code for the org
        while not_unique:
            code = randomCode()
            rows =  database.search_org_by_code(code)
            if(len(rows)==0):
                not_unique = False

            org_id = database.insert_org(org_name, name, datetime.datetime.now(), code, datetime.datetime.now())

        # rows = database.search_org(org_name)
        # if len(rows) > 0:
        #     org_id = rows[0][0]
        #     # set org_role = 0(admin) if this user create the org
        #     org_role = '0'
    else:
        rows = database.search_org_by_code(org_code)
        if len(rows)>0:
            org_id = rows[0][0]
        else:
            raise NameError('Cannot find org code')

    # insert user
    # (self, uuid, name, password, flag, org_id, org_role, creator, create_date, editor, edit_date)
    user_id = database.insert_user(uid, name, password, "1", str(
        org_id), org_role, name, datetime.datetime.now(), name, datetime.datetime.now())

    # insert member for projects
    # default: no role, no permission
    # if this user is the creator of org (org_role="0"), then there is no project now, so we don't need to add this member to the project
    # if this user is the member of org (org_role="1"), then he/she should be added to all the valid projects in this organization, with role:"4" and permission:""
    role = "4"
    permission = ""
    if org_role == "1":
        # add member to all the projects in this orgnization
        projects = projectDB.search_project(str(org_id))
        for project in projects:
            project_id = project[0]
            # user_uuid, user_name, role, permission, project_id, creator, create_date, editor, edit_date
            memberDB.insert_member(uid, name, role, permission, project_id, "System",
                                   datetime.datetime.now(), "System", datetime.datetime.now())

    # get the new added user for adding into users in app.py
    rows = database.view_user(user_id)
    newUser = {}
    if len(rows) > 0:
        result = rows[0]
        newUser['id'] = result[0]
        newUser['username'] = result[1]
        newUser['org_id'] = result[2]
        newUser['password'] = result[3]
    return newUser


# login
def login(json_user):
    try:
        user = json.loads(json_user)
        name = user["name"]
        password = toMd5(user["password"])
        rows = database.search_user_login(name, password)
        if len(rows) > 0:
            re = {
                'code': 0,
                'message': 'Login sucessfully',
            }
            return json.dumps(re)
        else:
            re = {
                'code': -1,
                'message': 'Username or password is incorrect',
            }
            return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

# delete a user (set flag = 0)
def delete_user(json_user):
    try:
        user = json.loads(json_user)
        id = user["id"]
        uuid = user["uuid"]
        database.update_user_flag(id)

        # delete the member from project view
        memberDB.delete_member(uuid)

        re = {
            'code': 0,
            'message': 'Deleted Successfully',
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return json.dumps(re)

# change password (set password to a new one)
def change_password(json_user):
    
    try:
        user = json.loads(json_user)
        username = user["name"]
        password = ""
        if ("current_password" in json_user):
            cur_password = toMd5(user["current_password"])
            rows = database.search_user_login(username, cur_password)

            # the current password is wrong
            if len(rows) == 0:
                re = {
                    'code': -1,
                    'message': "The current password is incorrect!",
                }
                return re
            else:
                password = user["new_password"]

                passwordMd5 = toMd5(password)
                database.update_user_password(username, passwordMd5)
                re = {
                    'code': 0,
                    'name': username,
                    'password': passwordMd5,
                    'message': 'Reseted successfully, please login',
                }
                return re
        else:
            password = "666666"

            passwordMd5 = toMd5(password)
            database.update_user_password(username, passwordMd5)
            re = {
                'code': 0,
                'name': username,
                'password': passwordMd5,
                'message': 'Reseted successfully, please login',
            }
        
            return re
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        return re

# get the current user's role and permission, in member table
def get_cur_user(current_user_name):
    rows = database.get_current_user(current_user_name)
    result = {}
    if len(rows)>0:
        result['name'] = rows[0][0]
        result['password'] = rows[0][1]
        result['role'] = rows[0][2]
        result['org_name'] = rows[0][3]
        result['org_code'] = rows[0][4]
    # return results
    return json.dumps(result)
