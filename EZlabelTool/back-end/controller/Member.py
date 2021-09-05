# -*- coding:utf-8 -*-
# Date: 16 April 2021
# Author：Yan Zhou a1807782
# Description：The service of member (different from user module, user is used for orgnizaition view
# member is userd for project view, member is the valid copy of user)
# updating the role and permission can be found here.
# add and delete functions can be founf in User.py module

import sqlite3
import json
import datetime

import sys
sys.path.append('..')
from  model.MemberDB import MemberDB

database = MemberDB("../EZlabel.db")

def change_role_permission(json_member,editor):
    try: 
        member = json.loads(json_member)
        id = member["id"]
        role = member["role"]
        permission = member["permission"]
        database.update_member(id, role, permission, editor, datetime.datetime.now())
        re = {
            'code':0,
            'message':'Saved',
        }
        return json.dumps(re)
    except Exception as e:
        re = {
            'code': -1,
            'message': repr(e)
        }
        print("Failed")
        return json.dumps(re) 
