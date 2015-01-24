__author__ = 'xfl'
#-*- coding:utf-8 -*-
import MySQLdb

class CConfig:
    @staticmethod
    def path():
        return "E:/test/"
    @staticmethod
    def getConnect():
        return MySQLdb.connect(host='xflit2048.mysql.rds.aliyuncs.com', user='xflcool',passwd='xflhyr_276852',db='jixiang',port=3306,charset='utf8')
