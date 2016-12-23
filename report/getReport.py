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

BASEURL = 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi'
REPORTURL = '''http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-102-对私存款开销户明细表']&ui.name=DPSIT-D-102-对私存款开销户明细表&run.outputFormat=&run.prompt=true&ui.backURL=/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463'''

#######第一次请求，登录
url0 = 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&gohome='
url1 = 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi'
headers0 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Host': '10.115.4.2:8080',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
s = requests.session()
response0 = s.get(url0, headers=headers0)
#CID1 = r.headers['Content-ID']
cookie0 = response0.headers['Set-Cookie']
#print('CID1:' + CID1)
#print('cookie1:' + cookie1)
headers1 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Content-Length': '109',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Cookie': cookie0,
           'Host': '10.115.4.2:8080',
           'Origin': 'http://10.115.4.2:8080',
           'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
form1 = {'encoding': 'UTF-8',
        'm': 'portal/main.xts',
        'CAMUsername': '00630',
        'CAMPassword': '123456',
        'h_CAM_action': 'logonAs',
        'CAMNamespace': 'DAS'}

#

response1 = s.post(url=url1, headers=headers1, data=form1)
#print"1---------------------------------------------------------------"
#print(response1.content)
#CID2 = r.headers['Content-ID']
cookie1 = response1.headers['Set-Cookie']
#print('CID2:' + CID2)
#print('cookie1:' + cookie1)
#print(r.content)

#第二次请求
#url2 = '''http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-101-定期储蓄提前支取明细日报表']&ui.name=DPSIT-D-101-定期储蓄提前支取明细日报表&run.outputFormat=&run.prompt=true&ui.backURL=/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463'''
url2 = '''http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-102-对私存款开销户明细表']&ui.name=DPSIT-D-102-对私存款开销户明细表&run.outputFormat=&run.prompt=true&ui.backURL=/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463'''
headers2 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cookie': cookie1,
           'Host': '10.115.4.2:8080',
           'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

response2 = s.post(url=url2, headers=headers2)
cookie2 = response2.headers['Set-Cookie']
#print"2----------------------------------------"
#print(response2.content)
#soup = BeautifulSoup(r.content, "html.parser")
pattern2 = re.compile(r"\"status\":(.*?), \"conversation\":(.*?), \"tracking\":(.*?), \"secondaryRequests\":(.*?), \"caf\":(.*?), \"outputFormat\":(.*?), \"parameters\":(.*?), \"action_state\":(.*?), \"primary_action\":(.*?)}", re.S)
rs = pattern2.search(response2.content)
actionState = rs.group(8).strip().strip('"')
executionParameters = rs.group(7).strip().strip('"')
conversation = rs.group(2).strip().strip('"')
tracking = rs.group(3).strip().strip('"')
cafcontextid = rs.group(5).strip().strip('"')

headers3 = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '5612',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie1,
            'Host': '10.115.4.2:8080',
            'Origin': 'http://10.115.4.2:8080',
            'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27%e8%80%83%e6%a0%b8%e6%8a%a5%e8%a1%a8%27%5d%2ffolder%5b%40name%3d%27%e5%ad%98%e6%ac%be%e7%b1%bb%e6%8a%a5%e8%a1%a8%27%5d%2freport%5b%40name%3d%27DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8%27%5d&ui.name=DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8&run.outputFormat=&run.prompt=true&ui.backURL=%2fibmcognos%2fcgi-bin%2fcognos.cgi%3fb_action%3dxts.run%26m%3dportal%2fcc.xts%26m_folder%3di2591F57F785F44C8A63442B4672A2463',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

form3 = {'cv.ignoreState': 'true',
         'b_action': 'cognosViewer',
         'cv.id': '_NS_',
         'cv.actionState': 'actionState',
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
         'p_p_branch_code': '<selectChoices><selectOption useValue="78300" displayValue="78300"/></selectChoices>',
         'ui.cafcontextid': cafcontextid,
         'cv.catchLogOnFault': 'true',
         'cv.responseFormat': 'data'}
response3 = s.post(url=url1, headers=headers3, data=form3)
#print"3------------------------------------------------#"
#print(response3.content)
soup = BeautifulSoup(response3.content, "html.parser")
pattern3 = re.compile(r"\"conversation\":(.*?), \"tracking\":(.*?), \"secondaryRequests\":(.*?), \"caf\":(.*?), \"outputFormat\":(.*?), \"parameters\":(.*?), \"action_state\":(.*?), \"primary_action\":(.*?)}", re.S)
rs = pattern3.search(str(soup.xml.state.prettify()))

actionState = rs.group(7).strip().strip('"')
executionParameters = rs.group(6).strip().strip('"')
conversation = rs.group(1).strip().strip('"')
tracking = rs.group(2).strip().strip('"')
cafcontextid = rs.group(4).strip().strip('"')



#print executionParameters
#print conversation
#print tracking
#print cafcontextid
headers4 = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '6053',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie1,
            'Host': '10.115.4.2:8080',
            'Origin': 'http://10.115.4.2:8080',
            'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27%e8%80%83%e6%a0%b8%e6%8a%a5%e8%a1%a8%27%5d%2ffolder%5b%40name%3d%27%e5%ad%98%e6%ac%be%e7%b1%bb%e6%8a%a5%e8%a1%a8%27%5d%2freport%5b%40name%3d%27DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8%27%5d&ui.name=DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8&run.outputFormat=&run.prompt=true&ui.backURL=%2fibmcognos%2fcgi-bin%2fcognos.cgi%3fb_action%3dxts.run%26m%3dportal%2fcc.xts%26m_folder%3di2591F57F785F44C8A63442B4672A2463',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/53'}

