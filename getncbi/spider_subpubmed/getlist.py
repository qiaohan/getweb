#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re
import time
from datetime import datetime
import random
import MySQLdb as db
from multiprocessing import Process,Queue
import hashlib

class ncbiQuery:
    count = 0
    postbody = {}
    for line in open('page_body.http'):
        line = line[0:len(line)-1]
        t = line.split(':')
        postbody[t[0]] = t[1]
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
    def getrequest(self,page):
        if page == 1:
            value = {'term':self.__query}
            data = urllib.urlencode(value)
            request = urllib2.Request(self.__base_url,data)
        else:
            body = self.__class__.postbody
            body['EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.CurrPage'] = str(page)
            body['EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.cPage'] = str(page-1)
            data = urllib.urlencode(body)
            request = urllib2.Request(self.__base_url,data)
        return request
    def insertRecord(self,cursor):
        me = [str(self.__queryid),self.__base_url,self.__query,str(self.__update_time)]
        sql = "insert into querylog value('"+ "','".join(me)  +"')"
        #print sql
        cursor.execute(sql)

class listHtml:
    #count = 0
    def __init__(self,htmlcode,query):
        self.__html = htmlcode
        self.__draw_time = time.time()
        self.__queryid = query.getid()
        self.__querywd = query.getqueryword()
        self.__querylist = query.getquerylist()
        #self.__class__.count = self.__class__.count + 1
        #self.__id = int(self.__draw_time)%10000000 + 10000000*self.__class__.count
        self.__id = int( (self.__draw_time+random.random())*1000 )
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
        outfile = open(self.__path+'w0.html','w')#self.__name,'w')
        outfile.write(self.__html)
        outfile.close()
    def insertRecord(self,cursor):
        me = [str(self.__id),'null',str(self.__queryid),str(self.__draw_time),self.__path,self.__name,'1','1']
        sql = "insert into listfile value('"+ "','".join(me)  +"')"
        #print sql
        cursor.execute(sql)

def getlist(queue,opener,req,path,filename):
    for i in range(0,10):
        try:
            res = opener.open(req,timeout=60)
            conn = db.connect(host='localhost',user='subpubmed',passwd='ncbisubpubmed',db='subpubmed')
            cur = conn.cursor()
            listhtml = listHtml(res.read(),query)
            listhtml.saveHtml(path)
            listhtml.insertRecord(cur)
            queue.put(path+listhtml.getname()+'\t'+str(listhtml.getid())+'\n')
            conn.commit()
            cur.close()
            conn.close()
        except Exception,e:
            print e
            time.sleep(2)
        else:
            break

if __name__=="__main__":
    root_url = "http://www.ncbi.nlm.nih.gov/pubmed/"
    #query = "olaparib erlotinib"
    querywd = '(tumor OR cancer) mutation ("2006/01/01"[Date - Publication] : "3000"[Date - Publication])'
    #uptime = datetime.now()
    query = ncbiQuery(root_url,querywd) 
    #filename = 'updatelist.txt'
    #listupfile = open(filename,'a')
    #conn = db.connect(host='localhost',user='qiaoh',passwd='qiaohan123',db='ncbi_pubmed_qiaoh')
    #cur = conn.cursor()
    #query.insertRecord(cur)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    path = '/var/www/html/qiaoh/'
    #path = '/home/qiaoh/getweb/getncbi/downloadfile/listhtml/'
    #q = Queue()
    process = []
    num = 1
    for i in range(0,num):
        try:
            req = query.getrequest(i+1)
            if i==0:
                conn = db.connect(host='localhost',user='subpubmed',passwd='ncbisubpubmed',db='subpubmed')
                cur = conn.cursor()
                res = opener.open(req)
                listhtml = listHtml(res.read(),query)
                listhtml.saveHtml(path)
                #listhtml.insertRecord(cur)
                #listupfile.write(path+listhtml.getname()+'\t'+str(listhtml.getid())+'\n')
                conn.commit()
                cur.close()
                conn.close()
            else:
                p = Process(target=getlist,args=(q,opener,req,path,filename))
                p.start()
                process.append(p)
        except Exception,e:
            print e
    for i in range(1,num):
        process[i-1].join()
    #while not q.empty():
    #    listupfile.write(q.get())
    #listupfile.close() 
