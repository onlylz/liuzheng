#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
功能：
1.采集所有考勤机的员工信息和考勤记录并插入数据库的临时表中
2.调用数据库中的存储过程将采集到的数据插入到员工信息和考勤记录表中，并截断临时表
3.考勤机参数存放于数据库中的机器参数表，采集日志存放于log表
4.-d 参数可指定采集的天数
安装配置：
1.使用32位环境：
2、python 2.7.11 32bit
3、pywin32-220.win32-py2.7 用于调用中控SDK
4、中控SDK32bit，只能用32位，64bit在win8下试过不行。
  中控sdk的dll拷贝到c:\python27\lib
5、cx_Oracle-5.2.1-11g.win32-py2.7用于连接oracle数据库,依赖oracle客户端
6、oracle客户端32bit
数据库表结构：

存储过程：


insert into record_tmp values(seq_rec_tmp.nextval,'洪都大道','1234','1','1','2015-12-01','09:03:01','1',sysdate)

CREATE TABLE "HR"."HR_RECORD_TMP"
   (	"ID" NUMBER(10,0),
	"REC_LOC" VARCHAR2(40),
	"EMP_ID" VARCHAR2(6),
	"VERIFY_MODE" VARCHAR2(2),
	"IN_OUT_MODE" VARCHAR2(2),
	"REC_DATA" VARCHAR2(20),
	"REC_TIME" VARCHAR2(20),
	"WORK_CODE" VARCHAR2(2),
	"IMP_TIME" TIMESTAMP (6),
	 PRIMARY KEY ("ID")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "HR"  ENABLE
   ) SEGMENT CREATION IMMEDIATE
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "HR" ;

  CREATE UNIQUE INDEX "HR"."SYS_C0050632" ON "HR"."RECORD_TMP" ("ID")
  PCTFREE 10 INITRANS 2 MAXTRANS 255
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "HR" ;

  ALTER TABLE "HR"."RECORD_TMP" ADD PRIMARY KEY ("ID")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "HR"  ENABLE;
