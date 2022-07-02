from bs4 import BeautifulSoup
import requests
import core.status  as status
# import e.status  as status
import time



def get_source(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text


def get_info(source):
    # 解决网页乱码，添加'html5lib'，而不是lxml
    soup = BeautifulSoup(source, 'html5lib')  # pip install html5lib
    # 1.进入整体表格
    conMidtab = soup.find('div', class_='conMidtab')
    # 2.进入子表格
    tables = conMidtab.find_all('table')
    # 3.进入每个子表格收集天气信息
    info = []
    for table in tables:
        # (1)过滤前两个（城市和时间）
        trs = table.find_all('tr')[2:]  # tr存储了每个城市的天气信息
        # enumerate 返回2个值第一个是下标 第二个下标所对应的元素
        # (2)进入每个城市（每一行），判断是否是省会
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')  # td存储每个城市天气信息的每个具体项目
            # 城市名字判断：因为对于每个省份的第一行的第一列为省名，对应不了省会。爬取会出错，因而要判断修改
            city_td = tds[0] # 城市
            if index == 0:  #  index==0，代表的是第一个tr，第一个城市
                city_td = tds[1] # 省会
        # (3)获取每个城市的具体天气项目
            city = list(city_td.stripped_strings)[0]  # 城市名字
            # 该城市最低气温
            temp_low_td = tds[-2]
            temp_low = list(temp_low_td.stripped_strings)[0]
            # print('城市:', city, '最高气温:', temp_high,'最低气温:',temp_low)
            item = city,temp_low
            info.append(item)
    return info  # 存储在info内部

def get_weather():
    print("ttttttttttttt")
    while(True):
        url = 'http://www.weather.com.cn/textFC/anhui.shtml'
        source = get_source(url)
        info = get_info(source)
        status.weather=info[7][0]+info[7][1]+"℃"
        print(status.weather)
        time.sleep(3600)
        # print(status.city,",",status.weather)

