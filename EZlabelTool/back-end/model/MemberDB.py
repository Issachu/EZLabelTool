# -*- coding:utf-8 -*-
# Date: 16 April 2021
# Author：Yan Zhou a1807782
# Description：the database connection process of members (project view)

import sqlite3

class MemberDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_member (id INTEGER PRIMARY KEY, user_uuid, user_name, role, permission, project_id, creator, create_date, editor, edit_date)")
        self.conn.commit()

    def insert_member(self, user_uuid, user_name, role, permission, project_id, creator, create_date, editor, edit_date):
        self.cur.execute("INSERT INTO t_member VALUES (NULL,?,?,?,?,?,?,?,?,?)",( user_uuid, user_name, role, permission, str(project_id), creator, create_date, editor, edit_date))
        self.conn.commit()

    def view_member(self, project_id):
        self.cur.execute("SELECT * FROM t_member where project_id=? ORDER by role*1",(project_id,))
        rows = self.cur.fetchall()
        return rows  

    def get_member(self, project_id, name):
        self.cur.execute("SELECT * FROM t_member where project_id=? and user_name=?",(project_id,name,))
        rows = self.cur.fetchall()
        return rows  

    def update_member(self, id, role, permission, editor, edit_date):
        self.cur.execute("UPDATE t_member SET role=?, permission=?, editor=?, edit_date=? WHERE id=?", (role, permission, editor, edit_date, id,))
        self.conn.commit()
    
    # delete the memeber from table if the user is invalid
    def delete_member(self, uuid):
        self.cur.execute("DELETE FROM t_member where user_uuid=?", (uuid,))
        self.conn.commit()

    def get_project_quantity(self, uuid):
        self.cur.execute("SELECT name FROM (SELECT  t_member.user_uuid, t_member.role,t_member.project_id,t_project.flag,t_project.name from t_member,t_project where t_member.project_id=t_project.id) where flag='1' and role in ('0','1','2','3') and user_uuid=? group by project_id", (uuid,))
        rows = self.cur.fetchall()
        return rows 

    def __del__(self):
        self.conn.close()
