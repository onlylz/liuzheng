# coding: utf8
import sys
import telnetlib
import time
import pymysql
import os
import shutil
import logging
import paramiko

def bk_telnet_h3c_1(name, ip, area):
    host = {}
    host['name'] = name.encode(encoding="utf-8")
    host['ip'] = ip.encode(encoding="utf-8")
    host['user'] = b"liuzheng"
    host['password'] = b"jjyhncfh"
    host['tftp'] = b"tftp 99.99.11.11 put startup.cfg config.txt"
    try:
        tn = telnetlib.Telnet(host['ip'])
        tn.set_debuglevel(2)
        try:
            tn.read_until(b"(?i)Psername:", timeout=10)
        except EOFError:
            logging.error("time out")
        tn.write(host['user']+b"\n")
        tn.read_until(b"Password:", timeout=2)
        tn.write(host['password']+b"\n")
        tn.read_until(b">", timeout=2)
        tn.write(host['tftp']+b"\n")
        tn.read_until(b"successfully", timeout=6)
        # movefile_txt(name, ip, area)
    except TimeoutError:
        logging.warning(name + "(" + ip + ") TimeoutError: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。")
    except FileNotFoundError:
        logging.error(name + "(" + ip + ") FileNotFoundError: 未成功备份startup.cfg！")
    except ConnectionResetError:
        logging.warning(name + "(" + ip + ") ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。")
    except:
        logging.error(name + "(" + ip + ") 发生未知错误！")


file_year = time.strftime("%Y", time.localtime())
file_mon = time.strftime("%m", time.localtime())
file_mday = time.strftime("%d", time.localtime())
file_time = time.strftime("%Y%m%d", time.localtime())
backup_dir = os.getcwd() + "\\备份路径\\"
tftp_dir = os.getcwd() + "\\TFTP\\Root\\"
logging_dir = os.getcwd() + "\\备份路径\\备份程序执行日志"
logging_name = "log_" + file_time + ".txt"
if not os.path.isdir(logging_dir):
    os.makedirs(logging_dir)
logging.basicConfig(filename = os.path.join(logging_dir, logging_name), level = logging.INFO, filemode = "a", format = "%(asctime)s - %(levelname)s: %(message)s")
#logging.debug("debug")
#logging.info("info")
#logging.warning("warn")
#logging.error("error")
bk_telnet_h3c_1("11F","99.99.11.1","11")
logging.shutdown()