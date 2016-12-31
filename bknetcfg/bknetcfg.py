#!/usr/local/bin/python
# encoding=utf-8

import sys
import datetime
import telnetlib
from ftplib import FTP
import pymysql
import logging
from mylogging import setup_logging

FTP_SERVER = {'ip': '192.90.33.235',
              'port': 21,
              'user': 'bknetcfg',
              'passwd': 'bknetcfg',
              'bak_dir': '/'}

DB_SERVER = {'host': '192.90.33.212',
             'port': 3306,
             'user': 'chknet',
             'password': 'chknet',
             'db': 'chknet',
             'charset': 'utf8mb4',
             'cursorclass': pymysql.cursors.DictCursor}


def mk_bak_dir_on_ftp(ftp_server, bak_dir):
    #print(sys._getframe().f_code.co_name)

    logger.info("Begin to create directory on FTP server for backup...")
    ftp = FTP()
    try:
        ftp.connect(ftp_server['ip'], ftp_server['port'])
    except:
        logger.error("Can not connect FTP server " + ftp_server['ip'] + "!")
        exit(3)
    try:
        ftp.login(ftp_server['user'], ftp_server['passwd'])
    except:
        logger.error("Can not login FTP server " + ftp_server['ip'] + "!")
        exit(3)

    try:
        ftp.mkd(bak_dir)
    except:
        logger.error("Can not create directory " + bak_dir + " on FTP server " + ftp_server['ip'] + "!")
        ftp.quit()
        exit(3)
    logger.info("Create directory " + bak_dir + " on FTP server " + ftp_server['ip'] + " success!")
    ftp.quit()
    return

def get_devices(db_server):
    #print(sys._getframe().f_code.co_name)
    logger.info("Begin to get network device's parameter from DB server...")
    try:
        conn = pymysql.connect(**db_server)
    except:
        logger.error("Can not connect to DB server " + DB_SERVER['host'] + "!")
    result=[]
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT vendor, sw_ver, name, hostname, ipaddr, user, passwd, supasswd FROM cn_device WHERE bak_cfg = % s ORDER BY hostname'
            cursor.execute(sql, '1')
            result = cursor.fetchall()

        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        #conn.commit()
        #
    except:
        logger.error("Can not get network device's parameter from DB server!")
    finally:
        conn.close()
        logger.info("Get " + str(len(result)) + " network device's parameter from DB server.")
        return result

