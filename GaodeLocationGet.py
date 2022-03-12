import requests as rq
import xml.dom.minidom

def location(address,key):
    httpText = rq.get('https://restapi.amap.com/v3/geocode/geo?address='+address+'&output=XML&key='+key).text
    dom = xml.dom.minidom.parseString(httpText)
    root = dom.documentElement
    locationElement = root.getElementsByTagName('location')
    print(locationElement)
    try:
        item = locationElement[0]
        dataComplex = str(item.firstChild.data)
        dataFinal = dataComplex#.split(',',1)
        return dataFinal
    except IndexError:
        print('errorhere'+httpText)
