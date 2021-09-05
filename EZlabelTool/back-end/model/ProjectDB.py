# -*- coding:utf-8 -*-
# Date: 11 April 2021
# Author：Yan Zhou a1807782
# Description：the database connection process of project

import sqlite3

class ProjectDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS t_project (id INTEGER PRIMARY KEY, name, desc, org_id, status, flag, 
        creator_id, creator, create_date, editor_id, editor, edit_date)""")
        self.conn.commit()

    def insert_project(self, name, desc, org_id, creator_id, creator, create_date, editor_id, editor, edit_date):
        self.cur.execute("INSERT INTO t_project VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)",
            (name, desc, org_id, "0","1", creator_id, creator, create_date, editor_id, editor, edit_date))
        self.conn.commit()
        return self.cur.lastrowid

    def view_project(self,id):
        self.cur.execute("SELECT * FROM t_project where id=?",(id,))
        rows = self.cur.fetchall()
        return rows

    # do not change the sequence of the fields, used in user.py and project.py
    def search_project(self, org_id="", name=""):
        if(name == ""):
            self.cur.execute("SELECT id,name,desc,status,creator,create_date FROM t_project WHERE org_id=? and flag=? ORDER BY create_date DESC", (org_id,"1",))
        else:
            self.cur.execute("SELECT id,name,desc,status,creator,create_date FROM t_project WHERE org_id=? and flag=? and name like '%' || ? || '%' ORDER BY create_date DESC", (org_id,"1", name, ))
        rows = self.cur.fetchall()
        return rows
    
    def find_project(self, org_id="", name=""):
        self.cur.execute("SELECT id,name,desc,status,creator,create_date FROM t_project WHERE org_id=? and flag=? and name=? ORDER BY create_date DESC", (org_id,"1", name, ))
        rows = self.cur.fetchall()
        return rows

    def update_project_status(self, id, status):
        self.cur.execute("UPDATE t_project SET status=? WHERE id=?", (status,id,))
        self.conn.commit()

    def update_project_flag(self, id):
        self.cur.execute("UPDATE t_project SET flag=0 WHERE id=?", (id,))
        self.conn.commit()


    