def bak_H3C_Sv5_cfg(device, ftp_server):
    #适用于S3100、S3100v2
    #print(sys._getframe().f_code.co_name)
    logger.info("Begin to backup " + device['name'] + "(" + device['ipaddr'] + ")'s config ...")
    try:
        tn = telnetlib.Telnet(device['ipaddr'])
        tn.set_debuglevel(2)
    except:
        logger.error("Can not connect to " + device['name'] + "(" + device['ipaddr'] + ")!")
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

    try:
        tn.read_until(b"Username:")
        tn.write(device['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(device['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b">")
        tn.write(b"su \n")
        tn.read_until(b"Password:")
        tn.write(device['supasswd'].encode('utf-8') + b"\n")
        tn.read_until(b">")
        tn.write(b"ftp " + ftp_server['ip'].encode('utf-8') + b"\n")
        tn.read_until(b"):")
        tn.write(ftp_server['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(ftp_server['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b"[ftp]")
        tn.write(b"cd " + ftp_server['bak_dir'].encode('utf-8') + b"\n")
        tn.read_until(b"[ftp]")
        tn.write(b"put config.cfg " + device['hostname'].encode('utf-8') + b".cfg\n")
        tn.read_until(b"[ftp]")
        tn.write(b"quit\n")
        tn.read_until(b">")
        tn.write(b"quit\n")
        tn.close()
        logger.info("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config successful.")
        return 1
    except:
        logger.error("Encounter errors when backuping " + device['name'])
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

def bak_H3C_Rv5_cfg(device, ftp_server):
    #适用S7507、R20XX、R30XX
    #print(sys._getframe().f_code.co_name)

    logger.info("Begin to backup " + device['name'] + "(" + device['ipaddr'] + ")'s config ...")
    try:
        tn = telnetlib.Telnet(device['ipaddr'])
        tn.set_debuglevel(2)
    except:
        logger.error("Can not connect to " + device['name'] + "(" + device['ipaddr'] + ")!")
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

    try:
        tn.read_until(b"Username:")
        tn.write(device['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(device['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b">")
        tn.write(b"su \n")
        tn.read_until(b"Password:")
        tn.write(device['supasswd'].encode('utf-8') + b"\n")
        tn.read_until(b">")
        tn.write(b"ftp " + ftp_server['ip'].encode('utf-8') + b"\n")
        tn.read_until(b"):")
        tn.write(ftp_server['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(ftp_server['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b"[ftp]")
        tn.write(b"cd " + ftp_server['bak_dir'].encode('utf-8') + b"\n")
        tn.read_until(b"[ftp]")
        tn.write(b"put startup.cfg " + device['hostname'].encode('utf-8') + b".cfg\n")
        tn.read_until(b"[ftp]")
        tn.write(b"quit\n")
        tn.read_until(b">")
        tn.write(b"quit\n")
        tn.close()
        logger.info("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config successful.")
        return 1
    except:
        logger.error("Encounter error when backuping " + device['name'])
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

def bak_H3C_Rv7_cfg(device, ftp_server):
    # 适用3600-28、3600-51
    #print(sys._getframe().f_code.co_name)

    logger.info("Begin to backup " + device['name'] + "(" + device['ipaddr'] + ")'s config ...")
    try:
        tn = telnetlib.Telnet(device['ipaddr'])
        tn.set_debuglevel(2)
    except:
        logger.error("Can not connect to " + device['name'] + "(" + device['ipaddr'] + ")!")
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

    try:
        tn.read_until(b"login:")
        tn.write(device['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(device['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b">")
        tn.write(b"su \n")
        tn.read_until(b"Password:")
        tn.write(device['supasswd'].encode('utf-8') + b"\n")
        tn.read_until(b">")
        tn.write(b"ftp " + ftp_server['ip'].encode('utf-8') + b"\n")
        tn.read_until(b"):")
        tn.write(ftp_server['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(ftp_server['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b"ftp>")
        tn.write(b"cd " + ftp_server['bak_dir'].encode('utf-8') + b"\n")
        tn.read_until(b"ftp>")
        tn.write(b"put startup.cfg " + device['hostname'].encode('utf-8') + b".cfg\n")
        tn.read_until(b"ftp>")
        tn.write(b"quit\n")
        tn.read_until(b">")
        tn.write(b"quit\n")
        tn.close()
        logger.info("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config successful.")
        return 1
    except:
        logger.error("Encounter error when backuping " + device['name'])
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

def bak_CSC_v12_cfg(device, ftp_server):
    # 适用3800,2900
    #print(sys._getframe().f_code.co_name)

    logger.info("Begin to backup " + device['name'] + "(" + device['ipaddr'] + ")'s config ...")
    try:
        tn = telnetlib.Telnet(device['ipaddr'])
        tn.set_debuglevel(2)
    except:
        logger.error("Can not connect to " + device['name'] + "(" + device['ipaddr'] + "）!")
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

    try:
        tn.read_until(b"Username:")
        tn.write(device['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(device['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b">")
        tn.write(b"en\n")
        tn.read_until(b"Password:")
        tn.write(device['supasswd'].encode('utf-8') + b"\n")
        tn.read_until(b"#")
        tn.write(b"copy start ftp\n")
        tn.read_until(b"]?")
        tn.write(ftp_server['ip'].encode('utf-8') + b"\n")
        tn.read_until(b"]?")
        tn.write(ftp_server['bak_dir'].encode('utf-8') +b"/" + device['hostname'].encode('utf-8') + b".cfg\n")
        tn.read_until(b"#")
        tn.write(b"exit\n")
        tn.close()
        logger.info("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config successful.")
        return 1
    except:
        logger.error("Encounter error when backuping " + device['name'])
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0



if __name__ == '__main__':

    setup_logging()
    logger = logging.getLogger(__name__)
    bat_no = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    logger.info("***Begin to backup network device's config to FTP...")
    ftp_server = mk_bak_dir_on_ftp(FTP_SERVER, bat_no)
    FTP_SERVER['bak_dir'] = bat_no
    devices = get_devices(DB_SERVER)
    backed_devices = 0
    for device in devices:
        backed_devices = backed_devices + eval("bak_" + device['vendor'] + "_" + device['sw_ver'] + "_cfg")(device, FTP_SERVER)
    logger.info("There are " + str(backed_devices) + " of " + str(len(devices)) + " devices backuped to ftp://" + \
          FTP_SERVER['ip'] + '/' + FTP_SERVER['bak_dir'] + ".")
