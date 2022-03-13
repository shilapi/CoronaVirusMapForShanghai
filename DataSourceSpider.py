# -*- coding: UTF-8 -*-
import os
import requests
import virusmap_main
from bs4 import BeautifulSoup


def contentGet(url):
    # 目录爬取
    spiderHeaders = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
        }
    content = []
    contentRaw = requests.get(url,headers=spiderHeaders)
    contentRaw = contentRaw.text.split('\n')
    # print(contentRaw)
    contentFiltered = virusmap_main.findKeyWord(contentRaw, '<li><a href="(.+?)" title="上海\d+年\d+月\d+日')  # 筛选新闻
    contentFiltered = sum(contentFiltered, [])
    for i, j in enumerate(contentFiltered):
        contentFiltered[i] = 'http://wsjkw.sh.gov.cn' + contentFiltered[i]  # 补全为链接
    return contentFiltered


def newsGet(content) :
    # 每日通报内容爬取
    spiderHeaders = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
        }
    filter = '<span style="font-size: 20px;font-family: 仿宋_GB2312">(.+?)</span></p><p><br/></p>'
    newsChache = requests.get(content, headers=spiderHeaders).text
    newsFiltered = BeautifulSoup(newsChache, 'lxml').select('#ivs_content')  # 筛选文章内容部分
    try :
        news.append(str(newsFiltered[0].get_text()))
    except IndexError :
        pass
    return news


if __name__ == '__main__':
    news = []
    contentPageList = ['', '_2', '_3', '_4', '_5']
    newsContent =[]
    for i in contentPageList :
        newsContent.append(contentGet('http://wsjkw.sh.gov.cn/xwfb/index'+i+'.html'))
        newsChache = []
    for i in newsContent :
        try :
            for j in i :
                newsChache.append(j)
        except all :
            pass
    newsContent = newsChache
    print(newsContent)
    for i in newsContent :
        news.append(newsGet(i))
    print(news)
    # 写入数据
    virusmap_main.mainProgess(news)
