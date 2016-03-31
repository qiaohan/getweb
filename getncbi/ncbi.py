#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re

class ncbi_spider:
    def __init__(self,root,query):
        self.root_url = root
        self.query = query 
        #request = urllib2.Request(data)
        response = urllib2.urlopen(root)
        self.listhtml = response.read()

    def html():
        return listhtml

if __name__=="__main__":
    root_url = "http://www.ncbi.nlm.nih.gov/pubmed/"
    #query = "olaparib erlotinib"
    query = "genome"
    #root_url = "http://www.baidu.com"
    spider = ncbi_spider(root_url,query)
    html = spider.html()
    print html
