# -*- coding:utf-8 -*-
# Date: 4 April 2021
# Author：Yan Zhou a1807782
# Description：the database connection process of user and orgnization

import sqlite3
import threading
lock = threading.Lock()

class UserDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_orgnization (id INTEGER PRIMARY KEY, name UNIQUE, creator, create_date, code UNIQUE, edit_date)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_user (id INTEGER PRIMARY KEY, uuid, name UNIQUE, password, flag, org_id, org_role, creator, create_date, editor, edit_date)")
        self.conn.commit()

    # org handle
    def insert_org(self, name, creator, create_date, code, edit_date):
        self.cur.execute("INSERT INTO t_orgnization VALUES (NULL,?,?,?,?,?)",(name, creator, create_date, code, edit_date))
        self.conn.commit()
        return self.cur.lastrowid

    def view_org(self):
        self.cur.execute("SELECT * FROM t_orgnization")
        rows = self.cur.fetchall()
        return rows

    def search_org(self, name=""):
        self.cur.execute("SELECT * FROM t_orgnization WHERE name=?", (name,))
        rows = self.cur.fetchall()
        return rows
    
    def search_org_by_code(self, code=""):
        self.cur.execute("SELECT * FROM t_orgnization WHERE code=?", (code,))
        rows = self.cur.fetchall()
        return rows

    # user handle
    def insert_user(self, uuid, name, password, flag, org_id, org_role, creator, create_date, editor, edit_date):
        self.cur.execute("INSERT INTO t_user VALUES (NULL,?,?,?,?,?,?,?,?,?,?)",(uuid, name, password, flag, org_id, org_role, creator, create_date, editor, edit_date))
        self.conn.commit()
        return self.cur.lastrowid

    def view_user(self, id):
        self.cur.execute("SELECT id,name,org_id,password FROM t_user where id=?",(id,))
        rows = self.cur.fetchall()
        return rows  

    def search_all_user(self):
        self.cur.execute("SELECT id,name,org_id,password FROM t_user WHERE flag=?", ("1",))
        rows = self.cur.fetchall()
        return rows

    def search_user(self, org_id="", name=""):
        if(name == ""):
            self.cur.execute("SELECT id,uuid,name,org_role,create_date FROM t_user WHERE org_id=? and flag=? ORDER BY create_date DESC", (org_id,"1",))
        else:
            self.cur.execute("SELECT id,uuid,name,org_role,create_date FROM t_user WHERE org_id=? and flag=? and name like '%' || ? || '%' ORDER BY create_date DESC", (org_id,"1", name, ))
  
        rows = self.cur.fetchall()
        return rows
    
    def search_user_login(self,name="", password=""):
        self.cur.execute("SELECT * FROM t_user WHERE name=? and password=? and flag='1'", (name,password))
        rows = self.cur.fetchall()
        return rows

    # logical delete
    def update_user_flag(self, id):
        self.cur.execute("UPDATE t_user SET flag=0 WHERE id=?", (id,))
        self.conn.commit()

    def update_user_password(self, name, password):
        self.cur.execute("UPDATE t_user SET password=? WHERE name=?", (password, name))
        self.conn.commit()  

    def get_current_user(self, name):
        try:
            lock.acquire(True)
            self.cur.execute("SELECT * FROM (SELECT t_user.name name, t_user.password password, t_user.org_role role , t_orgnization.name org_name, t_orgnization.code org_code from t_user, t_orgnization where t_user.org_id = t_orgnization.id) WHERE name = ?", (name,))
            rows = self.cur.fetchall()
            return rows
        finally:
            lock.release()


    def __del__(self):
        self.conn.close()
