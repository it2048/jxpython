#-*- coding:utf-8 -*-
import MySQLdb

class CConfig:
    @staticmethod
    def path():
        return "/opt/httpd/htdocs/jae_keyit2048/api/jixiang/server/project/public/upload/"
    @staticmethod
    def getConnect():
        return MySQLdb.connect(host='xflit2048.mysql.rds.aliyuncs.com', user='',passwd='',db='jixiang',port=3306,charset='utf8')
