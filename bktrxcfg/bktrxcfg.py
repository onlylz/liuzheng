#!/usr/local/bin/python
# encoding=utf-8
import telnetlib
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#适用于天融信防火墙

print("Begin to backup FW_EXT's config ...")
try:
    tn = telnetlib.Telnet('192.90.254.77')
    tn.set_debuglevel(2)
except:
    print("FW_EXT无法连接")
    print("Backup FW_EXT's config failure")


try:
    tn.read_until(b"login:")
    tn.write(b"superman\n")
    tn.read_until(b"Password:")
    tn.write(b"talent\n")
    tn.read_until(b"#")
    tn.write(b"show nostop\n")
    config = tn.read_until(b"#")
    tn.close()
    print("Get FW_EXT's config successful.")

except:
    print("Encounter error when backuping FW_EXT's config")
    print("Backup FW_EXT's config failure")

fn = "FW_EXT_"+datetime.datetime.now().strftime('%Y%m%d')+".cfg"
f = open(fn,'w')
try:
    f.write(config.decode(encoding='gb2312',errors='ignore'))
finally:
    f.close()
print(config.decode(encoding='gb2312',errors='ignore'))

