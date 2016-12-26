# encoding=utf-8

import sys
import datetime
import paramiko
from ftplib import FTP
import pymysql

FTP_SERVER = {'ip': '192.90.33.235',
              'port': 21,
              'user': 'bknetcfg',
              'passwd': 'bknetcfg'}

DB_SERVER = {'host': '192.90.33.212',
             'port': 3306,
             'user': 'chknet',
             'password': 'chknet',
             'db': 'chknet',
             'charset': 'utf8mb4',
             'cursorclass': pymysql.cursors.DictCursor}




def mk_ftp_dir(host, dir):
    #print(sys._getframe().f_code.co_name)

    ftp = FTP()
    try:
        ftp.connect(host['ip'], host['port'])
    except:
        print("Can not connect server " + host['ip'] + "!")
        exit(3)
    try:
        ftp.login(host['user'],host['passwd'])
    except:
        print("Can not login server " + host['ip'] + "!")
        exit(3)

    try:
        ftp.mkd(dir)
    except:
        print("Can no create directory " + "dir" + " on server " + host['ip'] + "!")
        ftp.quit()
        exit(3)
    print(ftp.dir())
    print("Create directory " + "dir" + " on server " + host['ip'] + "success!")
    ftp.quit()


def get_devices(db_host):
    conn = pymysql.connect(**db_host)

        # 执行sql语句
    try:
        with conn.cursor() as cursor:
            # 执行sql语句，进行查询
            sql = 'SELECT vendor, type, name, ipaddr, user, passwd, supasswd FROM cn_device'
            cursor.execute(sql)
            # 获取查询结果
            result = cursor.fetchall()
            #print(result)
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        conn.commit()

    finally:
        conn.close()
        return result




    print(sys._getframe().f_code.co_name)


def bak_csc_r38_cfg(name, ip, user, passwd, supasswd):
    print("bak_csc_r38_cfg: " + name + ip + user + passwd + supasswd)


def bak_h3c_s75_cfg(name, ip, user, passwd, supasswd):
    print("bak_h3c_s75_cfg: " + name + ip + user + passwd + supasswd)


def bak_dev_cfg(device):

    print(device['vendor'], device['type'], device['name'], device['ipaddr'], device['user'], device['passwd'], device['supasswd'])
    #eval("bak_" + vendor + "_" + type + "_cfg")(name, ipaddr, user, passwd, supasswd)


if __name__ == '__main__':

    bat_no = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    dir = bat_no
    #mk_ftp_dir(FTP_SERVER, dir)
    devices = get_devices(DB_SERVER)

    #print(hosts)
    # hosts = (('h3c', 's75', 'core1', '192.90.33.1', 'liuzheng', 'jjyhncfh', 'ncfhjjyh'),
    #         ('csc', 'r38', 'r1', '192.90.33.2', 'liuzheng', 'jjyhncfh', 'ncfhjjyh'))


    for device in devices:
        bak_dev_cfg(device)
