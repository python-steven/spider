import xlwt
import os
import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
from http import cookiejar
from requests import exceptions
from AEMSLite.settings import BASE_DIR
from openpyxl import Workbook

def crawl_data(username, password, plantcode, filepath='.', ddate=None):
    '''
    :param username: str 用户名
    :param password: str 密码
    :param plantcode: str 厂别
    :param filepath: str 存放文件的路径，默认为当前目录
    :param date:    date 查询日期 ，默认为昨天
    :return:        list 返回的数据列表可直接供 deal_not_excel 函数使用
    '''


    req = requests.Session()    # 使用会话维持HTTP状态

    # 进去登录页面需要携带Cookies，该Cookie为固定从文件获取，持续更新，从登录界面获取后续登录需要post的数据
    cookie_file = os.path.join(BASE_DIR, 'app/DBexcel/cookies.txt')
    cookie = cookiejar.LWPCookieJar(filename=cookie_file)
    try:
        cookie.load()
        req.cookies = cookie
        res = req.get('http://wzsqis.wistron.com/Logon/')
    except exceptions.Timeout as e:
        raise('get login page failed ', e)
    except exceptions.HTTPError as e:
        raise('get login page failed ', e)

    if res.status_code == 200:
        cookie.save(ignore_expires=True, ignore_discard=True)
    else:
        print('login page request failed with status code: %s' % res.status_code)


    soup = BeautifulSoup(res.text, 'lxml')
    view_state = soup.find('input', id='__VIEWSTATE').attrs['value']
    view_state_generator = soup.find('input', id='__VIEWSTATEGENERATOR').attrs['value']
    event_validation = soup.find('input', id='__EVENTVALIDATION').attrs['value']

    # 模拟登录
    login_params = {
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': view_state_generator,
        '__EVENTVALIDATION': event_validation,
        'txtUserID': username,
        'txtPassword': password,
        'cmdLogin': '登录',
        'dropLanguage': 'zh-CHS',
    }
    login_url = 'http://wzsqis.wistron.com/Logon/Login.aspx'
    try:
        res = req.post(login_url, data=login_params)    # 登录一次记录用户登录状态
    except exceptions.Timeout as e:
        raise('login failed ', e)
    except exceptions.HTTPError as e:
        raise('login failed ', e)
    finally:
        if res.status_code != 200:
            print('login failed with status code: %s' % res.status_code)

    # 后续的请求都是用这个url
    data_url = 'http://wzsqis.wistron.com/AEMS_MIAEMS019/MIAEMS019.aspx?APID=MIAEMS019&APID=MIAEMS019'

    # 进入查询页面并更新查询请求要提交的数据
    try:
        res = req.get(data_url)
    except exceptions.Timeout as e:
        raise('get search page fialed ', e)
    except exceptions.HTTPError as e:
        raise('get search page fialed ', e)
    finally:
        if res.status_code != 200:
            print('get search page fialed with status code: %s' % res.status_code)

    soup = BeautifulSoup(res.text, 'lxml')
    view_state = soup.find('input', id='__VIEWSTATE').attrs['value']
    view_state_generator = soup.find('input', id='__VIEWSTATEGENERATOR').attrs['value']
    event_validation = soup.find('input', id='__EVENTVALIDATION').attrs['value']

    # 查询请求并更新最终请求要提交的数据
    if not ddate:
        ddate = date.today() - timedelta(days=1)
    ddate = ddate.strftime('%Y/%m/%d')
    data_params = {
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': view_state_generator,
        '__EVENTVALIDATION': event_validation,
        'lstTab': 0,
        'drpPlant': plantcode,
        'txtDateTimeStart': ddate + ' 00:00:00',
        'txtDateTimeEnd': ddate + ' 23:59:59',
        'BtnQuery': '查询',
    }

    try:
        res = req.post(data_url, data=data_params)
    except exceptions.Timeout as e:
        raise('get datas fialed ', e)
    except exceptions.HTTPError as e:
        raise('get datas fialed ', e)
    finally:
        if res.status_code != 200:
            print('get datas fialed with status code: %s' % res.status_code)

    soup = BeautifulSoup(res.text, 'lxml')
    view_state = soup.find('input', id='__VIEWSTATE').attrs['value']
    view_state_generator = soup.find('input', id='__VIEWSTATEGENERATOR').attrs['value']
    event_validation = soup.find('input', id='__EVENTVALIDATION').attrs['value']

    # 下载所有数据请求（最终）
    data_params = {
        '__EVENTTARGET': 'PageDropDownList',
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': view_state_generator,
        '__EVENTVALIDATION': event_validation,
        'lstTab': 1,
        'drpPageSize': 10,
        'PageDropDownList': 3,
        'btndlexl': 'Download To Excel',
    }
    try:
        res = req.post(data_url, data=data_params)
    except exceptions as e:
        raise e
    if res.status_code != 200:
        print('get all fialed with status code: %s' % res.status_code)
        return

    content = res.text.strip().replace('\ufeff', '')
    soup = BeautifulSoup(content, 'lxml')
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")

    # 写入excel文件
    # 写入excel文件
    filepath = os.path.join(BASE_DIR, filepath)
    filename = os.path.join(filepath, plantcode + '_' + ddate.replace('/', '') + '.xlsx')
    wb = Workbook()
    ws = wb.create_sheet(plantcode, 0)

    for row in range(len(rows)):
        cols = rows[row].findAll(['td', 'th'])
        new_col = []
        for col in cols:
            new_col.append(col.getText())
        if row == 0:
            new_col.append('PlantCode')
        else:
            new_col.append(plantcode)
        ws.append(new_col)

    wb.save(filename)

# ddate = date.today() - timedelta(days=2)
# content = crawl_data('Z19033008','Cdw3623282','F136', '.', ddate)
