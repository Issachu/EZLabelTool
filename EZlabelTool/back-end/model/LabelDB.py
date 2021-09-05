# -*- coding:utf-8 -*-
# Date: 16 Apr 2021
# Author：Pingyi Hu a1805597
# Description：the database connection process of labelling

import sqlite3
import threading
lock = threading.Lock()

class LabelDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS t_label_image (id INTEGER PRIMARY KEY, uuid, filename, alias, url, project_id, dataset_id, dataset_name, status, type, review, editor, edit_date, creator, create_date, last_labeller, last_reviewer, label_time, review_time)")
        self.conn.commit()

    # get all the image by project_id
    def get_all_image(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE project_id=?", (project_id,))
        row = self.cur.fetchall()
        return row

    # if the labells have been labelled
    # 0-unlabelled;  1-labelling; 2: labelled; 3-reviewing; 4-reviewed
    def get_labels_edited(self, dataset_id, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status in ('2','3','4') and dataset_id=? and project_id=?", (dataset_id,project_id,))
        row = self.cur.fetchall()
        return row

    # get list in different tab (project view)
    # 0-unlabelled;  1-labelling; 2: labelled; 3-reviewing; 4-reviewed
    def get_labels_in_queue(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status in ('0','1') and project_id=? order by dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row
    
    def get_labels_in_labelled(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status in ('2','3') and project_id=? order by dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row

    def get_labels_in_reviewed(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status='4' and project_id=? order by dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row

    # get list in different tab by search (project view)
    # 0-unlabelled;  1-labelling; 2: labelled; 3-reviewing; 4-reviewed
    def get_labels_in_queue_search(self, project_id,uuid,dataset,comment,labeler,reviewer):
        
        sel = "SELECT * FROM t_label_image WHERE status in ('0','1') and project_id='%s'" % project_id

        if uuid != "":
            sel += " and uuid = '%s'" % uuid

        if dataset !="":
            sel += " and dataset_name = '%s'" % dataset
        
        if comment !="":
            sel += " and review = '%s'" % comment

        if labeler !="":
            sel += " and last_labeller = '%s'" % labeler

        if reviewer !="":
            sel += " and last_reviewer = '%s'" % reviewer

        sel += " order by dataset_id"

        self.cur.execute(sel)
        row = self.cur.fetchall()
        return row
    
    def get_labels_in_labelled_search(self, project_id,uuid,dataset,comment,labeler,reviewer):
        sel = "SELECT * FROM t_label_image WHERE status in ('2','3') and project_id='%s'" % project_id

        if uuid != "":
            sel += " and uuid = '%s'" % uuid

        if dataset !="":
            sel += " and dataset_name = '%s'" % dataset
        
        if comment !="":
            sel += " and review = '%s'" % comment

        if labeler !="":
            sel += " and last_labeller = '%s'" % labeler

        if reviewer !="":
            sel += " and last_reviewer = '%s'" % reviewer

        sel += " order by dataset_id"

        self.cur.execute(sel)
        row = self.cur.fetchall()
        return row

    def get_labels_in_reviewed_search(self, project_id,uuid,dataset,comment,labeler,reviewer):
        sel = "SELECT * FROM t_label_image WHERE status='4' and project_id= '%s'" % project_id

        if uuid != "":
            sel += " and uuid = '%s'" % uuid

        if dataset !="":
            sel += " and dataset_name = '%s'" % dataset
        
        if comment !="":
            sel += " and review = '%s'" % comment

        if labeler !="":
            sel += " and last_labeller = '%s'" % labeler

        if reviewer !="":
            sel += " and last_reviewer = '%s'" % reviewer

        sel += " order by dataset_id"
        
        self.cur.execute(sel)
        row = self.cur.fetchall()
        return row
    

    # insert: attach to project
    # uuid, filename, alias, url, project_id, dataset_id, dataset_name, status, type, review, editor, edit_date, creator, create_date, last_labeller, last_reviewer
    def insert_label_image(self, uuid, filename, alias, url, project_id, dataset_id, dataset_name, status, type, review, editor, edit_date, creator, create_date, last_labeller, last_reviewer):
        self.cur.execute("INSERT INTO t_label_image VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(uuid, filename, alias, url, project_id, dataset_id, dataset_name, status, type, review, editor, edit_date, creator, create_date, last_labeller, last_reviewer, 0, 0))
        self.conn.commit()
        return self.cur.lastrowid

    # delete: dettach to project
    def delete_labels(self, dataset_id, project_id):
        self.cur.execute("DELETE FROM t_label_image where dataset_id=? and project_id=?",(dataset_id,project_id,))
        self.conn.commit()

    
    # get attached dataset (return dataset_id array)
    def get_attached_dataset(self, project_id):
        self.cur.execute("SELECT dataset_id FROM t_label_image where project_id=? GROUP by dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row


    # handle label choose, skip & submit
    def get_labelled_images(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status in ('2','4') and project_id=? order by label_time, dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row
    
    def get_view_image(self, project_id, image_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status in ('2','4') and project_id=? and id=?", (project_id, image_id,))
        row = self.cur.fetchall()
        return row
        
    def get_images_in_queue(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status='0' and project_id=? order by label_time, dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row

    def set_choose_image(self, image_id, project_id):
        try:
            lock.acquire(True)
            self.cur.execute("UPDATE t_label_image SET status='1' WHERE id=? and project_id=?",(image_id,project_id,))
            self.conn.commit()
        finally:
            lock.release()
    
    def set_skip_image(self, image_id, project_id, creator):
        self.cur.execute("UPDATE t_label_image SET status='2', type='0', last_labeller=? WHERE id=? and project_id=?",(creator,image_id,project_id,))
        self.conn.commit()

    def set_submit_image(self, image_id, project_id, creator):
        self.cur.execute("UPDATE t_label_image SET status='2', type='1', last_labeller=? WHERE id=? and project_id=?",(creator,image_id,project_id,))
        self.conn.commit()

    def set_back_image(self, image_id, project_id, status):
        try:
            lock.acquire(True)
            self.cur.execute("UPDATE t_label_image SET status=? WHERE id=? and project_id=?",(status,image_id,project_id,))
            self.conn.commit()
        finally:
            lock.release()

    
    def reset_label_time(self, project_id):
        self.cur.execute("UPDATE t_label_image SET label_time=0 WHERE project_id=?",(project_id,))
        self.conn.commit()
    
    def set_label_time_plus(self, project_id, image_id):
        self.cur.execute("UPDATE t_label_image SET label_time=label_time+1 WHERE project_id=? and id=?",(project_id,image_id,))
        self.conn.commit()

    # handle review choose & submit
    def get_review_images_in_queue(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status in ('2') and project_id=? order by review_time, dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row
    
    def set_choose_review_image(self, image_id, project_id):
        try:
            lock.acquire(True)
            self.cur.execute("UPDATE t_label_image SET status='3' WHERE id=? and project_id=?",(image_id,project_id,))
            self.conn.commit()
        finally:
            lock.release()

    def get_reviewed_images(self, project_id):
        self.cur.execute("SELECT * FROM t_label_image WHERE status in ('4') and project_id=? order by review_time, dataset_id", (project_id,))
        row = self.cur.fetchall()
        return row
    
    def set_submit_review(self, image_id, project_id, creator, review):
        self.cur.execute("UPDATE t_label_image SET status='4', last_reviewer=?, review=? WHERE id=? and project_id=?",(creator,review,image_id,project_id,))
        self.conn.commit()
    
    def reset_review_time(self, project_id):
        self.cur.execute("UPDATE t_label_image SET review_time=0 WHERE project_id=?",(project_id,))
        self.conn.commit()
    
    def set_review_time_plus(self, project_id, image_id):
        self.cur.execute("UPDATE t_label_image SET review_time=review_time+1 WHERE project_id=? and id=?",(project_id,image_id,))
        self.conn.commit()
    
    

    # handle delete
    def delete_image_byurl(self, url=""):
        self.cur.execute("DELETE FROM t_label_image where url=?",(url,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# test
# database = Database("../EZlabel - py.db")

