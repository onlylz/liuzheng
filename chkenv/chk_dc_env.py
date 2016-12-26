#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import pymssql
import socket
import codecs


host = "192.90.33.180"
user = "sa"
pwd =  ""
db = "myserver"
tab = 'his'+ datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')

try:
    conn = pymssql.connect(host=host,user=user,password=pwd, database=db,charset='utf8')
except pymssql.OperationalError as msg:
    
    print('无法连接数据库！'.decode('utf-8').encode('gbk'))
    sys.exit()
else:
    print('连接数据库成功！'.decode('utf-8').encode('gbk'))
    cur = conn.cursor()
    sql = "Exec  sp_get_dc_env %s"
    cur.execute(sql, (tab))
    result = cur.fetchall()
    cur.close()
    conn.close()
    print('数据库已断开！'.decode('utf-8').encode('gbk'))

    content='000000006008'+str(datetime.datetime.strftime(datetime.datetime.now(),'%m-%d %H:%M'))+' '
    for r in result:
        
        content=content + r[0].encode('Latin1').decode('gbk') + r[1].encode('Latin1').decode('gbk') + ' ' + r[2].encode('Latin1').decode('gbk')+' '

    print content
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('dxpt.com', 8888))
    sock.send(content)
    sock.close()
