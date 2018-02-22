import xlrd
import pymongo

def getAdcode(path):
     excel = xlrd.open_workbook(path)
     sheet1 = excel.sheets()[1]
     row = sheet1.nrows
     print(row)
     client = pymongo.MongoClient('localhost',27017)
     db = client['data']
     collect = db['gdWeatherCode']
     for i in range(1,row):
        collect.insert({'城市':sheet1.cell_value(i,0), 'adcode':sheet1.cell_value(i,1), 'citycode':sheet1.cell_value(i,2)})


#getAdcode('高德地图API 城市编码表.xlsx')

#{"status":"1","count":"1","info":"OK","infocode":"10000","lives":[{"province":"安徽","city":"泾县","adcode":"341823","weather":"阵雨","temperature":"6","winddirection":"北","windpower":"5","humidity":"96","reporttime":"2018-02-18 18:00:00"}]}
client = pymongo.MongoClient('localhost',27017)
db = client['data']
collect = db['gdWeatherCode']
a = list(collect.find({'城市': '长安区'}))
print(a)

