# -*- coding:utf-8 -*-
# Date: 13 Apr 2021
# Author：Yan Zhou a1807782
# Description：the database connection process of dataset

import sqlite3
import threading
lock = threading.Lock()

class DatasetDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS t_dataset (id INTEGER PRIMARY KEY, name, desc, org_id, flag, rows,
        creator_id, creator, create_date, editor_id, editor, edit_date)""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS t_dataset_image (id INTEGER PRIMARY KEY, name, alias, url, dataset_id, creator, create_date)""")
        self.conn.commit()

    ######################################### dataset ###################################################
    def insert_dataset(self, name, desc, org_id, creator_id, creator, create_date, editor_id, editor, edit_date):
        self.cur.execute("INSERT INTO t_dataset VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)",
            (name, desc, org_id, "0", "0", creator_id, creator, create_date, editor_id, editor, edit_date))
        self.conn.commit()

    def view_dataset(self,id):
        self.cur.execute("SELECT * FROM t_dataset where id=?",(id,))
        rows = self.cur.fetchall()
        return rows

    def search_dataset(self, org_id="", name=""):
        if(name == ""):
            self.cur.execute("SELECT id,name,desc,rows,creator,create_date,flag FROM t_dataset WHERE org_id=? ORDER BY create_date DESC", (org_id,))
        else:
            self.cur.execute("SELECT id,name,desc,rows,creator,create_date,flag FROM t_dataset WHERE org_id=? and name like '%' || ? || '%' ORDER BY create_date DESC", (org_id, name, ))
        rows = self.cur.fetchall()
        return rows
    
    def search_active_dataset(self, org_id=""):
        self.cur.execute("SELECT id,name,desc,rows,creator,create_date FROM t_dataset WHERE org_id=? and flag=? ORDER BY create_date DESC", (org_id,"1",))
        rows = self.cur.fetchall()
        return rows

    def update_dataset_flag(self, id):
        self.cur.execute("UPDATE t_dataset SET flag=? WHERE id=?", ("1", id,))
        self.conn.commit()

    def update_dataset_rows(self, rows,id):
        self.cur.execute("UPDATE t_dataset SET rows=? WHERE id=?", (rows,id,))
        self.conn.commit()

    def get_project_quantity(self, dataset_id):
        self.cur.execute("SELECT name FROM (SELECT * FROM t_label_image,t_project WHERE t_label_image.project_id = t_project.id and t_project.flag='1') WHERE dataset_id = ?  group by project_id", (dataset_id,))
        rows = self.cur.fetchall()
        return rows 
    
    def delete_dataset(self, id):
        self.cur.execute("DELETE FROM t_dataset WHERE id=?",( id,))
        self.conn.commit()

    ######################################### image in dataset ###################################################
  
    def insert_image_in_dataset(self, name, alias, url, dataset_id, creator, create_date):
        try:
            lock.acquire(True)
            self.cur.execute("INSERT INTO t_dataset_image VALUES (NULL,?,?,?,?,?,?)",(name, alias, url, dataset_id, creator, create_date))
            self.conn.commit()
            self.cur.execute("UPDATE t_dataset set rows = (SELECT count(1) from t_dataset_image where dataset_id=?) WHERE id=?",( dataset_id,dataset_id, ))
            self.conn.commit()
        finally:
            lock.release()
    
    def delete_image_in_dataset(self, id):
        try:
            lock.acquire(True)
            self.cur.execute("DELETE FROM t_dataset_image WHERE id=?",( id,))
            self.conn.commit()
        finally:
            lock.release()

    def delete_image_by_alias(self, alias):
        try:
            lock.acquire(True)
            self.cur.execute("SELECT dataset_id from t_dataset_image where alias = ?",( alias,))
            rows = self.cur.fetchall()
            dataset_id = ""
            if len(rows) > 0:
                dataset_id = str(rows[0][0])
            self.cur.execute("DELETE FROM t_dataset_image WHERE alias=?",( alias,))
            self.conn.commit()
            if len(rows) > 0:
                self.cur.execute("UPDATE t_dataset set rows = (SELECT count(1) from t_dataset_image where dataset_id=?) WHERE id=?",( dataset_id,dataset_id, ))
                self.conn.commit()
            
        finally:
            lock.release()

    def delete_images_in_dataset(self, dataset_id):
        self.cur.execute("DELETE FROM t_dataset_image WHERE dataset_id=?",(dataset_id,))
        self.conn.commit()

    def search_image_in_dataset(self, dataset_id=""):
        self.cur.execute("SELECT * FROM t_dataset_image WHERE dataset_id=?", (dataset_id,))
        rows = self.cur.fetchall()
        return rows