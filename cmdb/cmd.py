import paramiko
import os

def command(ip,port,user,password,cmd):
    '''执行系统命令'''
    req=[]
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip,port=port,username=str(user),password=password,timeout=3)
    cin,cout,cerr=client.exec_command(cmd)
    for i in cout:
        req.append(str(i).replace('\n',''))
    return req

def check_host_active(ip):
    check=os.system("ping -n 1 -w 2 "+ip)
    return check #1失败  0正常


if __name__ == '__main__':
    #print(check_host_active('192.168.3.209'))
    pass
