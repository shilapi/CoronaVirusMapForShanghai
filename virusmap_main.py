import datetime
import os.path
import re
import time
import xlwings as xw
import numpy as np
import GaodeLocationGet


# 关键词查找&提取到列表
def findKeyWord(sourceString,regex) :
    final = []
    for sourceStringClip in sourceString:
        try:
            matchRule = re.compile(regex)
            found = matchRule.findall(sourceStringClip)
            #print(found)
            if found != [] :
                final.append(found)
        except AttributeError:
            pass
    print(final)
    return final


def mainProgess(virusPlaceListInput):
    '''
    # 建立excel文件或打开文件
    if os.path.isfile('virusPlace.xlsx'):
        exl_main = xw.Book('virusPlace.xlsx')
        sheet1 = exl_main.sheets['sheet1']
        i = 1
        #查找起始编辑区域
        while True:
            findLocation = 'A'
            placeStart = findLocation + str(i)
            locationNow = sheet1.range(placeStart).value
            if locationNow == None:
                break
            i=i+1
        print('Start editing excel in ' + placeStart)
        placeStart = str(i)
    else:
    '''
    # 从表格头部编辑
    placeStart = '2'
    exl_main = xw.Book()
    sheet1 = exl_main.sheets['sheet1']
    sheet1.range('a1').value = ['地址', '经纬度']  # 增加表头

    virusPlaceList = []
    print('input Here')
    print(virusPlaceListInput)
    virusPlaceTmp = [s for s in virusPlaceListInput if "居住" in s]  # 初筛
    print(virusPlaceTmp)

    # 提取地址
    # '(居住地为(.+?)，)|(居住于(.+?)，)'
    virusPlaceList.append(findKeyWord(virusPlaceTmp, '居住地为(.+?)，'))
    virusPlaceList.append(findKeyWord(virusPlaceTmp, '居住于(.+?)，'))

    # 写入地址
    virusPlaceListOut = np.unique(sum(sum(virusPlaceList, []), []))
    print('outputStart' + str(virusPlaceListOut))
    sheet1.range('a' + placeStart).options(transpose=True).value = virusPlaceListOut

    # 查找经纬度并写入
    viruslocationList = []
    for address in virusPlaceListOut:
        locationChache = GaodeLocationGet.location(address, '4050c5266eaba083b4dda056ae8d3633')  # Token为个人token，请勿滥用
        if locationChache == None:
            locationChache = ['', '']
        viruslocationList.append(locationChache)
        time.sleep(0.01)  # 防止服务器拒绝访问
    print('outputStart' + str(viruslocationList))
    sheet1.range('b' + placeStart).options(transpose=True).value = viruslocationList

    # save&close session
    exl_main.save('virusPlace'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'.xlsx')
    exl_main.close()


if __name__ == '__main__':
    virusPlaceListInput = []
    #通报输入
    while True:
        chache=input("start")
        if chache == 'end':
            break
        virusPlaceListInput.append(chache)

    mainProgess(virusPlaceListInput)