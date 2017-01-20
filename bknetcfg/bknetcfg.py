#!/usr/local/bin/python
# encoding=utf-8

import sys
import datetime
import telnetlib
from ftplib import FTP
#import pymysql
import logging
from mylogging import setup_logging
import socket
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

FTP_SERVER = {'ip': '192.90.33.235',
              'port': 21,
              'user': 'bknetcfg',
              'passwd': 'bknetcfg',
              'bak_dir': '/'}

# DB_SERVER = {'host': '192.90.33.212',
#              'port': 3306,
#              'user': 'chknet',
#              'password': 'chknet',
#              'db': 'chknet',
#              'charset': 'utf8mb4',
#              'cursorclass': pymysql.cursors.DictCursor}


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
    return 0

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
            cursor.execute(sql, '1 ')
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

def get_cmds(db_server, group_name):
    # print(sys._getframe().f_code.co_name)
    logger.info("Begin to get commands from DB server...")
    try:
        conn = pymysql.connect(**db_server)
    except:
        logger.error("Can not connect to DB server " + DB_SERVER['host'] + "!")
    result = []
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT c.seq_in_group, c.prompt, c.command FROM cn_cmd_group g, cn_cmd c WHERE g.group_name= % s AND c.group_id=g.id ORDER BY c.seq_in_group'
            cursor.execute(sql, group_name)
            result = cursor.fetchall()

            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            # conn.commit()
            #
    except:
        logger.error("Can not get any commands to execute from DB server!")
    finally:
        conn.close()
        logger.info("Get " + str(len(result)) + " commands to execute from DB server.")
        return result

def send_sms(content):

    h = '000000006008'
    t = str(datetime.datetime.strftime(datetime.datetime.now(), '%m-%d %H:%M'))
    header = h + t
    c = header + " " + content
    print(c)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('dxpt.com', 8888))
    sock.send(c.encode("utf-8"))
    sock.close()

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

def bak_trx_cfg(device, ftp_server):
    # print("Begin to backup FW_EXT's config ...")
    # try:
    #     tn = telnetlib.Telnet('192.90.254.77')
    #     tn.set_debuglevel(2)
    # except:
    #     print("FW_EXT无法连接")
    #     print("Backup FW_EXT's config failure")
    #
    # try:
    #     tn.read_until(b"login:")
    #     tn.write(b"superman\n")
    #     tn.read_until(b"Password:")
    #     tn.write(b"talent\n")
    #     tn.read_until(b"#")
    #     tn.write(b"show nostop\n")
    #     config = tn.read_until(b"#")
    #     tn.close()
    #     print("Get FW_EXT's config successful.")
    #
    # except:
    #     print("Encounter error when backuping FW_EXT's config")
    #     print("Backup FW_EXT's config failure")


    logger.info("Begin to backup " + device['name'] + "(" + device['ipaddr'] + ")'s config ...")
    try:
        tn = telnetlib.Telnet(device['ipaddr'])
        tn.set_debuglevel(2)
    except:
        logger.error("Can not connect to " + device['name'] + "(" + device['ipaddr'] + "）!")
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

    try:
        tn.read_until(b"login:")
        tn.write(device['user'].encode('utf-8') + b"\n")
        tn.read_until(b"Password:")
        tn.write(device['passwd'].encode('utf-8') + b"\n")
        tn.read_until(b"#")
        tn.write(b"show nostop\n")
        config = tn.read_until(b"#")
        tn.close()
        logger.info("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config successful.")

    except:
        logger.error("Encounter error when backuping " + device['name'])
        logger.error("Backup " + device['name'] + "(" + device['ipaddr'] + ")'s config failure!")
        return 0

    fn = device['name'] + datetime.datetime.now().strftime('%Y%m%d') + ".cfg"
    print(fn)
    f = open(fn, 'w')
    try:
        f.write(config.decode(encoding='gb2312', errors='ignore'))
    finally:
        f.close()

    logger.info("Begin to upload FW's config to FTP server ...")
    ftp = FTP()
    cmd1 = "cd " + ftp_server['bak_dir']
    cmd2 = "put " + fn

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
        ftp.cwd(ftp_server['bak_dir'])
        fp = open(fn, 'rb')
        ftp.storbinary('STOR '+fn, fp)

    except:
        logger.error("Can not upload to  FTP server " + ftp_server['ip'] + "!")
        ftp.quit()
        exit(3)
    logger.info("Upload FW's config on FTP server " + ftp_server['ip'] + " success!")
    ftp.quit()
    fp.close()
    return 1


def r_exec(device, cmds):
    logger.info("Begin to execute commands on " + device['name'] + "(" + device['ipaddr'] + "...")
    try:
        tn = telnetlib.Telnet(device['ipaddr'])
        tn.set_debuglevel(2)
    except:
        logger.error("Can not connect to " + device['name'] + "(" + device['ipaddr'] + ")!")
        logger.error("Execute commands on " + device['name'] + "(" + device['ipaddr'] + ") failure!")
        return 0

    try:
        for cmd in cmds:
            print(cmd)
            print(cmd['prompt'].encode('utf-8'))
            logger.debug(tn.read_until(eval(cmd['prompt'])))
            tn.write((eval(cmd['command'])))
        tn.close()
        logger.info("Execute commands on " + device['name'] + "(" + device['ipaddr'] + ") successful.")
        return 1
    except:
        logger.error("Encounter errors when executing commands on " + device['name'] + "!")
        logger.error("Execute commands on " + device['name'] + "(" + device['ipaddr'] + ") failure!")
        return 0


if __name__ == '__main__':

    setup_logging()
    logger = logging.getLogger(__name__)
    bat_no = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    logger.info("***Begin to backup network device's config to FTP...")
    if mk_bak_dir_on_ftp(FTP_SERVER, bat_no) == 0:
        FTP_SERVER['bak_dir'] = bat_no
    else:
        FTP_SERVER['bak_dir'] = '/'
    '********备份网络设备'
    # devices = get_devices(DB_SERVER)
    # backed_devices = 0
    #
    # for device in devices:
    #     #backed_devices = backed_devices + eval("bak_" + device['vendor'] + "_" + device['sw_ver'] + "_cfg")(device, FTP_SERVER)
    #     group_name = "bak_" + device['vendor'] + "_" + device['sw_ver'] + "_cfg"
    #     cmds = get_cmds(DB_SERVER, group_name)
    #     backed_devices = backed_devices + r_exec(device, cmds)
    # content = str(backed_devices) + "/" + str(len(devices)) + "设备配置已备份至ftp://" + \
    #       FTP_SERVER['ip'] + '/' + FTP_SERVER['bak_dir'] + "."
    # logger.info(content)
    # send_sms(content)

    '********备份天融信防火墙'

    logger.info("***Begin to backup FW's config to FTP...")
    fws = [{'name':'NC_EXT_F40_001',
             'ipaddr': '192.90.254.77',
             'user': 'superman',
             'passwd': 'talent'},
           {'name': 'NC_SS_F40_001',
            'ipaddr': '192.90.254.109',
            'user': 'superman',
            'passwd': 'talent'}]

    backed_fws = 0
    for fw in fws:
        backed_fws = backed_fws + bak_trx_cfg(fw,FTP_SERVER)
    content = str(backed_fws) + "/" + str(len(fws)) + "防火墙配置已备份至ftp://" + \
              FTP_SERVER['ip'] + '/' + FTP_SERVER['bak_dir'] + "."
    logger.info(content)
    send_sms(content)




