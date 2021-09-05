# -*- coding:utf-8 -*-
# Date: 13 Apr 2021
# Author：Pingyi Hu a1805597
# Description：the database connection process of editor

import sqlite3

class EditorDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_editor (id INTEGER PRIMARY KEY, name, org_id, description, creator, create_date, editor, edit_date)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_editor_object (id INTEGER PRIMARY KEY, editor_id, name, shape, color)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_editor_classification (id INTEGER PRIMARY KEY, editor_id, name, type, classes)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_editor_copy (id INTEGER PRIMARY KEY, name, project_id, description, creator, create_date, editor, edit_date, editor_id)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_editor_object_copy (id INTEGER PRIMARY KEY, editor_copy_id, name, shape, color)")
        self.conn.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_editor_classification_copy (id INTEGER PRIMARY KEY, editor_copy_id, name, type, classes)")
        self.conn.commit()

    # editor handle
    def insert_editor(self, name, org_id, description, creator, create_date, editor, edit_date):
        self.cur.execute("INSERT INTO t_editor VALUES (NULL,?,?,?,?,?,?,?)",(name, org_id, description, creator, create_date, editor, edit_date))
        self.conn.commit()

    def view_editor(self):
        self.cur.execute("SELECT * FROM t_editor")
        rows = self.cur.fetchall()
        return rows
    
    def view_editor_id(self, editor_id):
        self.cur.execute("SELECT * FROM t_editor WHERE id=?", (editor_id,))
        row = self.cur.fetchall()
        return row

    def view_editor_in_org(self, org_id=""):
        self.cur.execute("SELECT * FROM t_editor WHERE org_id=?", (org_id,))
        rows = self.cur.fetchall()
        return rows

    def search_editor(self, name, org_id):
        self.cur.execute("SELECT * FROM t_editor WHERE name=? and org_id=?", (name, org_id,))
        rows = self.cur.fetchall()
        return rows

    #TODO update_editor

    # object handle
    def insert_object(self, editor_id, name, shape, color):
        self.cur.execute("INSERT INTO t_editor_object VALUES (NULL,?,?,?,?)",(editor_id, name, shape, color,))
        self.conn.commit()

    def view_object(self, editor_id=""):
        self.cur.execute("SELECT * FROM t_editor_object where editor_id=?",(editor_id,))
        rows = self.cur.fetchall()
        return rows

    # TODO delete_object

    # classification handle
    def insert_classification(self, editor_id, name, type, classes):
        self.cur.execute("INSERT INTO t_editor_classification VALUES (NULL,?,?,?,?)",(editor_id, name, type, classes,))
        self.conn.commit()

    def view_classification(self, editor_id=""):
        self.cur.execute("SELECT * FROM t_editor_classification where editor_id=?",(editor_id,))
        rows = self.cur.fetchall()
        return rows

    # TODO delete_classification
    # editor_copy handle
    def insert_editor_copy(self, name, project_id, description, creator, create_date, editor, edit_date):
        self.cur.execute("INSERT INTO t_editor_copy VALUES (NULL,?,?,?,?,?,?,?,?)",(name, project_id, description, creator, create_date, editor, edit_date, "",))
        self.conn.commit()

    def copy_editor(self, editor_id, project_id):
        #self.cur.execute("INSERT INTO t_editor_copy (name, project_id, description, creator, create_date, editor, edit_date) SELECT name, org_id, description, creator, create_date, editor, edit_date FROM t_editor where org_id=?",(org_id))
        row = self.view_editor_id(editor_id)
        self.cur.execute("INSERT INTO t_editor_copy VALUES (NULL,?,?,?,?,?,?,?,?)",(row[0][1], project_id, row[0][3], row[0][4], row[0][5], row[0][6], row[0][7],editor_id,))
        self.conn.commit()
        return self.cur.lastrowid

    def view_editor_copy(self):
        self.cur.execute("SELECT * FROM t_editor_copy")
        rows = self.cur.fetchall()
        return rows

    def view_editor_copy_in_project(self, project_id=""):
        self.cur.execute("SELECT * FROM t_editor_copy WHERE project_id=?", (project_id,))
        rows = self.cur.fetchall()
        return rows

    def search_editor_copy(self, name="", project_id=""):
        self.cur.execute("SELECT * FROM t_editor_copy WHERE name=? and project_id=?", (name,project_id,))
        rows = self.cur.fetchall()
        return rows

    def get_project_quantity(self, editor_id):
        self.cur.execute("SELECT project_id FROM (SELECT t_editor_copy.project_id, t_editor_copy.editor_id FROM t_editor_copy,t_project WHERE t_editor_copy.project_id = t_project.id and t_project.flag='1') WHERE editor_id =?", (editor_id,))
        rows = self.cur.fetchall()
        return rows 

    #TODO update_editor

    # object_copy handle
    def insert_object_copy(self, editor_copy_id, name, shape, color):
        self.cur.execute("INSERT INTO t_editor_object_copy VALUES (NULL,?,?,?,?)",(editor_copy_id, name, shape, color,))
        self.conn.commit()

    def copy_object(self, editor_id, editor_copy_id):
        rows = self.view_object(editor_id)
        for row in rows:
            self.cur.execute("INSERT INTO t_editor_object_copy VALUES (NULL,?,?,?,?)",(editor_copy_id, row[2], row[3], row[4],))
            self.conn.commit()

    def view_object_copy(self, editor_copy_id=""):
        self.cur.execute("SELECT * FROM t_editor_object_copy where editor_copy_id=?",(editor_copy_id,))
        rows = self.cur.fetchall()
        return rows
    
    def delete_object_copy(self, editor_copy_id=""):
        self.cur.execute("DELETE FROM t_editor_object_copy where editor_copy_id=?",(editor_copy_id,))
        self.conn.commit()

    # classification_copy handle
    def insert_classification_copy(self, editor_copy_id, name, type, classes):
        self.cur.execute("INSERT INTO t_editor_classification_copy VALUES (NULL,?,?,?,?)",(editor_copy_id, name, type, classes,))
        self.conn.commit()

    def copy_classification(self, editor_id, editor_copy_id):
        rows = self.view_classification(editor_id)
        for row in rows:
            self.cur.execute("INSERT INTO t_editor_classification_copy VALUES (NULL,?,?,?,?)",(editor_copy_id, row[2], row[3],row[4],))
            self.conn.commit()

    def view_classification_copy(self, editor_copy_id=""):
        self.cur.execute("SELECT * FROM t_editor_classification_copy where editor_copy_id=?",(editor_copy_id,))
        rows = self.cur.fetchall()
        return rows

    def delete_classification_copy(self, editor_copy_id=""):
        self.cur.execute("DELETE FROM t_editor_classification_copy where editor_copy_id=?",(editor_copy_id,))
        self.conn.commit()
    
    #TODO delete_editor_setting
    def delete_editor_objects(self, editor_id=""):
        self.cur.execute("DELETE FROM t_editor_object where editor_id=?",(editor_id,))
        self.conn.commit()   

    def delete_editor_classifications(self, editor_id=""):
        self.cur.execute("DELETE FROM t_editor_classification where editor_id=?",(editor_id,))
        self.conn.commit()   

    def __del__(self):
        self.conn.close()

            
# test
# database = EditorDB("../EZlabel - zy.db")
# database.delete_object_copy("5")
# rows = database.view_classification("1")
# database.copy_classification("1", "2")
# row2 = database.view_classification_copy("2")
# print(row2)
# print(row2)
# print(rowss)
# print(database.view_object_copy("1"))