__author__ = 'xfl'
#-*- coding:utf-8 -*-
from CCommon import CCommon
from CConfig import CConfig
import bs4
import time
import re
import datetime
import sys
import MySQLdb

#置顶文章蜘蛛
def main():
    sql = "INSERT INTO `jx_news` (`addtime` ,`adduser` ,`title`,`content`,`img_url`," \
                  "`type` ,`source`,`status`)VALUES"
    url = 'http://www.kbcmw.com'

    sqlSel = "SELECT * FROM jx_news WHERE type=0"
    common = CCommon()
    html = common.getHtml(url)
    rows = common.querySql(sqlSel)
    newLst = []
    for row in rows:
        newLst.append(row[3])
    soup = bs4.BeautifulSoup(html)
    table = soup.find(attrs={"class" : "pic"})
    for finda in table.findAll('a'):
        if not (finda.get('title') in newLst):
            print "link good!\n"
            hrf = url+finda.get('href')
            arti = common.getHtml(hrf)
            souparti = bs4.BeautifulSoup(arti)
            content = souparti.find(attrs={"class" : "list_left_content"})
            tm = content.find(attrs={"class" : "show_info"}).text
            tn = tm.find("\r")
            tm = tm[3:tn].strip()
            intdate = int(time.mktime(time.strptime(tm[:11],u"%Y年%m月%d日")))
            source = tm[tm.find("：")+1:]
            desc = content.find(attrs={"style" : "text-align:justify"})
            if hasattr(desc,"contents")==False:
                desc = content.find(attrs={"id" : "MyContent"})
                tp = desc.find(attrs={"style" : "text-align:center"})
                if hasattr(tp,"contents")==False:
                    tp = desc.find(attrs={"style" : "text-align: center;"})
                tp.decompose()
            desc = unicode(desc)
            #将封面文件存储
            imgname = common.downloadImageFile(url+finda.find('img').get('src'),CConfig.path())
            sql += '''(%d,"robots","%s","%s","%s",0,"%s",1),''' %(
                intdate,finda.get('title'),MySQLdb.escape_string(desc),'/public/upload/'+imgname,source)
    return common.exeSql(sql[:-1])


reload(sys)
sys.setdefaultencoding('utf8')
print main()