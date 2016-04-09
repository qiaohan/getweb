#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re
import time
import MySQLdb as db

class ncbiQuery:
    count = 0
    def __init__(self,url,queryword,uptime=0):
        self.__base_url = url
        self.__query = queryword
        self.__querylist = queryword.split()
        self.__class__.count = self.__class__.count + 1
        self.__queryid = self.__class__.count*10000000 + int(uptime)%10000000
        self.__update_time = uptime
    def getquerylist(self):
        return self.__querylist
    def getqueryword(self):
        return self.__query
    def getid(self):
        return self.__queryid
    def getrequest(self):
        value = {'term':self.__query}
        data = urllib.urlencode(value)
        request = urllib2.Request(self.__base_url,data)     
        return request
    def insertRecord(self,cursor):
        me = [str(self.__queryid),self.__base_url,self.__query,str(self.__update_time)]
        sql = "insert into querylog value('"+ "','".join(me)  +"')"
        #print sql
        cursor.execute(sql)

class listHtml:
    count = 0
    def __init__(self,htmlcode,query):
        self.__html = htmlcode
        self.__draw_time = time.time()
        self.__queryid = query.getid()
        self.__querywd = query.getqueryword()
        self.__querylist = query.getquerylist()
        self.__class__.count = self.__class__.count + 1
        self.__id = int(self.__draw_time)%10000000 + 10000000*self.__class__.count
        self.__name = '_'.join(self.__querylist)+'_'+str(self.__id)+'.html'
    def getname(self):
        return self.__name
    def getid(self):
        return self.__id
    def saveHtml(self,path):
        if path[-1]=='/':
            self.__path = path
        else:
            self.__path = path + '/'
        outfile = open(path+self.__name,'w')
        outfile.write(self.__html)
        outfile.close()
    def insertRecord(self,cursor):
        me = [str(self.__id),'null',str(self.__queryid),str(self.__draw_time),self.__path,self.__name,'1','1']
        sql = "insert into listfile value('"+ "','".join(me)  +"')"
        #print sql
        cursor.execute(sql)

if __name__=="__main__":
    root_url = "http://www.ncbi.nlm.nih.gov/pubmed/"
    #query = "olaparib erlotinib"
    querywd = "genome"
    uptime = time.time()
    query = ncbiQuery(root_url,querywd,uptime) 
    
    listfilename = open('updatelist.txt','a')
    conn = db.connect(host='localhost',user='root',passwd='TwAxT7s1UjyoMzxnf7gQ',db='ncbi')
    cur = conn.cursor()
    query.insertRecord(cur)
    conn.commit()

    req = query.getrequest()
    res = urllib2.urlopen(req)
    listhtml = listHtml(res.read(),query)
    path = '/home/qiaoh/getweb/getncbi/downloadfile/listhtml/'
    listhtml.saveHtml(path)
    listhtml.insertRecord(cur)
    listfilename.write(path+listhtml.getname()+'\t'+str(listhtml.getid())+'\n')
    conn.commit()

    listfilename.close()
    cur.close()
    conn.close()
