# -*- coding:utf-8 -*-
# Date: 16 Apr 2021
# Author：Pingyi Hu a1805597
# Description：the database connection process of output task

import sqlite3

class TaskDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS t_export (id INTEGER PRIMARY KEY, project_id, file_url, file_name, creator, create_time)""")
        self.conn.commit()

    def insert_export(self, project_id, file_url, file_name, creator, create_time):
        self.cur.execute("INSERT INTO t_export VALUES (NULL,?,?,?,?,?)",(project_id, file_url, file_name, creator, create_time,))
        self.conn.commit()

    def view_export(self,project_id):
        self.cur.execute("SELECT * FROM t_dataset where org_id=?",(project_id,))
        rows = self.cur.fetchall()
        return rows

    