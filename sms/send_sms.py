import socket
import datetime


def send_sms(content):

    h = '000000006008'
    t = str(datetime.datetime.strftime(datetime.datetime.now(), '%m-%d %H:%M'))
    header = h + t
    c = header + content
    print(c)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('dxpt.com', 8888))
    sock.send(c.encode("utf-8"))
    sock.close()

content= "测试123"
send_sms(content)



