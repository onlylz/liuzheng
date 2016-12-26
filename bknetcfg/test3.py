# coding: utf8
import re, sys
import pexpect
from pexpect import popen_spawn

# enable/disable debug mode
#DEBUG = True


#
# child = pexpect.spawn('telnet %s' % ip)

child = pexpect.popen_spawn.PopenSpawn('cmd')
#child = pexpect.popen_spawn.PopenSpawn('telnet 99.99.11.1')
print(child)
child.send("telnet 99.99.11.1\r")
'''child.expect('(?i)Password: ', timeout=2)  # 匹配Password: ,注意问号后有空格
child.send(pwd + '\r')  # 这里要输入密码+回车(\r),不要用sendline方法
child.expect('Please press ENTER.\r\n', timeout=1)
child.send('\r')  # 根据上面提示,按回车后继续
child.expect(ps[0], timeout=2)  # 匹配第1提示符
child.send('system-view' + '\r')  # 进入system-view视图
child.expect(ps[1], timeout=2)  # 匹配第2个提示符
output = ""
out = ""
child.send(tcmd + '\r')  # 执行命令
child.expect(tcmd + '\r')  # 匹配命令回显
child.expect(ps[1], timeout=2)  # 匹配命令执行完提示符
out = child.before  # 捕获命令的输出结果
if out != '':
     out = re.sub('.*\[.*', '', out)  # 处理输出结果的尾部提示符
     out = re.sub('\015', '', out)  # 处理输出结果的尾部^M(实际上是回车符)
     output += "\n" + tcmd + "执行结果: \n" + "\n".join(
     [j.strip() for j in out.split('\n') if j != ''])  # 删除命令输出中的多余空行和行首尾空格

'''
#child.expect(pexpect.EOF)
#print(child.before)
r = child.expect('name:')
print(r)
'''
child.send("liuzheng\r")
child.expect("Password:", timeout=10)
child.send("jjyhncfh\r")
child.expect(">", timeout=10)
child.send("ncfhjjyh\r")
child.expect(">", timeout=10)
child.send("dis arp")
'''