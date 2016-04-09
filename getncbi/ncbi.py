#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re
import time
import MySQLdb as db

class listHtml:
    count = 0
    def __init__(self,htmlcode,uptime=0,query='NULL'):
        self.__html = htmlcode
        self.__updatetime = uptime
        self.__gettime = time.time()
        self.__query = query.split()
        self.__class__.count = self.__class__.count + 1
        self.__id = 10000*int(self.__updatetime) + self.__class__.count
    def saveHtml(self,path):
        self.__path = path
        self.__name = '_'.join(self.__query)
        outfile = open(path+self.__name+str(count),'w')
        outfile.write(self.__html)
        outfile.close()
    def insertRecord(self,cursor):
        cursor.execute('insert into listfile value()')
    def extractAbstractURL(self):
        urls = []
        rprt_pattern = re.compile('<div class="rprt">.*?</p></div></div></div>')
        self.__rprt = rprt_pattern.findall(self.__html)
        for rprt in self.__rprt:
            href_pattern = re.compile('<dd>.*?</dd>')
            href = href_pattern.findall(rprt)
            url = href[0][4:len(href)-6]
            urls.append(url)
        return urls

#class abstractHtml:

class ncbi_spider:
    uptime = time.time()
    conn = db.connect(host='localhost',user='root',passwd='TwAxT7s1UjyoMzxnf7gQ',db='ncbi')
    cur = conn.cursor()
    def __init__(self,root,query):
        self.__root_url = root
        self.__query = query 
        value = {'term':query}
        data = urllib.urlencode(value)
        self.__request = urllib2.Request(root,data)     
    def run(self,pagenumber):
        response = urllib2.urlopen(self.__request)
        listhtml = listHtml(response.read(),self.__class__.uptime,self.__query)
        path = '/home/qiaoh/getweb/getncbi/downloadfile/'
        listhtml.saveHtml(path)
        for i in range(1,pagenumber):
            listhtml = listHtml(response.read(),self.__class__.uptime,self.__query)

    def html():
        return listhtml

if __name__=="__main__":
    root_url = "http://www.ncbi.nlm.nih.gov/pubmed/"
    #query = "olaparib erlotinib"
    query = "genome"
    #root_url = "http://www.baidu.com"
    spider = ncbi_spider(root_url,query)
    spider.run(5)
    #file = open('/var/www/html/qiaoh/test.html','r')
    #h = file.read()
    #file.close()
    #l = listHtml(h)
    #a = l.extractAbstractURL()
