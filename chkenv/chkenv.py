#coding=utf8
import pymssql
import socket
import sys
import datetime


host = "192.90.33.180"
user = "sa"
pwd =  ""
db = "myserver"
tab = 'his'+ datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')

try:
    conn = pymssql.connect(host=host,user=user,password=pwd, database=db)
except pymssql.OperationalError as msg:
    print('无法连接数据库！')
    sys.exit()
else:
    print('连接数据库成功！')
    cur = conn.cursor()
    #sql = "Exec  sp_get_dc_env %s"
    sql = "Exec  sp_chkenv %s"
    cur.execute(sql, (tab))
    result = cur.fetchall()
    cur.close()
    conn.close()
    print('数据库已断开！')
    content=['000000006008']
    content.append(datetime.datetime.strftime(datetime.datetime.now(),'%m-%d %H:%M'))
    for r in result:
        #content.append(r[0] + r[1] + ' '+ r[2] + ' '+ datetime.datetime.strftime(r[3], '%m-%d %H:%M'))
        content.append(r[0] + r[1] + ' ' + r[2]+' ')

    c=''.join(content)
    #print c
    print str(c.encode('utf-8'))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('dxpt.com', 8888))
    sock.send(str(c.encode('utf-8')))
    sock.close()
