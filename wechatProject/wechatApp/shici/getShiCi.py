import requests
from bs4 import BeautifulSoup
import pymongo
import random
import time
'''
2018.2.21 爬取古诗词网，存入数据库中
2018.2.22 ip代理等基本完善,去除空格（&nbsp;）的方法replace('\xa0','')
'''
user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
    'Mobile/13B143 Safari/601.1]',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/48.0.2564.23 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/48.0.2564.23 Mobile Safari/537.36'
]

heads = {
    'User_Agent': random.choice(user_agents)
}

urls = ['http://www.gushiwen.org/shiwen/default_4A1A1.aspx', 'http://www.gushiwen.org/shiwen/default_4A2A1.aspx', 'http://www.gushiwen.org/shiwen/default_4A3A1.aspx', 'http://www.gushiwen.org/shiwen/default_4A4A1.aspx']

client = pymongo.MongoClient('localhost', 27017)
db = client['data']
collect = db['shi']

def getGSW(url,proxy):
    #response = requests.get(url,headers=heads,proxies=proxies)
    try:
        response = requests.get(url,headers=heads,proxies=proxy)
    except:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    main3 = soup.find('div', class_='main3')
    left = main3.find('div', class_='left')
    sons = left.find_all('div', class_='sons')
    for son in sons[3:]:
        p = son.find_all('p')
        title = p[0].a.b.text
        source = p[1].find_all('a')
        dynasty = source[0].text
        author = source[1].text
        main_text = son.find('div',class_='contson').text.replace('\n', '')
        try:
            tags = son.find('div', class_='tag').find_all('a')
        except:
            tagList = []
        else:
            tagList = [tag.text for tag in tags]
        try:
            good = int(son.find('div', class_='good').a.span.text.replace('\xa0', ''))
        except:
            good = 0
        collect.insert(
            {
                'title':title,
                'dynasty':dynasty,
                'author':author,
                'main_text':main_text,
                'tags':tagList,
                'good':good
            }
        )

def getIp():
    '''

    :return: 一个ip
    '''
    ipHeads = {
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':random.choice(user_agents),
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer':'http://www.xicidaili.com/nn/',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    }
    page = int(random.uniform(0,20))
    url = 'http://www.xicidaili.com/nn/%d'%page
    response = requests.get(url, headers = ipHeads)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    trList = soup.find_all('tr')
    try:
        a = random.randint(1,len(trList)-1)
        tr = trList[a]
    except:
        print('-'*20,'第%d页,第%d条数据，ip条数总共有%d'%(page,a,len(trList)))
        tr = trList[random.randint(1,len(trList)-1)]
    tdList = tr.find_all('td')
    ip = tdList[1].get_text()
    port = tdList[2].get_text()
    http = tdList[5].get_text().lower()
    proxy = {http:ip + ':' + port}
    return proxy




proxy = getIp()
i = 1
while i != 4925:
    url = 'http://www.gushiwen.org/shiwen/default_4A1A%d.aspx'%i
    try:
        getGSW(url,proxy)
    except:
        proxy = getIp()
        print('#'*10,'第%d页失败'%i)
        time.sleep(3)
        continue
    print('第%d页爬取完毕'%i)
    i += 1
    time.sleep(3)