"""
import sys
import getopt
import win32com.client
import datetime
import string
import cx_Oracle
import logging

log_file = "d:\\atten\\"+datetime.datetime.now().strftime('%Y%m')+".log"
log_format = '[%(levelname)s][%(asctime)s] %(message)s'
#log记录到文件
logging.basicConfig(filename=log_file, filemode='a', format=log_format, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
#log记录到控制台
#logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('sqlalchemy.*').setLevel(logging.ERROR)

def Usage():
    print 'Collect ZK attendance record'
    print 'Usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-d, --days: record days to collect.eg: ""-d 30"" or ""--days 30""'

def Version():
    print 'Version 1.0'

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hvd:', ['days=',])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-d', '--days'):
            global DAYS
            #传入的参数都是string型，如果不能转为int，则退出
            try:
                DAYS = string.atoi(a)
            except:
                print str(a) + ' is invalid option'
                Usage()
                sys.exit(3)
        else:
            print 'unhandled option'
            sys.exit(3)

def getrecord(machineID,machineIP,machineLOC,days):
    """
    根据传入的machineID,machineIP,machineLOC参数，
    调用中控SDK提供的函数采集考勤机中的考勤记录，
    根据传入的days变量确定采集数据的日期范围筛选采集到的数据并插入db的data_tbl表
    日志记录到log_tbl表
    数据库连接有主程序打开，通过db变量传入
    读取考勤机记录成功返回1，考勤机无法连接返回0
    """
    rec = []
    employee = []
    logging.info("正在连接"+ str(machineLOC) + str(machineIP)+"...")
    zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')
    if not zk.Connect_Net(machineIP, 4370):
        logging.error("***" + str(machineLOC) + str(machineIP)+"连接失败")
        return 0, employee, rec
    logging.info(str(machineLOC) + str(machineIP)+"连接成功")
    if zk.ReadAllGLogData(1):
        while 1:
            dwMachineNumber, dwEnrollNumber, dwVerifyMode, dwInOutMode, dwYear, dwMonth, dwDay, dwHour, dwMinute, dwSecond, dwWorkcode = zk.SSR_GetGeneralLogData(1)
            if not dwMachineNumber:
                break
            empID = '%04d' % int(dwEnrollNumber)
            time = '%02d' % dwHour + ':' + '%02d' % dwMinute + ':' + '%02d' % dwSecond
            date = '%04d' % dwYear + '-' + '%02d' % dwMonth + '-' + '%02d' % dwDay
            n = datetime.datetime.now()
            d = datetime.datetime.strptime(str(date+" "+time),"%Y-%m-%d %H:%M:%S")
            #days天以内的记录才插入数据库
            if (-1<(n-d).days*86400+(n-d).seconds<=days*86400):
                rec.append({"machine_id":machineID, "emp_id":empID, "verify_mode":dwVerifyMode, "in_out_mode":dwInOutMode, "rec_data":date, "rec_time":time, "work_code":dwWorkcode})
        logging.info(str(machineLOC) + str(machineIP)+"采集考勤记录成功")
    if zk.ReadAllUserID(1):
        while 1:
            machenum, EnrollNumber, username, other, privilege, dwEnable = zk.SSR_GetAllUserInfo(1)
            if not machenum:
                break
            if dwEnable:
                empID = '%04d' % int(EnrollNumber)
                empName = str(username.split(u'\x00')[0].encode('utf8')) #去除结尾的空格
                employee.append({"machine_id": machineID, "emp_id": empID, "emp_name": empName})

        logging.info(str(machineLOC) + str(machineIP)+"采集员工信息成功")
    zk.Disconnect()
    return 1, employee, rec

if __name__ == '__main__':
    #初始化参数
    #采集天数的缺省值，如果命令行传入days则以命令行传入的为准
    DAYS = 1
    DB_TSN = 'hr/123@192.90.33.212:1521/orcl'
    DATA_TBL = 'hr_record_tmp'
    LOG_TBL = 'hr_col_log'
    SYS_TBL = 'hr_machine'
    EMP_TBL = 'hr_employee_tmp'
    #获取命令行传递的参数days，采集的天数，如果没有则使用默认
    main(sys.argv)
    #连接数据库
    logging.info("开始采集考勤机记录，正在连接数据库...")
    try:
        db = cx_Oracle.connect(DB_TSN)
    except:
        logging.error("***无法连接数据库！！！")
        exit(10)
    cursor = db.cursor()
    #获取考勤机参数
    statement = "select * from " + SYS_TBL
    cursor.execute(statement)
    m = list(cursor)
    logging.info("读取考勤机参数成功，"+"本次采集天数为" + str(DAYS) + "天。")
    success = 0
    for row in m:
        machineID = row[0]
        machineIP = row[1]
        machineLOC = row[2]
        #读取考勤记录和员工信息，成功返回1和考勤记录和员工信息，失败返回0
        result_code, employee, rec = getrecord(machineID, machineIP, machineLOC, DAYS)
        if result_code == 1:
            statement = "insert into " \
                  + DATA_TBL \
                  + " values(seq_hr_record_tmp.nextval," \
                  + ":machine_id,:emp_id,:verify_mode,:in_out_mode,:rec_data,:rec_time,:work_code," \
                  + "sysdate)"
            db.cursor().executemany(statement, rec)
            db.cursor().execute("insert into " + LOG_TBL + " values(sysdate," + "'" + str(machineLOC) + str(machineIP)+"采集考勤记录成功.')")
            statement2 = "insert into " \
                  + EMP_TBL \
                  + " values(seq_hr_employee_tmp.nextval," \
                  + ":emp_id,:emp_name,:machine_id)"
            db.cursor().executemany(statement2, employee)
            db.cursor().execute("insert into " + LOG_TBL + " values(sysdate," + "'" + str(machineLOC) + str(machineIP)+"采集员工信息成功.')")
            success = success + 1
        if result_code == 0:
            db.cursor().execute("insert into " + LOG_TBL + " values(sysdate," + "'!!!" + str(machineLOC) + str(machineIP)+"连接失败.')")
        db.commit()
    #cursor.callproc('proc_hr_imp_employee')
    cursor.callproc('proc_hr_imp_record')
    logging.info("采集完毕，本次共采集"+str(len(m))+"台，成功"+str(success)+ "台，失败"+str(len(m)-success)+"台。")
    logging.info("考勤数据请查看" + str(DATA_TBL) + "表，员工信息请查看" + str(EMP_TBL) + "表，错误日志请查看"+ str(LOG_TBL) + "表。")
    db.close()