# encoding=utf-8

import sys
import datetime
import telnetlib
from ftplib import FTP
import pymysql

FTP_SERVER = {'ip': '192.90.33.235',
              'port': 21,
              'user': 'bknetcfg',
              'passwd': 'bknetcfg',
              'bak_dir': ''}

DB_SERVER = {'host': '192.90.33.212',
             'port': 3306,
             'user': 'chknet',
             'password': 'chknet',
             'db': 'chknet',
             'charset': 'utf8mb4',
             'cursorclass': pymysql.cursors.DictCursor}




def mk_bak_dir_on_ftp(ftp_server, bak_dir):
    print(sys._getframe().f_code.co_name)

    ftp = FTP()
    try:
        ftp.connect(ftp_server['ip'], ftp_server['port'])
    except:
        print("Can not connect server " + ftp_server['ip'] + "!")
        exit(3)
    try:
        ftp.login(ftp_server['user'],ftp_server['passwd'])
    except:
        print("Can not login server " + ftp_server['ip'] + "!")
        exit(3)

    try:
        ftp.mkd(bak_dir)
    except:
        print("Can no create directory " + bak_dir + " on server " + ftp_server['ip'] + "!")
        ftp.quit()
        exit(3)
    print(ftp.dir())
    print("Create directory " + ftp_server + " on server " + ftp_server['ip'] + "success!")
    ftp.quit()

    return


def get_devices(db_server):
    print(sys._getframe().f_code.co_name)

    conn = pymysql.connect(**db_server)
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT vendor, type, name, ipaddr, user, passwd, supasswd FROM cn_device'
            cursor.execute(sql)
            result = cursor.fetchall()

        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        conn.commit()
    finally:
        conn.close()
        return result

def bak_csc_r38_cfg(device, ftp_server):
    print("bak_csc_r38_cfg: " + device['name'], device['ipaddr'], device['user'], device['passwd'], device['supasswd'])

def bak_h3c_s75_cfg(device, ftp_server):
    print("bak_h3c_s75_cfg: " + device['name'], device['ipaddr'], device['user'], device['passwd'], device['supasswd'])

def bak_h3c_s31_cfg(device, ftp_server):
    print("Begin to backup " + device['name'] + "(" + device['ipaddr'] + ")'s config to ftp://" \
          + ftp_server['ip'] + '/' + ftp_server['bak_dir'] + '...')
    try:
        tn = telnetlib.Telnet(device['ip'])
        tn.set_debuglevel(2)
        try:
            tn.read_until(b"(?i)Username:", timeout=10)
        except EOFError:
            print("time out")
        tn.write(device['user']+b"\n")
        tn.read_until(b"Password:", timeout=2)
        tn.write(device['passwd']+b"\n")
        tn.read_until(b">", timeout=2)
        #tn.write(host['tftp']+b"\n")
        #tn.read_until(b"successfully", timeout=6)
        # movefile_txt(name, ip, area)
    except TimeoutError:
        print(device['name'] + "(" + device['ip'] + ") TimeoutError: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。")
    except FileNotFoundError:
        print(device['name'] + "(" + device['ip'] + ") FileNotFoundError: 未成功备份startup.cfg！")
    except ConnectionResetError:
        print(device['name'] + "(" + device['ip'] + ") ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。")
    except:
        print(device['name'] + "(" + device['ip'] + ") 发生未知错误！")

    print("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config to ftp://" \
          + ftp_server['ip'] + '/' + ftp_server['bak_dir'] + 'successful.')
'''def bak_dev_cfg(device):
    print(device['vendor'], device['type'], device['name'], device['ipaddr'], device['user'], device['passwd'], device['supasswd'])
    #eval("bak_" + device['vendor'] + "_" + device['type'] + "_cfg")\
    # (device['name'], device['ipaddr'], device['user'], device['passwd'], device['supasswd'])
    #eval("bak_" + device['vendor'] + "_" + device['type'] + "_cfg")(device)
'''
if __name__ == '__main__':

    bat_no = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    #ftp_server = mk_ftp_dir(FTP_SERVER, bat_no)
    FTP_SERVER['bak_dir'] = bat_no
    devices = get_devices(DB_SERVER)
    for device in devices:
        #bak_dev_cfg(device)
        #eval("bak_" + device['vendor'] + "_" + device['type'] + "_cfg")(device,FTP_SERVER)
