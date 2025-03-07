# -*- coding=utf-8 -*-
import time

import requests
from lxml import etree
from chardet import detect
from datetime import datetime
from urllib import parse
from lxml.html.clean import Cleaner
import xlsxwriter
import math
import random
from selenium.webdriver.common.by import By

def open_url(url , params , refer=None):
    headers = get_request_headers(refer)

    # 避免请求被拒绝（403 Forbidden），延迟几秒后请求服务器
    time.sleep(random.randint(2,6))
    response = requests.get(url, headers=headers, params=params,  allow_redirects=True)
    print(response.url)
    # 服务器返回异常页面
    if 200 != response.status_code :
        print(response.url)
        print('Response Status Code: ' + str(response.status_code))
        print(response)
    return response


def get_request_headers(referer=None):
    "返回一个http请求头"
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    ]
    ua = random.choice(user_agents)

    headers = {
        "User-Agent": ua,
        "Host": "search.ccgp.gov.cn",
        "Referer": referer if referer else "http://search.ccgp.gov.cn/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",  # 修正连字符格式
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    return headers
    # user_agents1 = [
    #     'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    #     'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36',
    #     'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
    #     'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
    #     'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
    #     'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
    #     'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    # ]
    # user_agents = [
    #     'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    #     'Opera/9.25 (Windows NT 5.1; U; en)',
    #     'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    #     'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    #     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    #     'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    #     "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    #     "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    # ]
    #
    # ua = random.choice(user_agents1)
    # # ua = random.choice(user_agents)
    # # print(ua)
    #
    # headers= {"Referer":referer,
    #           'Host': 'search.ccgp.gov.cn',
    #           'Upgrade-Insecure-Requests': '1',
    #           'Connection': 'keep - alive' ,
    #           'Accept - Encoding': 'gzip, deflate',
    #           'Accept - Language': 'zh - CN, zh;q = 0.9',
    #           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #           'Cookie' : 'Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1650939609,1651830589,1652150458,1652234205; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1650076632,1651830642,1652150461,1652234207; JSESSIONID=wt3AifLykOW8vb0IzXfwXbcfRCRSWLzNDS6bzKIwGZ-Sw8VjFORl!-1094063090; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1652498396; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1652499001'
    #           }
    # headers["User-Agent"] = ua
    # # headers["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    # return headers

def crawler_ccgp(sheetdata=[], year='', buyerName=''):
    from datetime import datetime,timedelta
    import math
    from lxml import etree
    import requests
    from chardet import detect

    url = 'http://search.ccgp.gov.cn/bxsearch?'
    curr_date = datetime.now()
    start_date = curr_date - timedelta(days=30)
    start_time = start_date.strftime("%Y:%m:%d")
    end_time = curr_date.strftime("%Y:%m:%d")
    '''
    curr_year = curr_date.year
    curr_date = datetime.now()
    curr_year = curr_date.year
    y = curr_year - int(year)
    if y < 1:
        start_time = str(curr_year) + ':01:01'
        end_time = str(curr_year) + ':12:31'
    else:
        start_time = year + ':01:01'
        end_time = year + ':12:31'
    '''
    # http://search.ccgp.gov.cn/bxsearch?
    # searchtype=1
    # &page_index=1
    # &bidSort=0
    # &buyerName=
    # &projectId=
    # &pinMu=0
    # &bidType=0
    # &dbselect=bidx
    # &kw=%E7%AD%89%E7%BA%A7%E4%BF%9D%E6%8A%A4
    # &start_time=2025%3A01%3A14
    # &end_time=2025%3A02%3A14
    # &timeType=6
    # &displayZone=%E5%B1%B1%E8%A5%BF
    # &zoneId=14
    # &pppStatus=0
    # &agentName=

    # http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0
    # &buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=%E7%AD%89%E7%BA%A7%E4%BF%9D%E6%8A%A4
    # &start_time=2025%3A02%3A01&end_time=2025%3A02%3A14&timeType=6&displayZone=%E5%B1%B1%E8%A5%BF&zoneId=14&pppStatus=0&agentName=
    print(start_time + "\n" + end_time + "\n")
    params = {
        'searchtype': 1,
        'page_index': 1,
        'bidSort': 0,
        'buyerName': '',
        'projectId': '',
        'pinMu': 0,
        'bidType': 0,
        'dbselect': 'bidx',
        'kw': '等级保护',
        'start_time': start_time,
        'end_time': end_time,
        'timeType': 6,
        'displayZone': '山西',
        'zoneId': '14',
        'pppStatus': 0,
        'agentName': ''
    }
    # 调用自定义的 open_url 函数
    
    resp = open_url(url, params)
    print(resp)
    resp.raise_for_status()  # 检查响应状态

    referer = resp.url
    ecoding = detect(resp.content).get('encoding', 'utf-8')
    html = resp.content.decode(ecoding)
    
    tree = etree.HTML(html)
    
    try:
        total = int(tree.xpath('/html/body/div[5]/div[1]/div/p[1]/span[2]')[0].text.strip())
    except IndexError:
        print("Not fund total datas number")
        return sheetdata

    print('found data from web page;Total: ' + str(total))

    if total > 0:
        pagesize = math.ceil(total/20)  #计算出有多少页
        curr_page = 1
        sheetdata = sheetdata  #存储抓取的数据
        while(curr_page <= pagesize):
            # 开始抓取项目信息
            list = tree.xpath('/html/body/div[5]/div[2]/div/div/div[1]/ul/li')

            # print(etree.tostring(ul) )
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            # import re

            # rp3 = '公开招标|询价公告|竞争性谈判|单一来源|资格预审|中标公告|更正公告|其他公告|竞争性磋商|成交公告|终止公告)'  # 直接使用关键字
            # i = 1
            # for li in list:
            #     title = li[0]
            #     summary = li[1]
            #     span = li[2]
            #     info = span.xpath('string()').replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')

            #     # 使用正则表达式查找匹配位置
            #     match = re.search(rp3, info)
            #     print(match)
                
            #     if match:
            #         str1 = info[:match.start()]
            #         str2 = info[match.start() + len(rp3):]  # 匹配字符串之后的部分
            #         strs = str2.split('|')
            #     else:
            #         str1 = info  # 如果没有匹配，保留整个字符串
            #         strs = []  # 没有分割结果

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            rp3 = '公告'  # 直接使用关键字
            i = 1
            for li in list:
                # print(i , li[0].text.strip() , li[2].text.strip())
                
                title = li[0]
                summary = li[1]
                span = li[2]
                info = span.xpath('string()').replace(' ','').replace('\r','').replace('\n','').replace('\t','')

                str1 = info[:info.index(rp3)]
                str2 = info[info.index(rp3):].replace(rp3,'' )

                strs = str2.split('|')
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 

                # if len(strs) > 1 and is_exist(strs[1].split('/')):
                if len(strs) > 1:
                    row = []
                    row.insert(0, len(sheetdata) + 1)
                    row.insert(1,rp3.replace('|',''))
                    row.insert(2,title.text.strip())
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    from selenium import webdriver

                    # 启动浏览器
                    driver = webdriver.Chrome()

                    # 打开目标网页
                    driver.get(resp.url)

                    # 找到链接元素
                    ele = title.text.strip()
                    link_element = driver.find_element(By.XPATH, f"//a[contains(text(), '{ele}')]")
                    link_href = link_element.get_attribute("href")

                    print(link_href)  # 输出链接的 href

                    # 关闭浏览器
                    driver.quit()
                    row.insert(7,link_href)
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                   
                    # row.insert(7,title.get('href'))
                    row.insert(8,summary.text.strip())

                    str1s = str1.split('|')
                    row.insert(3,str1s[0][:10])
                    row.insert(4,str1s[1].replace('采购人：',''))
                    row.insert(5,str1s[2].replace('代理机构：',''))
                    row.insert(6,strs[0])
                    # print(str1 , str2)
                    # print(i, info )
                    i += 1
                    # print(row)
                    sheetdata.append(row)
            # 抓取下一页
            curr_page += 1
            if curr_page <= pagesize :
                params['page_index'] = curr_page
                print('total{}pages, now{}page'.format(pagesize, curr_page))

                resp = open_url(url , params ,referer)
                if 200 != resp.status_code:
                    continue

                # resp = requests.get(url, timeout=15)
                ecoding = detect(resp.content).get('encoding')
                html = resp.content.decode(ecoding)
                tree = etree.HTML(html)
                referer = resp.url
                
    return sheetdata


def is_exist(keys):
    "传入抓取的标签列表，判断这条标讯是不是我们需要的数据"
    fs = ['信息技术服务','软件开发服务','运行维护服务','信息系统集成实施服务',
          '计算机设备及软件','计算机软件','通用设备','计算机网络设备']
    for s in fs:
        if s in keys:
            return True
    else:
        return False
    # print( )


def writer_excel(data, head=['A1','A2','A3','A4','A5','A6','A7','A8'] ,  sheetname='sheet1',filename='DataFile'):
    "用XlsxWriter库把数据写入Excel文件"
    workbook = xlsxwriter.Workbook(filename+'.xlsx')
    worksheet = workbook.add_worksheet(sheetname)

    row = 0
    col = 0

    # 插入表头
    cvi = 0
    for cv in head:
        worksheet.write(row, col + cvi, cv)
        cvi += 1
    row += 1
    # 插入表数据
    for rowdata in data:
        cvindex  = 0
        for cv in rowdata:
            worksheet.write(row, col + cvindex, cv)
            cvindex += 1
        row += 1
    workbook.close()

if __name__ == "__main__":
    start_year = 2024  #从哪年开始抓取数据
    buyer_name = ''
    sheetdata = []
    curr_time = datetime.now()
    curr_year = curr_time.year
    y = curr_year - start_year
    if y >= 0 :
        year = curr_year
        print(str(year))
        sheetdata = crawler_ccgp( sheetdata,  str(year) , buyer_name)
    else:
        print(y)

    # print(curr_time)
    print('acquired ' + str(len(sheetdata)), 'pieces of data')
    print(sheetdata)

    head = ['序号','类型','名称','日期','招标人','代理机构','区域','详情','项目概况']
    writer_excel(sheetdata ,head , '中标公告',buyer_name + '-'+ str(curr_time).replace(':','.'))