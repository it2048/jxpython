__author__ = 'xfl'
#-*- coding:utf-8 -*-
import requests
import MySQLdb
import time
from CConfig import CConfig

class CCommon:
    def getHtml(self,url):
        response = requests.get(url)
        return response.content

    def exeSql(self,sql):
        try:
            tim = time.strftime('%Y%m%d',time.localtime(time.time()))
            conn = CConfig.getConnect()
            cur = conn.cursor()
            cur.execute('SET NAMES utf8')
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print "%s :Mysql Error %d: %s \n" % (tim,e.args[0], e.args[1])

    def querySql(self,sql):
        try:
            tim = time.strftime('%Y%m%d',time.localtime(time.time()))
            conn = CConfig.getConnect()
            cur = conn.cursor()
            cur.execute('SET NAMES utf8')
            cur.execute(sql)
            rows =cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except MySQLdb.Error,e:
            print "%s :Mysql Error %d: %s \n" % (tim,e.args[0], e.args[1])

    def downloadImageFile(self,imgUrl,path):
        local_filename = str(time.strftime('%H%M%S',time.localtime(time.time())))+imgUrl.split('/')[-1]
        r = requests.get(imgUrl, stream=True) # here we need to set stream = True parameter
        with open(path+local_filename,'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        return local_filename