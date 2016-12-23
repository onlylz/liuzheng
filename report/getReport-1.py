#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import re
import logging
import requests
from httplib import HTTPConnection
from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import CData

#HTTPConnection.debuglevel = 1
#logging.basicConfig(level=logging.DEBUG)

AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
BASEURL = 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi'
PATTERN = re.compile(r"\"conversation\":(.*?), \"tracking\":(.*?), \"secondaryRequests\":(.*?), \"caf\":(.*?), \"outputFormat\":(.*?), \"parameters\":(.*?), \"action_state\":(.*?), \"primary_action\":(.*?)}", re.S)
REPORTURL = '''http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-102-对私存款开销户明细表']&ui.name=DPSIT-D-102-对私存款开销户明细表&run.outputFormat=&run.prompt=true&ui.backURL=/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463'''
DATA = '20160401'
BRANCH = '78300'

print("1.发送登录请求")
headers0 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Content-Length': '109',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Cookie': '',
           'Host': '10.115.4.2:8080',
           'Origin': 'http://10.115.4.2:8080',
           'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': AGENT}
form = {'encoding': 'UTF-8',
        'm': 'portal/main.xts',
        'CAMUsername': '00630',
        'CAMPassword': '123456',
        'h_CAM_action': 'logonAs',
        'CAMNamespace': 'DAS'}
s = requests.session()
response = s.post(url=BASEURL, headers=headers0, data=form)
print("2.请求相应报表")
#登录成功后服务器将返回cookie，将cookie加入到下一次request的header中
cookie = response.headers['Set-Cookie']
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cookie': cookie,
           'Host': '10.115.4.2:8080',
           'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': AGENT}
response = s.post(url=REPORTURL, headers=headers)
print("3.提交报表参数：机构号"+BRANCH +"，日期："+DATA)
rs = PATTERN.search(response.content)
actionState = rs.group(7).strip().strip('"')
executionParameters = rs.group(6).strip().strip('"')
conversation = rs.group(1).strip().strip('"')
tracking = rs.group(2).strip().strip('"')
cafcontextid = rs.group(4).strip().strip('"')
"""headers = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '5612',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Host': '10.115.4.2:8080',
            'Origin': 'http://10.115.4.2:8080',
            'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27%e8%80%83%e6%a0%b8%e6%8a%a5%e8%a1%a8%27%5d%2ffolder%5b%40name%3d%27%e5%ad%98%e6%ac%be%e7%b1%bb%e6%8a%a5%e8%a1%a8%27%5d%2freport%5b%40name%3d%27DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8%27%5d&ui.name=DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8&run.outputFormat=&run.prompt=true&ui.backURL=%2fibmcognos%2fcgi-bin%2fcognos.cgi%3fb_action%3dxts.run%26m%3dportal%2fcc.xts%26m_folder%3di2591F57F785F44C8A63442B4672A2463',
            'User-Agent': AGENT}
"""
form = {'cv.ignoreState': 'true',
         'b_action': 'cognosViewer',
         'cv.id': '_NS_',
         'cv.actionState': actionState,
         'ui.action': 'forward',
         'ui.object': '''/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-102-对私存款开销户明细表']''',
         'ui.primaryAction': 'run',
         'errURL': '/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463',
         'ui.objectClass': 'report',
         'executionParameters': executionParameters,
         '_promptControl': 'prompt',
         'run.prompt': 'true',
         'ui.conversation': conversation,
         'm_tracking': tracking,
         'p_p_branch_code': '<selectChoices><selectOption useValue="'+ BRANCH + '" displayValue="' + BRANCH + '"/></selectChoices>',
         'p_p_date_8': '<selectChoices><selectOption useValue="'+DATA+'" displayValue="'+DATA+'20160505"/></selectChoices>',
         'ui.cafcontextid': cafcontextid,
         'cv.catchLogOnFault': 'true',
         'cv.responseFormat': 'data'}
response = s.post(url=BASEURL, headers=headers, data=form)
"""现在开始返回xml数据，用bs解析，
   这一次response有可能没有报表数据，
   如果response的xml数据state中secondaryRequests值如果包含wait的话需要再次request
   如果response的xml数据state中secondaryRequests值如果包含nextPage的话便是报表数据，并且还有下一页的数据"""
soup = BeautifulSoup(response.content, "html.parser")
rs = PATTERN.search(str(soup.xml.state.prettify()))
"""根据secondaryRequests值中是否包含wait来判断本次回应是否包含该报表数据，
   如果包含wait的话需要再次再次发出post请求，form中的'ui.action'字段值为 'wait'"""
