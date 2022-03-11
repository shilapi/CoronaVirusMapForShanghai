import os.path
import re
import xlwings as xw

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
for keyWdOut in virusPlaceTmp :
    try:
        found = re.compile('居住地为(.+?)，|居住于(.+?)，').findall(keyWdOut)
        print(found)
        virusPlaceList.append(found)
    except AttributeError:
        pass
print(virusPlaceList)

virusPlaceListout = [x for j in virusPlaceList for x in j]
sheet1.range(placeStart).options(transpose=True).value = virusPlaceListout

#save stage
exl_main.save('virusPlace.xlsx')
exl_main.close()
