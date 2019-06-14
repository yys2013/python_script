#-*- coding:utf8 -*-

import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
import webbrowser as web
import itchat
from tkinter import messagebox
from selenium import webdriver

def fecth_mac_book_web(url):
    wbdata = requests.get(url).text
    #print(wbdata)
    #soup = BeautifulSoup(wbdata,'html.parser')
    soup = BeautifulSoup(wbdata,'xml')
    macList = soup.select("div.refurbished-category-grid-no-js > ul > li")
    count = 0
    for cont in macList:
        title = cont.select('a')[0].get_text()
        if title.find('Pro') != -1 and title.find('13') != -1 and title.find('i5') != -1 and title.find('四核') != -1:
            #print(cont.select('a')[0].get("href").strip())
            #print('%s, %s'%(cont.select('a')[0].get_text().strip(), cont.select('div')[0].get_text().strip()))
            count = count + 1
    if count == 0:
        print('No Book!')

    scriptCont = soup.select("script")
    for cont in scriptCont:
        text = cont.get_text()
        if text.find('window.REFURB_GRID_BOOTSTRAP') != -1:
            print('Current Sell:')
            f.write('Current Sell:\n')
            jsonStr = text.split('= ')[1].replace(';', '').strip()
            jsonData = json.loads(jsonStr)
            #print(jsonData['tiles'])
            isHave = 0
            for jsonCont in jsonData['tiles']:
                ptxt = parsejsonCont(jsonCont)
                if len(ptxt) != 0:
                    f.write(ptxt)
            global noticeCount
            if  nType.upper() == 'WX' and noticeCount > 0 and isHave == 0:
                itchat.send('扫描到的产品已经卖完, 继续等待新机会! %s'%nowTime, 'filehelper')
                noticeCount = 0
    print('---------------------------------------------------')
    f.write('---------------------------------------------------\n')

def parsejsonCont(jsonCont):
    dimensionCapacity = ''
    refurbClearModel = ''
    dimensionRelYear = ''
    dimensionScreensize = ''
    ptxt = ''
    title = jsonCont['title']
    try:
        refurbClearModel = jsonCont['filters']['dimensions']['refurbClearModel']
    except Exception:
        print('%s no refurbClearModel' % (title))
    try:
        dimensionRelYear = jsonCont['filters']['dimensions']['dimensionRelYear']
    except Exception:
        print('%s no dimensionRelYear' % (title))
    try:
        dimensionScreensize = jsonCont['filters']['dimensions']['dimensionScreensize']
    except Exception:
        print('%s no dimensionScreensize' % (title))

    if refurbClearModel == 'macbookpro' and dimensionRelYear == '2018' \
    and dimensionScreensize=='13inch':
        try:
            dimensionCapacity = jsonCont['filters']['dimensions']['dimensionCapacity']
        except Exception:
            print('%s no dimensionCapacity'%(title))
        dimensionColor = jsonCont['filters']['dimensions']['dimensionColor']
        tsMemorySize = jsonCont['filters']['dimensions']['tsMemorySize']
        amount = jsonCont['price']['currentPrice']['amount']
        productDetailsUrl = jsonCont['productDetailsUrl']

        cpuType = ''
        if title.find('i5') != -1:
            cpuType = 'i5'
        elif title.find('i7') != -1:
            cpuType = 'i7'
        else:
            cpuType = 'unknown'

        ptxt = 'MacBook Pro %s, %s, %s, %s, %s, %s, %s\n'%(dimensionScreensize, dimensionColor, cpuType, dimensionRelYear, tsMemorySize.upper(), dimensionCapacity.upper(), amount)
        print(ptxt)
        if tsMemorySize == '16gb' and (dimensionCapacity == '512gb' or dimensionCapacity == '1tb') \
        and cpuType == 'i5':
            bookUrl = 'https://www.apple.com%s' % (productDetailsUrl)
            print(bookUrl)
            print('==================================')
            f.write(bookUrl)
            f.write('==================================\n')
            global noticeCount
            if noticeCount < 6:
                if nType.upper() == 'WX':
                    itchat.send('速度点击下面链接, 关注的好东西到了! %s\n %s'%(nowTime, ptxt), 'filehelper')
                    itchat.send(bookUrl, 'filehelper')
                else:
                    messagebox.showwarning("提示", '关注的好东西到了!%s'%nowTime)
            #web.open_new(bookUrl)
            noticeCount = noticeCount + 1
            isHave = 1
    return ptxt

f = ''
nType = ''
nowTime = ''
noticeCount = 0
isHave = 0
if __name__ == '__main__':
    print('请输入通知方式:')
    nType = input()
    if nType.upper() == 'WX':
        print('通知方式： 微信')
        itchat.login()
    else:
        print('通知方式： 本地')
    count = 1
    refurbishedUrl = 'https://www.apple.com/cn/shop/refurbished/mac/512gb-%E6%B7%B1%E7%A9%BA%E7%81%B0%E8%89%B2-%E9%93%B6%E8%89%B2-2018-13-%E8%8B%B1%E5%AF%B8-macbook-pro-16gb'
    while 1:
        f = open('D:/code/python_script/fetch_web_data/data.txt','a', encoding="utf-8")
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('%s, 当前第%d次开始扫描'%(nowTime, count))
        f.write('%s, 当前第%d次开始扫描\n'%(nowTime, count))
        currentTime = time.time()
        url = '%s?%s'%(refurbishedUrl, currentTime)
        fecth_mac_book_web(url)
        f.close()
        if (count == 1 or count % 8 == 0) and nType.upper() == 'WX':
            if noticeCount > 0:
                itchat.send('已经成功扫描到%d次,请尽快下单!%s' % (noticeCount, nowTime), 'filehelper')
            else:
                itchat.send('已经扫描了%d次,不辞劳苦,继续加油！%s' % (count, nowTime), 'filehelper')
        count = count + 1
        time.sleep(90)