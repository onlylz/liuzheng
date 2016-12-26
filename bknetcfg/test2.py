# encoding=utf-8


def bak_csc_r38_cfg(name, ip, user, passwd, supasswd):
    print("bak_csc_r38_cfg: " + name + ip + user + passwd + supasswd)


def bak_h3c_s75_cfg(name, ip, user, passwd, supasswd):
    print("bak_h3c_s75_cfg: "+name+ip+user+passwd+supasswd)


def bak_dev_cfg(ven, model, name, ip, user, passwd, supasswd):
    eval("bak_"+ven+"_"+model+"_cfg")(name, ip, user, passwd, supasswd)

if __name__ == '__main__':
    hosts = (('h3c','s75','core1','192.90.33.1','liuzheng','jjyhncfh','ncfhjjyh'),
           ('csc','r38', 'r1', '192.90.33.2', 'liuzheng', 'jjyhncfh', 'ncfhjjyh'))
    for host in hosts:
        bak_dev_cfg(host[0],host[1],host[2],host[3],host[4],host[5],host[6])