form4 = {'cv.ignoreState': 'true',
         'b_action': 'cognosViewer',
         'cv.id' :'_NS_',
         'cv.actionState': actionState,
         'ui.action': 'forward',
         'ui.object': '''/content/folder[@name='考核报表']/folder[@name='存款类报表']/report[@name='DPSIT-D-102-对私存款开销户明细表']''',
         'ui.primaryAction':'run',
         'errURL': '/ibmcognos/cgi-bin/cognos.cgi?b_action=xts.run&m=portal/cc.xts&m_folder=i2591F57F785F44C8A63442B4672A2463',
         'ui.objectClass': 'report',
         'executionParameters': executionParameters,
         '_promptControl': 'prompt',
         'run.prompt': 'true',
         'ui.conversation': conversation,
         'm_tracking': tracking,
         'p_p_date_8': '<selectChoices><selectOption useValue="20160505" displayValue="20160505"/></selectChoices>',
         'ui.cafcontextid': cafcontextid,
         'cv.catchLogOnFault':'true',
         'cv.responseFormat':'data'}
response4 = s.post(url=url1, headers=headers4, data=form4)
print '4-----------------------------------------------------------'
print(response4.content)


soup = BeautifulSoup(response4.content, "html.parser")
pattern4 = re.compile(r"\"conversation\":(.*?), \"tracking\":(.*?), \"secondaryRequests\":(.*?), \"caf\":(.*?), \"outputFormat\":(.*?), \"parameters\":(.*?), \"action_state\":(.*?), \"primary_action\":(.*?)}", re.S)
rs = pattern4.search(str(soup.xml.state.prettify()))

actionState = rs.group(7).strip().strip('"')
executionParameters = rs.group(6).strip().strip('"')
conversation = rs.group(1).strip().strip('"')
tracking = rs.group(2).strip().strip('"')
cafcontextid = rs.group(4).strip().strip('"')



#print executionParameters
#print conversation
#print tracking
#print cafcontextid
headers5 = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '5954',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie1,
            'Host': '10.115.4.2:8080',
            'Origin': 'http://10.115.4.2:8080',
            'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27%e8%80%83%e6%a0%b8%e6%8a%a5%e8%a1%a8%27%5d%2ffolder%5b%40name%3d%27%e5%ad%98%e6%ac%be%e7%b1%bb%e6%8a%a5%e8%a1%a8%27%5d%2freport%5b%40name%3d%27DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8%27%5d&ui.name=DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8&run.outputFormat=&run.prompt=true&ui.backURL=%2fibmcognos%2fcgi-bin%2fcognos.cgi%3fb_action%3dxts.run%26m%3dportal%2fcc.xts%26m_folder%3di2591F57F785F44C8A63442B4672A2463',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/53'}
form5 = {'cv.ignoreState': 'true',
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
         'cv.catchLogOnFault':'true',
         'cv.responseFormat':'data'}



response5 = s.post(url=url1, headers=headers5, data=form5)
print '5-----------------------------------------------------------'
#print(response5.content)
print "#------------------------------------------------------------------------------------------"

soup = BeautifulSoup(response5.content, "html.parser")
pattern5 = re.compile(r"\"conversation\":(.*?), \"tracking\":(.*?), \"secondaryRequests\":(.*?), \"caf\":(.*?), \"outputFormat\":(.*?), \"parameters\":(.*?), \"action_state\":(.*?), \"primary_action\":(.*?)}", re.S)
rs = pattern5.search(str(soup.xml.state.prettify()))


while re.search(r"nextPage",rs.group(3).strip()):
    actionState = rs.group(7).strip().strip('"')
    executionParameters = rs.group(6).strip().strip('"')
    conversation = rs.group(1).strip().strip('"')
    tracking = rs.group(2).strip().strip('"')
    cafcontextid = rs.group(4).strip().strip('"')
    headers = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '4323',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie1,
            'Host': '10.115.4.2:8080',
            'Origin': 'http://10.115.4.2:8080',
            'Referer': 'http://10.115.4.2:8080/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27%e8%80%83%e6%a0%b8%e6%8a%a5%e8%a1%a8%27%5d%2ffolder%5b%40name%3d%27%e5%ad%98%e6%ac%be%e7%b1%bb%e6%8a%a5%e8%a1%a8%27%5d%2freport%5b%40name%3d%27DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8%27%5d&ui.name=DPSIT-D-102-%e5%af%b9%e7%a7%81%e5%ad%98%e6%ac%be%e5%bc%80%e9%94%80%e6%88%b7%e6%98%8e%e7%bb%86%e8%a1%a8&run.outputFormat=&run.prompt=true&ui.backURL=%2fibmcognos%2fcgi-bin%2fcognos.cgi%3fb_action%3dxts.run%26m%3dportal%2fcc.xts%26m_folder%3di2591F57F785F44C8A63442B4672A2463',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/53'}

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

    response = s.post(url=url1, headers=headers, data=form)
    #print response.content
    print '*-----------------------------------------------------------'
    soup = BeautifulSoup(response.content, "html.parser")
    pattern = re.compile(r"\"conversation\":(.*?), \"tracking\":(.*?), \"secondaryRequests\":(.*?), \"caf\":(.*?), \"outputFormat\":(.*?), \"parameters\":(.*?), \"action_state\":(.*?), \"primary_action\":(.*?)}", re.S)
    rs = pattern.search(str(soup.xml.state.prettify()))
print "end"


