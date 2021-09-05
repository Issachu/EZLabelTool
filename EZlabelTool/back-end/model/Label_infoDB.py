# -*- coding:utf-8 -*-
# Date: 22 Apr 2021
# Author：Pingyi Hu a1805597
# Description：the database connection process of label information

import sqlite3
import threading
lock = threading.Lock()

class Label_infoDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_label_time (id INTEGER PRIMARY KEY, image_id, start_time, end_time, creator, create_date)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_label_bbox (id INTEGER PRIMARY KEY, image_id, label_id, name, x, y, height, weight, color, creator, create_date)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_label_polygon (id INTEGER PRIMARY KEY, image_id, label_id, name, color, creator, create_date)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_label_polygon_points (id INTEGER PRIMARY KEY, image_id, label_id, x_axis, y_axis)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_label_classification (id INTEGER PRIMARY KEY, image_id, name, classify, creator, create_date)")
        self.conn.commit()


    # handle insert informations
    def insert_label_time(self, image_id, start_time, end_time, creator, create_date):
        self.cur.execute("INSERT INTO t_label_time VALUES (NULL,?,?,?,?,?)",(image_id, start_time, end_time, creator, create_date))
        self.conn.commit()

    def insert_label_bbox(self, image_id, label_id, name, x, y, height, weight, color, creator, create_date):
        self.cur.execute("INSERT INTO t_label_bbox VALUES (NULL,?,?,?,?,?,?,?,?,?,?)",(image_id, label_id, name, x, y, height, weight, color, creator, create_date))
        self.conn.commit()
    
    def insert_label_polygon(self, image_id, label_id, name, color, creator, create_date):
        self.cur.execute("INSERT INTO t_label_polygon VALUES (NULL,?,?,?,?,?,?)",(image_id, label_id, name, color, creator, create_date))
        self.conn.commit()

    def insert_label_polygon_points(self, image_id, label_id, x_axis, y_axis):
        self.cur.execute("INSERT INTO t_label_polygon_points VALUES (NULL,?,?,?,?)",(image_id, label_id, x_axis, y_axis))
        self.conn.commit()

    def insert_label_classification(self, image_id, name, classify,  creator, create_date):
        self.cur.execute("INSERT INTO t_label_classification VALUES (NULL,?,?,?,?,?)",(image_id, name, classify, creator, create_date))
        self.conn.commit()

    # handle searching
    def view_label_time_by_id(self,image_id):
        self.cur.execute("SELECT * FROM t_label_time where image_id=?",(image_id,))
        rows = self.cur.fetchall()
        return rows
    
    def view_label_bbox_by_id(self,image_id):
        self.cur.execute("SELECT * FROM t_label_bbox where image_id=?",(image_id,))
        rows = self.cur.fetchall()
        return rows
    
    def view_label_polygon_by_id(self,image_id):
        self.cur.execute("SELECT * FROM t_label_polygon where image_id=?",(image_id,))
        rows = self.cur.fetchall()
        return rows

    def view_polygon_points_by_labelID(self, label_id):
        self.cur.execute("SELECT * FROM t_label_polygon_points where label_id=?",(label_id,))
        rows = self.cur.fetchall()
        return rows

    def view_label_classification_by_id(self, image_id):
        self.cur.execute("SELECT * FROM t_label_classification where image_id=?",(image_id,))
        rows = self.cur.fetchall()
        return rows

    # handle deleting
    def delete_label_info(self,image_id):
        self.cur.execute("DELETE FROM t_label_bbox where image_id=?",(image_id,))
        self.conn.commit()
        self.cur.execute("DELETE FROM t_label_polygon where image_id=?",(image_id,))
        self.conn.commit()
        self.cur.execute("DELETE FROM t_label_polygon_points where image_id=?",(image_id,))
        self.conn.commit()
        self.cur.execute("DELETE FROM t_label_classification where image_id=?",(image_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
        