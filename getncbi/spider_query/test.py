#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re
import time
import httplib

if __name__=="__main__":
    url = "http://www.ncbi.nlm.nih.gov/pubmed"
    #query = "olaparib erlotinib"
    querywd = "genome"
    f = open('para.txt')
    parameter = {}
    for line in f:
        line = line[0:len(line)-1]
        t = line.split(':')
        parameter[t[0]] = t[1]
    f.close()
    f = open('header.txt')
    head = {}
    for line in f:
        line = line[0:len(line)-1]
        t = line.split(':')
        head[t[0]] = ':'.join(t[1:])
    f.close()
    #print parameter
    opener = urllib2.build_opener((urllib2.HTTPCookieProcessor()))
    for i in range(0,3):
        print i
        if i==0:
            req = urllib2.Request(url,urllib.urlencode({'term':'genome'}))
            res = opener.open(req)
        else:
            #opener = urllib2.build_opener((urllib2.HTTPCookieProcessor()))
            parameter['EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.CurrPage'] = str(i+1)
            parameter['EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.cPage'] = str(i)
            data = urllib.urlencode(parameter)
            #conn = httplib.HTTPConnection('2607:f220:41e:4290::110',80)
            #conn.request('POST','/pubmed',data,head)
            #res = conn.getresponse()
            req = urllib2.Request(url,data,head)
            #res = urllib2.urlopen(req)
            res = opener.open(url,data)
        ff = open('/home/qiaohan/genecrab/getweb/getncbi/html/'+str(i)+'.html','w')
        ff.write(res.read())
        ff.close()
