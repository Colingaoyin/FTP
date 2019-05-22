"""
ftp客户端
"""


from threading import Thread
from socket import *
import sys,os
import time

#具体功能
class FtpClient:
    def __init__(self,s):
        self.s = s

    def do_list(self):
        self.s.send(b"L")
        data = self.s.recv(128).decode()
        if data == "OK":
            data = self.s.recv(4096)
            print(data.decode())

    def do_quit(self):
        self.s.send(b"Q")
        self.s.close()
        sys.exit("谢谢使用")

    def do_get(self,filename):
        #发送请求
        self.s.send(("G " + filename).encode())
        data = self.s.recv(128).decode()
        if data == 'OK':
            fd = open(filename,'wb')
            #接受内容写入文件
            while True:
                data = self.s.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        #发送请求
        try:
            f = open(filename,'rb')
        except Exception:
            print("没有该文件")
            return

        filename = filename.split('/')[-1]
        self.s.send(("P " + filename).encode())
        data = self.s.recv(128).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.s.send(b"##")
                    break
                self.s.send(data)
            f.close()
        else:
            print(data)




#发起请求
def request(s):
    ftp = FtpClient(s)
    while True:
        print("\n=============命令选项=================")
        print("************* list******************")
        print("*************get file******************")
        print("*************put file******************")
        print("************* quit******************")
        print("=======================================")

        cmd = input("输入命令：")
        if cmd.strip() == 'list':
            s.send(cmd.encode())
            ftp.do_list()
        elif cmd[:3]== "get":
            filename = cmd.strip().split(' ')[-1]
            ftp.do_get(filename)

        elif cmd[:3] == "put":
            filename = cmd.strip().split(' ')[-1]
            ftp.do_put(filename)

        elif cmd == "quit":
            ftp.do_quit()

#网络链接
def main():
    ADDR = ('176.215.155.175',8888)
    s = socket()

    try:
        s.connect(ADDR)
    except Exception as e:
        print("链接服务器失败:",e)
        return
    else:
        print("""
        ******************************
                Data  File   Image
        *******************************
        """)
        try:
            cls = input("请输入文件种类：")
        except KeyboardInterrupt:
            print("您已经退出服务")
        else:
            if cls not in ['Data','File','Image']:
                print("Sorry input Error!!")
                return
            else:
             s.send(cls.encode())
             request(s)


if __name__ == "__main__":
    main()