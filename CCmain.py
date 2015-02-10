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

        sqlSel = "SELECT title FROM jx_news WHERE type=0"
        common = CCommon()
        html = common.getHtml(url)
        rows = common.querySql(sqlSel)
        newLst = []
        for row in rows:
            newLst.append(row[0])
        soup = bs4.BeautifulSoup(html,from_encoding='gb2312')
        table = soup.find(attrs={"class" : "pic"})
        for finda in table.findAll('a'):
            title = MySQLdb.escape_string(finda.get('title'))
            if not (title in newLst):
                print "link good!\n"
                hrf = url+finda.get('href')
                arti = common.getHtml(hrf)
                souparti = bs4.BeautifulSoup(arti,from_encoding='gb2312')
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
                        if hasattr(tp,"contents")!=False:
                            tp.decompose()
                    else:
                        tp.decompose()
                desc = unicode(desc)
                imgname = common.downloadImageFile(url+finda.find('img').get('src'),CConfig.path())
                sql += '''(%d,"robots","%s","%s","%s",0,"%s",1),''' %(
                    intdate,title,MySQLdb.escape_string(desc),'/public/upload/'+imgname,source)
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
        sqlSel = "SELECT title FROM jx_news"
        newLst = []
        common = CCommon()
        rows = common.querySql(sqlSel)
        for row in rows:
           newLst.append(row[0])
        for url in UrlList:
            html = common.getHtml(url[0])
            soup = bs4.BeautifulSoup(html,from_encoding='gb2312')
            table = soup.find(attrs={"class" : "list_left_content"})
            i = 0;
            for finda in table.findAll('ul'):
                i = i+1
                if i>10:break
                tmpa = finda.find('a')
                txt = url[1]+tmpa.text[2:]
                txt = MySQLdb.escape_string(txt)
                if not (txt in newLst):
                    print "{0} {1} link good!\n".format(i,url[1])
                    hrf = tmpa.get('href')
                    try:
                        arti = common.getHtml(hrf)
                    except:
                        continue
                    souparti = bs4.BeautifulSoup(arti,from_encoding='gb2312')
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
                        else:
                            tp = desc.find(attrs={"style" : "text-align: center;"})
                            if hasattr(tp,"contents")!=False:
                                tp.decompose()
                    desc = unicode(desc)
                    desc = desc.replace("/UploadFiles/", urll+"/UploadFiles/");
                    status = 0
                    if imgname!='':
                        status = 1
                        imgname = '/public/upload/'+ imgname
                    if "/public/upload/"==imgname:
                        imgname = ''
                        status = 0
                    sql += '''(%d,"robots","%s","%s","%s",%d,"%s",%d),''' %(
                        intdate,txt,MySQLdb.escape_string(desc),imgname,url[2],source,status)
        if i==0:
            return True
        else:
            return common.exeSql(sql[:-1])

    def dtore(self,intdate,txt,source,imgll1,imgll2):
        sql = "INSERT INTO `jx_news` (`addtime` ,`adduser` ,`title`,`content`,`img_url`," \
              "`type` ,`source`,`status`)VALUES"
        url = 'http://www.kbcmw.com'
        common = CCommon()
        i=0
        idp = 0;
        newLst = []
        for test in imgll1:
            if i==0:
                imgname = common.downloadImageFile(url+test,CConfig.path())
                if imgname!='':
                    imgname = '/public/upload/'+ imgname
                else:
                    break
                if "/public/upload/"==imgname:
                    break
                sql1 =sql + '''(%d,"robots","%s","%s","%s",%d,"%s",%d),''' %(
                        intdate,txt,MySQLdb.escape_string(imgll2[0]),imgname,2,source,0)
                idp = common.exeSql(sql1[:-1])
            else:
                imgname = common.downloadImageFile(url+test,CConfig.path())
                if imgname!='':
                    imgname = '/public/upload/'+ imgname
                else:
                    break
                if "/public/upload/"==imgname:
                    break
                sql2 =sql + '''(%d,"robots","%s","%s","%s",%d,"%s",%d),''' %(
                        intdate,txt,MySQLdb.escape_string(imgll2[i]),imgname,2,source,0)
                newLst.append(str(common.exeSql(sql2[:-1])))
            i = i+1
        if idp<>0:
            lst = ",".join(newLst)
            upade = '''UPDATE `jx_news` SET `child_list` = "%s" WHERE `id` = %d''' %(lst,idp)
            ui = common.exeSql(upade)
            print txt+"nice!"

    def main2(self):
        UrlList = [
            ['http://www.kbcmw.com/?list-1497.html',u'【康巴风光】',0],
            ['http://www.kbcmw.com/?list-1530.html',u'【图片新闻】',0],
            ['http://www.kbcmw.com/?list-1527.html',u'【记忆康巴】',0],
            ['http://www.kbcmw.com/?list-1529.html',u'【摄影世界】',0]
        ]
        sqlSel = "SELECT title FROM jx_news WHERE type=2 and child_list is not null and child_list!=''"
        common = CCommon()
        rows = common.querySql(sqlSel)
        newLst = []
        for row in rows:
            newLst.append(row[0])
        for urll in UrlList:
            html = common.getHtml(urll[0])
            soup = bs4.BeautifulSoup(html,from_encoding='gb2312')
            table = soup.find(attrs={"class" : "listpicmain_content"})
            for finda in table.findAll(attrs={"class" : "listpicsimple"}):
                tmpa = finda.find(attrs={"class" : "listpicsimpletitle"}).find('a')
                title = MySQLdb.escape_string(urll[1]+tmpa.text)
                if not (title in newLst):
                    print "link good!\n"
                    hrf = tmpa.get('href')
                    arti = common.getHtml(hrf)
                    souparti = bs4.BeautifulSoup(arti,from_encoding='gb2312')
                    content = souparti.find(attrs={"class" : "show_title"}).text
                    tn = content.find("时间：")
                    tm = content[tn+3:tn+21].strip()
                    try:
                        intdate = int(time.mktime(time.strptime(tm,u"%Y-%m-%d %H:%M:%S")))
                    except:
                        continue
                    src = content.find("作者：")
                    source = content[src+3:].strip()
                    imgList = souparti.find(attrs={"class" : "picnrbox"}).find('script').text
                    if imgList=="":
                        continue
                    st1 = imgList.find("imgArr=")+8
                    st2 = imgList.find("split")-3
                    imgll1 = imgList[st1:st2].split("|")
                    tmp2 = imgList[st2+30:]
                    st3 = tmp2.find("Arr=")+5
                    st4 = tmp2.find("split")-3
                    imgll2 = tmp2[st3:st4].split("|")
                    self.dtore(intdate,title,source,imgll1,imgll2)
        return 1
