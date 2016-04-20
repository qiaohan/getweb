#!/usr/bin/env python
# coding=utf-8
import urllib
import re
import time
from datetime import datetime
import MySQLdb as db
import sys

class abstractHtml:
    def __init__(self,htmlcode,pmid):
        self.__html = htmlcode
        t = datetime.now()
        self.__uptime = "%04d%02d%02d%02d%02d%02d%03d"%(t.year,t.month,t.day,t.hour,t.minute,t.second,int(1000*t.microsecond))
        self.__pmid = pmid
        self.__name = str(self.__pmid)+'.html'
    def getname(self):
        return self.__name
    def getid(self):
        return self.__pmid
    def save(self,path):
        if path[-1]=='/':
            self.__path = path
        else:
            self.__path = path + '/'
        outfile = open(path+self.__name,'w')
        outfile.write(self.__html)
        outfile.close()
    def insert_pmabstractfile(self,cursor):
        me = [str(self.__pmid),self.__uptime,self.__path]
        sql = "insert into pmabstractfile value('"+ "','".join(me)  +"')"
        cursor.execute(sql)
    def hascontent(self):
        p = re.compile('<title>.*? -')
        s,e = re.search(p,self.__html).span()
        title = self.__html[s+7:e-2]
        if title == 'Error':
            return False
        else:
            self.__title = title
            return True
if __name__=="__main__":
    conn = db.connect(host='localhost',user='pubmed',passwd='ncbipubmed',db='ncbi_pubmed')
    cur = conn.cursor()
    path = '/opt/allpubmed_abstract/'
    pmstart = int(sys.argv[1])
    pmend = int(sys.argv[2])
    for pmid in range(pmstart,pmend):
        print 'pmid:',pmid
        for i in range(0,10):
            try:
                abshtml = abstractHtml(urllib.urlopen('http://www.ncbi.nlm.nih.gov/pubmed/'+str(pmid)).read(),pmid)
                if abshtml.hascontent():
                    abshtml.save(path)
                    abshtml.insert_pmabstractfile(cur)
                    conn.commit()
            except Exception,e:
                print e
                time.sleep(1)
            else:
                break
    cur.close()
    conn.close()
