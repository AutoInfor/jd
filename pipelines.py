# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl
import os
import datetime
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import socket

#from util import *

class JdPipeline(object):
    def __init__(self):
        self.db = ReviewDB()
        self.productIDlist=self.db.execute('SELECT productID from product_comment')
        print("productIDlist",self.productIDlist)
    def process_item(self, item, spider):
        
        if item['referenceName'] and item['productId'] not in self.productIDlist:
            self.savePrductComment(item['productId'],item['referenceName'][0],item['commentCount'],item['goodRateShow'],'jd',item['generalRateShow'],item['poorRateShow'])           
            
                 
        #firstTime=读库
        # d1 = datetime.datetime.strptime(firstTime, '%Y-%m-%d %H:%M:%S')
        # d2 = datetime.datetime.strptime(item['creationTime'], '%Y-%m-%d %H:%M:%S')
        # delta = d1 - d2
        # if delta>0:
            # pass #入库
        print('item[referenceName]',item['referenceName'])
        if item['referenceId']:
            
            for i in range(1, len(item['referenceId'])):
                self.saveProductCommentData(item['referenceId'][i],item['nickname'][i],item['userLevelName'][i],item['userClientShow'][i],item['content'][i],item['creationTime'][i],item['guid'][i],item['score'][i],item['referenceName'][i])
            
        return item
        
    def savePrductComment(self, productID,productName,commentCount,goodRateShow,PlatForm,generalRateShow,poorRateShow):
        sql='''insert ignore into product_comment(productID,productName,commentCount,goodRateShow,PlatForm,generalRateShow,poorRateShow)
         VALUES("{}","{}","{}","{}","{}","{}","{}") '''.format(productID,productName,commentCount,goodRateShow,PlatForm,generalRateShow,poorRateShow)
        self.db.execute(sql)
    

    def saveProductCommentData(self, productID,user,userLevel,userClient,content,contentCreattime,guid,score,referenceName):

        sql='''insert ignore into product_comment_data(productID,user,userLevel,userClient,content,contentCreattime,guid,score,referenceName)
         VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}") '''.format(productID,user,userLevel,userClient,content,contentCreattime,guid,score,referenceName)
        self.db.execute(sql)

class ReviewDB():

    def __init__(self, host='10.63.229.30', user='ci_db', pwd='zte,123', database='ci', port=3306):
        if socket.gethostbyname(socket.gethostname()) == '10.63.229.30':
            self.host = 'localhost'
            self.user = 'ci'
        else:
            self.host = host
            self.user = user
        self.password = pwd
        self.db = database
        self.port = port
        self.connect()

    def connect(self):
        try:
            self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db,
                                        port=self.port, use_unicode=True, charset="utf8")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def disconnect(self):
        if (None != self.cursor):
            self.cursor.close()
        if (None != self.conn):
            self.conn.close()

    def table_exists(self, table):
        result = self.cursor.execute(
            "SELECT table_name FROM information_schema.TABLES WHERE table_name ='{}'".format(table))
        return result > 0

    def execute(self, sql, need_return=True):
        self.cursor.execute(sql)
        self.conn.commit()
        if need_return:
            if sql[0:6].lower() in ['update', 'delete', 'create']:
                rowcount = self.cursor.rowcount if hasattr(self.cursor, 'rowcount') else -1
                return rowcount
            return self.cursor.fetchall()

    def insert_by_many(self, sql, param):
        try:
            self.cursor.executemany(sql, param)
            self.conn.commit()
        except Exception as e:
            traceback.print_exc()
            self.conn.rollback()
            raise (e)
