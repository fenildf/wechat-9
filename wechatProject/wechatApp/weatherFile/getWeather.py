import pymongo
import requests
import random
import time
import json
'''
2018.2.18 从数据库中查询到的可迭代对象，和通过api查询返回的数据混淆，one_code不含lives的key
2018.2.19 问题基本解决，但是服务器装上mongodb后卡，无法操作 
'''


user_agents = [
'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
'Mobile/13B143 Safari/601.1]',
'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
'Chrome/48.0.2564.23 Mobile Safari/537.36',
'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
'Chrome/48.0.2564.23 Mobile Safari/537.36']

heads = {
    'User_Agent': random.choice(user_agents)
}

province = ['河北省',
 '山西省',
 '内蒙古自治区',
 '黑龙江省',
 '吉林省',
 '辽宁省',
 '陕西省',
 '甘肃省',
 '青海省',
 '新疆维吾尔自治区',
 '宁夏回族自治区',
 '山东省',
 '河南省',
 '江苏省',
 '浙江省',
 '安徽省',
 '江西省',
 '福建省',
 '台湾省',
 '湖北省',
 '湖南省',
 '广东省',
 '广西壮族自治区',
 '海南省',
 '四川省',
 '云南省',
 '贵州省',
 '西藏自治区']


def referWeather(place):
    '''

    :param place: 地点列表
    :return: 字符串
    '''
    client = pymongo.MongoClient('localhost', 27017)
    db = client['data']
    collect = db['gdWeatherCode']
    if not place[-1][-1] == '市':
        place[-1] += '市'
    code = list(collect.find({'城市': place[-1]}))
    if len(code) == 0:
        return '抱歉，客官您的输入的地点暂无天气信息，您可以检查地点是否正确或者与在后台留言。'
    elif len(code) == 1:
        url = 'http://restapi.amap.com/v3/weather/weatherInfo?city=%s&key=58122721fe32ac8b4219d15db4d35e94'%code[0]['adcode']
        s = requests.get(url, headers=heads)
        weather = json.loads(s.text)
        weather = dealData(weather)
        return weather
    else:
        if len(place) == 1:
            return '客官您输入的地点，全国一共有%d个同名城市，请输入省或者市以便查询。'%len(code)
        else:
            if place[0] in province or place[0]+'省' in province:
                for one_code in code:
                    url = 'http://restapi.amap.com/v3/weather/weatherInfo?city=%s&key=58122721fe32ac8b4219d15db4d35e94'%one_code['adcode']
                    s = requests.get(url, headers=heads)
                    weather = json.loads(s.text)
                    if weather['lives'][0]['province'] == place[0] or weather['lives'][0]['province'] == place[0]+'省':
                        weather = dealData(weather)
                        return weather
            else:
                cityCode = list(collect.find({'城市': place[0]}))
                if len(cityCode) == 0:
                    cityCode = list(collect.find({'城市':place[0]+'市'}))
                for one_code in code:
                    for one_cityCode in cityCode:
                        if one_code['citycode'] == one_cityCode['citycode']:
                            url = 'http://restapi.amap.com/v3/weather/weatherInfo?city=%s&key=58122721fe32ac8b4219d15db4d35e94'%one_code['adcode']
                            s = requests.get(url, headers=heads)
                            weather = json.loads(s.text)
                            weather = dealData(weather)
                            return weather




def dealData(weather):
    '''

    :param weather: json数据
    :return: 字符串
    '''
    province = '省份：' + weather['lives'][0]['province'] + '\n'
    city = '城市：' + weather['lives'][0]['city'] + '\n'
    cityWeather = '天气：' + weather['lives'][0]['weather'] + '\n'
    temperature = '温度：' + weather['lives'][0]['temperature'] + '℃' + '\n'
    winddirection = '风向：' + weather['lives'][0]['winddirection'] + '风' + '\n'
    windpower = '风力：' + weather['lives'][0]['windpower'] + '级' + '\n'
    humidity = '空气湿度：' + weather['lives'][0]['humidity'] + '%' + '\n'
    reporttime = '数据发布时间：' + weather['lives'][0]['reporttime']
    weather = province + city + cityWeather + temperature + winddirection + windpower + humidity + reporttime

    return weather


print(referWeather(['西安']))
