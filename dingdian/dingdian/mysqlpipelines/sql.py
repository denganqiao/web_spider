#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: James Zhang
@date:   
"""
import pymysql.cursors
import sys
sys.path.append('../..')
from dingdian import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

conn = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cursor = conn.cursor()

conn.set_charset('utf8')

cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

class Sql:

    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        sql = 'INSERT INTO dd_name (`xs_name`,`xs_author`,`category`,`name_id`) VALUES (%(xs_name)s, %(xs_author)s, %(category)s, %(name_id)s)'
        value = {
            'xs_name':xs_name,
            'xs_author':xs_author,
            'category':category,
            'name_id':name_id
        }
        cursor.execute(sql, value)
        conn.commit()


    @classmethod
    def select_name(cls, name_id):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)"
        value = {
            'name_id':name_id
        }
        cursor.execute(sql, value)
        return cursor.fetchall()[0]


    @classmethod
    def insert_dd_chaptername(cls, xs_chaptername, xs_content, id_name, num_id, url):
        sql = 'INSERT INTO dd_chaptername (`xs_chaptername`, `xs_content`, `id_name`, `num_id`, `url`) VALUES (%(xs_chaptername)s, %(xs_content)s, %(id_name)s, %(num_id)s, %(url)s)'
        value = {
            'xs_chaptername':xs_chaptername,
            'xs_content':xs_content,
            'id_name':id_name,
            'num_id':num_id,
            'url':url
        }

        cursor.execute(sql, value)
        conn.commit()

    @classmethod
    def select_chapter(cls, url):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_chaptername WHERE url=%(url)s)"
        value = {
            'url':url
        }
        cursor.execute(sql, value)
        return cursor.fetchall()[0]
