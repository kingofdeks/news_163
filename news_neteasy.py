# -*- coding:utf-8 -*-

import os,time
import sys
import urllib
from urllib import request
import re
from lxml import etree


def StringListSave(save_path, filename, slist):  #在爬虫所在的文件夹中创建文件夹保存网页新闻信息
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0], s[1]))

def CellPage(save_path, filename, slist):    #将每个新闻网页以html格式保存在对应的文件夹内
    '''单个新闻内容的存储'''
    folder = save_path+'/'+filename
    print (folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    i = 0
    for item, url in slist:
        #设置每个频道保存多少条
        if i >= 200:break
        #过滤不符合windows的文件名
        newitem = re.sub(r"[\/\\\:\*\?\"\<\>\|]","",item)
        print (item)
        with open(folder+'/'+newitem+'.html', "w+", encoding='GB18030') as fp:
            PageContent = request.urlopen(url).read().decode("GB18030")
            fp.write("%s\n" %  PageContent)
        i += 1

def Page_Info(myPage):     #用正则分析原始页面
    mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage, re.S)
    return mypage_Info

def New_Page_Info(new_page):    #Xpath分析出新闻首页中新闻标题和链接，然后打包返回
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    return zip(new_items, new_urls)

def Spider(url):    #爬虫主程序
    i = 0
    print ("downloading ", url)
    myPage = request.urlopen(url).read().decode("GB18030")
    myPageResults = Page_Info(myPage)
    ntime = time.strftime("%Y%m%d",time.localtime(time.time()))
    save_path = "news-" + ntime
    filename = str(i)+"_"+u"Ranking"
    StringListSave(save_path, filename, myPageResults)
    i += 1                                            #设置保存文件的格式的位置
    for item, url in myPageResults:                   #写入爬取后的标题和链接
        print ("downloading ", url)
        new_page = request.urlopen(url).read().decode("GB18030")
        newPageResults = New_Page_Info(new_page)
        filename = str(i)+"_"+item
        StringListSave(save_path, filename, newPageResults)
        newPageResults = New_Page_Info(new_page)
        CellPage(save_path, filename, newPageResults)
        i += 1


if __name__ == '__main__':
    print ("start")
    start_url = "http://news.163.com/rank/"
    Spider(start_url)
    print ("end")