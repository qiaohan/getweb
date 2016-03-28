#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re

class ncbi_spider:
    def __init__(self,root,query):
        self.root_url = root

if __name__=="__main__":
    root_url = "http://www.ncbi.nlm.nih.gov/pubmed/"
    query = "olaparib erlotinib"
    html = ncbi_spider.html()
    print html
