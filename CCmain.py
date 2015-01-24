#-*- coding:utf-8 -*-
from CCommon import CCommon
from CConfig import CConfig
import bs4
import time
import MySQLdb

class CCmain:
    def main(self):
        sql = "INSERT INTO `jx_news` (`addtime` ,`adduser` ,`title`,`content`,`img_url`," \
                      "`type` ,`source`,`status`)VALUES"
        url = 'http://www.kbcmw.com'

        sqlSel = "SELECT title FROM jx_news WHERE type=0 and status=1"
        common = CCommon()
        html = common.getHtml(url)
        rows = common.querySql(sqlSel)
        newLst = []
        for row in rows:
            newLst.append(row[0])
        soup = bs4.BeautifulSoup(html,from_encoding='utf8')
        table = soup.find(attrs={"class" : "pic"})
        for finda in table.findAll('a'):
            if not (finda.get('title') in newLst):
                print "link good!\n"
                hrf = url+finda.get('href')
                arti = common.getHtml(hrf)
                souparti = bs4.BeautifulSoup(arti,from_encoding='utf8')
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
                    if hasattr(tp,"contents")!=False:
                        tp.decompose()
                desc = unicode(desc)
                imgname = common.downloadImageFile(url+finda.find('img').get('src'),CConfig.path())
                sql += '''(%d,"robots","%s","%s","%s",0,"%s",1),''' %(
                    intdate,finda.get('title'),MySQLdb.escape_string(desc),'/public/upload/'+imgname,source)
        return common.exeSql(sql[:-1])

    def main1(self):
        sql = "INSERT INTO `jx_news` (`addtime` ,`adduser` ,`title`,`content`,`img_url`," \
                      "`type` ,`source`,`status`)VALUES"
        UrlList = [
            ['http://www.kbcmw.com/?list-1536.html',u'【党政要闻】',0],
            ['http://www.kbcmw.com/?list-1543.html',u'【舆论监督哨】',0],
            ['http://www.kbcmw.com/?list-1537.html',u'【聚焦甘孜】',0],
            ['http://www.kbcmw.com/?list-1538.html',u'【各县动态】',0],
            ['http://www.kbcmw.com/?list-1539.html',u'【康巴时评】',0],
            ['http://www.kbcmw.com/?list-1543.html',u'【舆论监督哨】',0],
            ['http://www.kbcmw.com/?list-1545.html',u'【政策资讯】',1],
            ['http://www.kbcmw.com/?list-1546.html',u'【交通资讯】',1],
            ['http://www.kbcmw.com/?list-1547.html',u'【旅游资讯】',1],
            ['http://www.kbcmw.com/?list-1559.html',u'【康巴美景】',3],
            ['http://www.kbcmw.com/?list-1560.html',u'【旅游攻略】',3],
            ['http://www.kbcmw.com/?list-1561.html',u'【精品路线】',3],
            ['http://www.kbcmw.com/?list-1562.html',u'【旅游资讯】',3],
            ['http://www.kbcmw.com/?list-1563.html',u'【道听途说】',3],
            ['http://www.kbcmw.com/?list-1554.html',u'【康藏文化】',4],
            ['http://www.kbcmw.com/?list-1555.html',u'【康巴作家群】',4],
            ['http://www.kbcmw.com/?list-1556.html',u'【人文康藏】',4],
            ['http://www.kbcmw.com/?list-1557.html',u'【康巴历史】',4],
            ['http://www.kbcmw.com/?list-1558.html',u'【纪实康巴】',4]
        ]
        urll = 'http://www.kbcmw.com'
        sqlSel = "SELECT title FROM jx_news WHERE type=0 and status=0"
        common = CCommon()
        for url in UrlList:
            html = common.getHtml(url[0])
            newLst = []
            rows = common.querySql(sqlSel)
            for row in rows:
               newLst.append(row[0])
            soup = bs4.BeautifulSoup(html,from_encoding='utf8')
            table = soup.find(attrs={"class" : "list_left_content"})
            i = 0;
            for finda in table.findAll('ul'):
                i = i+1
                if i>10:break
                tmpa = finda.find('a')
                txt = url[1]+tmpa.text[2:]
                if not (txt in newLst):
                    print "{0} {1} link good!\n".format(i,url[1])
                    hrf = tmpa.get('href')
                    try:
                        arti = common.getHtml(hrf)
                    except:
                        continue
                    souparti = bs4.BeautifulSoup(arti,from_encoding='utf8')
                    content = souparti.find(attrs={"class" : "list_left_content"})
                    tm = content.find(attrs={"class" : "show_info"}).text
                    tn = tm.find("\r")
                    tm = tm[3:tn].strip()
                    try:
                        intdate = int(time.mktime(time.strptime(tm[:11],u"%Y年%m月%d日")))
                    except:
                        continue
                    source = tm[tm.find("：")+1:]
                    desc = content.find(attrs={"style" : "text-align:justify"})
                    imgname = ''
                    if hasattr(desc,"contents")==False:
                        desc = content.find(attrs={"id" : "MyContent"})
                        tp = desc.find(attrs={"style" : "text-align:center"})
                        if hasattr(tp,"contents")!=False:
                            try:
                                urlll = urll+tp.find('img').get('src')
                            except:
                                urlll=''
                            if urlll!='':
                                imgname = common.downloadImageFile(urlll,CConfig.path())
                            tp.decompose()
                    desc = unicode(desc)
                    desc = desc.replace("/UploadFiles/", urll+"/UploadFiles/");
                    status = 0
                    if imgname!='':
                        status = 1
                    sql += '''(%d,"robots","%s","%s","%s",%d,"%s",%d),''' %(
                        intdate,txt,MySQLdb.escape_string(desc),'/public/upload/'+imgname,url[2],source,status)
        if i==0:
            return True
        else:
            return common.exeSql(sql[:-1])
