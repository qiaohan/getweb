#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re
import time
import MySQLdb as db

#class article:

class abstractHtml:
    count = 0
    def __init__(self,htmlcode,listid):
        self.__html = htmlcode
        self.__draw_time = time.time()
        self.__class__.count = self.__class__.count + 1
        self.__id = int(self.__draw_time)%10000000 + 10000000*self.__class__.count
        self.__listid = listid
        self.__name = str(self.__id)+'.html'
        self.__articleid = 1
    def getname(self):
        return self.__name
    def getid(self):
        return self.__id
    def save(self,path):
        if path[-1]=='/':
            self.__path = path
        else:
            self.__path = path + '/'
        outfile = open(path+self.__name,'w')
        outfile.write(self.__html)
        outfile.close()
    def insertRecord(self,cursor):
        me = [str(self.__id),'null',str(self.__listid),str(self.__draw_time),self.__path,self.__name,'1']
        sql = "insert into abstractfile value('"+ "','".join(me)  +"')"
        cursor.execute(sql)

def extractAbstractURL(html):
        urls = []
        rprt_pattern = re.compile('<div class="rprt">.*?</p></div></div></div>')
        rprt = rprt_pattern.findall(html)
        for rprt in rprt:
            href_pattern = re.compile('<dd>.*?</dd>')
            href = href_pattern.findall(rprt)
            url = href[0][4:len(href)-6]
            urls.append(url)
        return urls

if __name__=="__main__":
    conn = db.connect(host='localhost',user='root',passwd='TwAxT7s1UjyoMzxnf7gQ',db='ncbi')
    cur = conn.cursor()
    path = '/home/qiaoh/getweb/getncbi/downloadfile/abstracthtml/'
    absupfile = open('updateabs.txt','a')
    for line in open('updatelist.txt'):
        s = line.split()
        thefile = s[0]
        theid = s[1]
        listfile = open(thefile).read()
        for url in extractAbstractURL(listfile):
            abstracthtml = abstractHtml(urllib2.urlopen('http://www.ncbi.nlm.nih.gov/pubmed/'+url).read(),int(theid))
            abstracthtml.save(path)
            abstracthtml.insertRecord(cur)
            absupfile.write(path+abstracthtml.getname()+'\t'+str(abstracthtml.getid())+'\n')
            print abstractHtml.count
    conn.commit()
    absupfile.close()
    cur.close()
    conn.close()
