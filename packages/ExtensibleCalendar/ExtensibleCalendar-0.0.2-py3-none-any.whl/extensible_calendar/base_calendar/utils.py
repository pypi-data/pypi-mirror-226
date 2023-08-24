#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2023/8/21 14:07
# file: utils.py
# author: 孙伟亮
# email: 2849068933@qq.com
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sqlite3, os, datetime


def connect(name, dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"文件夹:{dir_path}不存在，已自动创建...")
    sql_path = os.path.join(dir_path, f"{name}.db")
    conn = sqlite3.connect(sql_path)
    # 初始化表
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS`date_state` (
  `date` datetime NOT NULL,
  `state` int DEFAULT NULL,
  PRIMARY KEY (`date`)
)''')
    conn.commit()
    return conn


def add_state(date: datetime.datetime, state, name, dir_path):
    try:
        coon = connect(name, dir_path)
        c = coon.cursor()
        c.execute('''INSERT INTO date_state (date,state) VALUES ("%s","%s")''' % (date, state))
        coon.commit()
        coon.close()
    except Exception as e:
        print(e)


def remove_state(date: datetime.datetime, name, dir_path):
    try:
        coon = connect(name, dir_path)
        c = coon.cursor()
        c.execute('''DELETE from date_state where date="%s";''' % (date))
        coon.commit()
        coon.close()
    except Exception as e:
        print(e)


def select_all(name, dir_path):
    try:
        coon = connect(name, dir_path)
        c = coon.cursor()
        all_workday = c.execute('''SELECT * from date_state where state=1;''')
        all_workday = set([datetime.datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S') for i in all_workday])
        all_un_workday = c.execute('''SELECT * from date_state where state=0;''')
        all_un_workday = set([datetime.datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S') for i in all_un_workday])
        coon.commit()
        coon.close()
        return all_workday, all_un_workday
    except Exception as e:
        print(e)
        return set(), set()
