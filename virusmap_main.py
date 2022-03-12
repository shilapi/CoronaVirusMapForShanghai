import os.path
import re
import xlwings as xw
import numpy as np

def findKeyWord(keyString,regex) :
    final = []
    for keyString in virusPlaceTmp:
        try:
            matchRule = re.compile(regex)
            found = matchRule.findall(keyString)
            print(found)
            final.append(found)
        except AttributeError:
            pass
    print(final)
    return final

if os.path.isfile('virusPlace.xlsx'):
    exl_main = xw.Book('virusPlace.xlsx')
    sheet1 = exl_main.sheets['sheet1']
    i = 1
    while True:
        findLocation = 'A'
        placeStart = findLocation + str(i)
        locationNow = sheet1.range(placeStart).value
        if locationNow == None:
            break
        i=i+1
    print('Start editing excel in ' + placeStart)
else:
    placeStart = 'A1'
    exl_main = xw.Book()
    sheet1 = exl_main.sheets['sheet1']

virusPlaceListInput = []
virusPlaceList = []
while True:
    chache=input("start")
    if chache == 'end':
        break
    virusPlaceListInput.append(chache)
print(virusPlaceListInput)
virusPlaceTmp = [s for s in virusPlaceListInput if "居住" in s]
print(virusPlaceTmp)

#'(居住地为(.+?)，)|(居住于(.+?)，)'
virusPlaceList.append(findKeyWord(virusPlaceTmp,'居住地为(.+?)，'))
virusPlaceList.append(findKeyWord(virusPlaceTmp,'居住于(.+?)，'))

virusPlaceListOut = np.unique(sum(sum(virusPlaceList,[]),[]))
print('outputStart'+str(virusPlaceListOut))
sheet1.range(placeStart).options(transpose=True).value = virusPlaceListOut

#save stage
exl_main.save('virusPlace.xlsx')
exl_main.close()
