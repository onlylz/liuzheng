# encoding=utf-8
import re
import telnetlib


def do_telnet(Host, username, password, finish, commands):
    import telnetlib
    import re
    '''''Telnet远程登录：Windows客户端连接Linux服务器'''

    # 连接Telnet服务器
    tn = telnetlib.Telnet(Host, port=23, timeout=10)
    tn.set_debuglevel(9)

    # 输入登录用户名
    #
    # tn.read_until(b'login: ')
    if tn.expect([b"ogin"],timeout=5)[0]!=0:
        print("No Login promot")
        exit(2)
    tn.write(username.encode('ascii') + b"\n")

    # 输入登录密码
    #tn.read_until(b'Password: ')
    if tn.expect([b"assword"],timeout=5)[0]!=0:
         print("No Password promot")
         exit(2)
    tn.write(password.encode('ascii') + b"\n")

    # 登录完毕后执行命令
    # tn.read_until(finish.encode('ascii'))

    if tn.expect([b".*\$"],timeout=5)[0]!=0:
        print("No promot")
        exit(2)

    for command in commands:
        tn.write(command.encode('ascii') + b"\n")
        r = tn.read_until(finish.encode('ascii'))
        print(r.decode('utf8'))
    # 执行完毕后，终止Telnet连接（或输入exit退出）
    tn.close()

def auto_task_telnet_linux(hosts,cmds):
    for host in hosts:
        hostname = host[0]
        ip = host[1]
        username = host[2]
        password = host[3]
        ps = host[4]
        print([ps.encode('ascii')])
        try:
            print("Begin to connect host "+ ip )
            tn = telnetlib.Telnet(ip, port=23, timeout=10)
        except:
            print("Can not connect host "+ip)
            continue
        tn.set_debuglevel(9)
        # 输入用户名
        if tn.expect([b"ogin:"], timeout=10)[0]!=0:
            print("No Login prompt")
            tn.close()
            continue
        tn.write(username.encode('ascii') + b"\n")
        # 输入密码
        if tn.expect([b"assword"],timeout=10)[0]!=0:
            print("No Password prompt")
            tn.close()
            continue
        tn.write(password.encode('ascii') + b"\n")
        # 等待提示符
        try:
            tn.read_until(ps.encode('ascii'),timeout=10)
        except:
            print("Can not login")
            tn.close()
            continue

        # 批量执行命令
        for cmd in cmds:
            tn.write(cmd.encode('ascii') + b"\n")
            r = tn.read_until(ps.encode('ascii'))
            print(r.decode('utf8'))

        tn.close()


if __name__ == '__main__':
    # 配置选项
    #Host = '192.168.99.200'  # Telnet服务器IP
    #username = 'lz'  # 登录用户名
    #password = '123'  # 登录密码
    # finish = ':~$ '  # 命令提示符
    #finish = '$'
    #commands = ['ls / -l']
    #do_telnet(Host, username, password, finish, commands)
    hosts=[['host1','192.168.99.99','root','123456',"#"],['host2','192.168.99.200','lz','123',"$"]]
    cmds=['ls -l','mount']
    auto_task_telnet_linux(hosts,cmds)