# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 23:38
# @Author  : hxq
# @Software: PyCharm
# @File    : db.py


from hxq.libs.db import DBHelper

__all__ = [
    "DBHelper",
]

if __name__ == '__main__':
    CONFIG = {
        'SQL_CREATOR': 'sqlite3',
        'SQL_DATABASE': r'blog.sqlite3'
    }
    db = DBHelper(config=CONFIG)
    # print(db.all("SHOW DATABASES;"))
    # print(db.first("select * from posts"))
    create_table = '''
    CREATE TABLE hxq(
       ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL
    );
'''
    create_table1 = '''
        CREATE TABLE hxq(
           ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL
        );
    '''
    # print(db.execute(create_table))
    # print(db.execute(create_table1))
