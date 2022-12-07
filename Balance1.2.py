# -*- coding: utf-8 -*-
"""
Created on Mon Nov  28 16:44:51 2022

@author: Einck(WA2114174 张博文)

主要参考：
https://blog.csdn.net/weixin_43271108/article/details/106713402
http://www.voycn.com/article/python-paquwangyi-buff-shipinshujuji-steam-shipin
shichangshuju-dadaozheshangzhe
"""

from requests import get
from re import findall,M
from pandas import DataFrame
from time import time,sleep

time_start = time()#程序开始运行时间

def main():
    class Time:#计算时间
        @staticmethod 
        def minute():  
            now_time=time()
            dec = now_time - time_start
            minute_temp = int(dec / 60)
            return minute_temp
        def second():
            now_time=time()
            dec = now_time - time_start
            second_temp = dec % 60
            return second_temp
#选择运行模式 test: 可选爬取页数，耗时短 normal：正常运行，耗时长           
    mode= input("Please input mode:\n1:test   2:normal\n")
    try:
        mode = int(mode)
    except ValueError:
        print("Error: mode input error!")
        return
    if mode != 1 and 2:
        print("Error: mode input error!")
        return
    
    if mode == 1:
        maxpage=input("Please input max pages:")
        try:
            maxpage = int(maxpage)
        except ValueError:
            print("Error: mode input error!")
            return
    #获取表头和cookies
    buff_headers_str=input("Please input buff headers:")
    buff_cookies_str=input("Please input buff cookies:")
    buff_headers={}
    buff_headers['User-Agent']=buff_headers_str
    try:
        buff_cookies={}
        for line in buff_cookies_str.split(';'):
            key, value = line.split('=', 1)
            buff_cookies[key] = value
    except ValueError:
        print("Error: cookies input error!")
        return
    #初始化    
    names_list = []
    price_list = []
    steam_price_list = []
    balance_rate_list=[]
    #开始爬取
    print("%02d:%02d" % (Time.minute(), Time.second()),"Geting the data...")
    #爬取武器类型
    source_page_url = "https://buff.163.com/market/?game=csgo#tab=selling&page_num=1"
    try:
        cat_response = get(url=source_page_url, headers=buff_headers, cookies=buff_cookies)
    except ConnectionError:
        print("Error: headers or cookies input error or network unconnect!")
        return
    html_text0 = cat_response.text
    category_list = findall( r'li value="weapon_(.+?)">', html_text0, M)
    
    if mode == 1:
        maxpage = min(len(category_list),maxpage)
    else:
        maxpage = len(category_list)
    #爬取单个武器页数 
    for i in range(maxpage):
        category_list[i] = "weapon_" + category_list[i]
        category_url = "&category=" + category_list[i]
        first_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1' + category_url
        page_response = get(url=first_url, headers=buff_headers, cookies=buff_cookies)
        html_text1 = page_response.text
        page_num_list = findall(r'"total_page": (.*)', html_text1, M)
        page_num = int(page_num_list[0])
        #爬取单个武器种类及信息
        if mode == 1:
            page_num = min(page_num,maxpage)
        for j in range(page_num):
            print("%02d:%02d" % (Time.minute(),Time.second()),category_list[i], "page" ,j+1,"total" ,page_num)
            page_url='https://buff.163.com/api/market/goods?game=csgo&page_num='+str(j+1) + category_url
            page_response = get(url=page_url, headers=buff_headers, cookies=buff_cookies)
            html_text2 = page_response.text
            #爬取饰品中文名
            names_list_temp = findall(r'"name": "(.*)",', html_text2, M)
            #将饰品名转化为中文
            for p in range(len(names_list_temp)):
                names_list_temp[p] = names_list_temp[p].encode('ascii').decode('unicode_escape')
            #爬取buff最低售价
            price_list_temp = findall(r'"sell_min_price": "(.*)",', html_text2, M)
            #爬取steam最低售价
            steam_price_list_temp = findall(r'"steam_price_cny": "(.*)"',html_text2,M)
            names_list += names_list_temp
            price_list += price_list_temp
            steam_price_list += steam_price_list_temp
            sleep(15)#停止爬取15秒，防止封号
    print("%02d:%02d" % (Time.minute(), Time.second()),"Processing...")  
    #处理数据，计算steam余额与人民币的换算比率
    for k in range(len(price_list)):
        balance_rate = round(float(price_list[k])/(float(steam_price_list[k])*0.87),2)
        balance_rate_list.append(balance_rate)
    #将数据导入表格    
    excel_name = ["name","price","steam price","balance rate"]
    excel_data = zip(names_list,price_list,steam_price_list,balance_rate_list)
    items_information = DataFrame(columns=excel_name, data=excel_data)
    try:
        items_information.to_excel("items_information.xlsx")
    except :
            print("Error: excel storage error!")
    print("%02d:%02d" % (Time.minute(), Time.second()),"Completion!")
#程序运行
if __name__ == "__main__":
    main()