while re.search(r"wait", rs.group(3).strip()):
    actionState = rs.group(7).strip().strip('"')
    executionParameters = rs.group(6).strip().strip('"')
    conversation = rs.group(1).strip().strip('"')
    tracking = rs.group(2).strip().strip('"')
    cafcontextid = rs.group(4).strip().strip('"')
    """ headers = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '5954',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Host': '10.115.4.2:8080',
            'Origin': 'http://10.115.4.2:8080',
            'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27%e8%80%83%e6%a0%b8%e6%8a%a5%e8%a1%a8%27%5d%2ffolder%5b%40name%3d%27%e5%ad%98%e6%ac%be%e7%b1%bb%e6%8a%a5%e8%a1%a8%27%5d%2freport%5b%40name%3d%27DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8%27%5d&ui.name=DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8&run.outputFormat=&run.prompt=true&ui.backURL=%2fibmcognos%2fcgi-bin%2fcognos.cgi%3fb_action%3dxts.run%26m%3dportal%2fcc.xts%26m_folder%3di2591F57F785F44C8A63442B4672A2463',
            'User-Agent': AGENT}
    """
    form = {'cv.ignoreState': 'true',
            'b_action': 'cognosViewer',
            'cv.id' :'_NS_',
            'cv.actionState': actionState,
            'ui.action': 'wait',
            'ui.object': '''/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-102-对私存款开销户明细表']''',
            'ui.primaryAction':'run',
            'errURL': '/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463',
            'ui.objectClass': 'report',
            'executionParameters': executionParameters,
            'ui.conversation': conversation,
            'm_tracking': tracking,
            'ui.cafcontextid': cafcontextid,
            'cv.catchLogOnFault': 'true',
            'cv.responseFormat': 'data'}
    response = s.post(url=BASEURL, headers=headers, data=form)
    print"等待报表"
    soup = BeautifulSoup(response.content, "html.parser")
    #pattern = re.compile(r"\"conversation\":(.*?), \"tracking\":(.*?), \"secondaryRequests\":(.*?), \"caf\":(.*?), \"outputFormat\":(.*?), \"parameters\":(.*?), \"action_state\":(.*?), \"primary_action\":(.*?)}", re.S)
    rs = PATTERN.search(str(soup.xml.state.prettify()))

#如果SecondaryRequests值中不包含wait那么回应中便是报表数据，
i = int(1)
#打印网页中的报表数据
print('---接收报表第'+str(i)+'次---')
print(soup.table)
"""根据secondaryRequests值中是否包含nextPage来判断是否有下一页，
   如果存在下一页则再次发出post请求，form中的'ui.action'字段值为 'nextPage'"""
while re.search(r"nextPage", rs.group(3).strip()):
    actionState = rs.group(7).strip().strip('"')
    executionParameters = rs.group(6).strip().strip('"')
    conversation = rs.group(1).strip().strip('"')
    tracking = rs.group(2).strip().strip('"')
    cafcontextid = rs.group(4).strip().strip('"')
    """ headers = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '4323',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Host': '10.115.4.2:8080',
            'Origin': 'http://10.115.4.2:8080',
            'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27%e8%80%83%e6%a0%b8%e6%8a%a5%e8%a1%a8%27%5d%2ffolder%5b%40name%3d%27%e5%ad%98%e6%ac%be%e7%b1%bb%e6%8a%a5%e8%a1%a8%27%5d%2freport%5b%40name%3d%27DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8%27%5d&ui.name=DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8&run.outputFormat=&run.prompt=true&ui.backURL=%2fibmcognos%2fcgi-bin%2fcognos.cgi%3fb_action%3dxts.run%26m%3dportal%2fcc.xts%26m_folder%3di2591F57F785F44C8A63442B4672A2463',
            'User-Agent': AGENT}
    """
    form = {'cv.ignoreState': 'true',
         'b_action': 'cognosViewer',
         'cv.id' :'_NS_',
         'ui.action': 'nextPage',
         'ui.object': '''/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-102-对私存款开销户明细表']''',
         'ui.primaryAction':'run',
         'errURL': '/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463',
         'ui.objectClass': 'report',
         'executionParameters': executionParameters,
         'ui.conversation': conversation,
         'm_tracking': tracking,
         'ui.cafcontextid': cafcontextid,
         'cv.catchLogOnFault':'true',
         'cv.responseFormat':'data'}
    response = s.post(url=BASEURL, headers=headers, data=form)
    i = int(i)+1
    #提取secondaryRequests值用于检查是否有下一页
    soup = BeautifulSoup(response.content, "html.parser")
    rs = PATTERN.search(str(soup.xml.state.prettify()))
    #打印网页中的报表数据并打印
    print('---接收报表第'+str(i)+'次---')
    print(soup.table)
print "接收报表结束"


