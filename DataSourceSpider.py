# -*- coding: UTF-8 -*-
import requests
import virusmap_main
from bs4 import BeautifulSoup

if __name__ == '__main__':
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
        }

    #目录爬取
    content = []
    contentRaw = requests.get('http://wsjkw.sh.gov.cn/xwfb/index.html', headers=headers)
    contentRaw = contentRaw.text.split('\n')
    #print(contentRaw)
    contentFiltered = virusmap_main.findKeyWord(contentRaw, '<li><a href="(.+?)" title="上海\d+年\d+月\d+日') #筛选新闻
    contentFiltered = sum(contentFiltered,[])
    for i,j in enumerate(contentFiltered) :
        contentFiltered[i] = 'http://wsjkw.sh.gov.cn'+contentFiltered[i] #补全为链接
    print(contentFiltered)

    #每日通报内容爬取
    news = []
    filter = '<span style="font-size: 20px;font-family: 仿宋_GB2312">(.+?)</span></p><p><br/></p>'
    for i in contentFiltered :
        newsChache = requests.get(i, headers=headers).text
        newsFiltered = BeautifulSoup(newsChache, 'lxml').select('#ivs_content')  # 筛选文章内容部分
        news.append(str(newsFiltered[0].get_text()))
    print(news)
    #写入数据
    virusmap_main.mainProgess(news)
