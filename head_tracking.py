# -*- coding: utf-8 -*- # 
import pythoncom 
import pyHook  
import qi
import argparse
import sys
import socket
import time
import os 
import subprocess
import cv2
import itchat

s = socket.socket()         # 创建 socket 对象
#host = socket.gethostname() # 获取本地主机名
port = 12345                # 设置端口
s.bind(("127.0.0.1", port))        # 绑定端口
s.listen(5)
child1=subprocess.Popen('oculus.exe')#开启客户端子进程流出oculus数据
c, addr = s.accept()     # 建立客户端连接。

class pepper_test():#我们不清楚onKeyBoardEvent的构造才做出一个pepper_test类
    def __init__(self, params):
        self.ip = params['ip']
        self.port = params['port']
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        except RuntimeError:
            print ("[Kamerider W] : connection Error!!")
            sys.exit(1)
         #订阅需要的服务
        self.Motion=self.session.service("ALMotion")
        self.tab=self.session.service("ALTabletService")
params = {
    'ip' : "10.3.100.39",
    'port' : 9559,
    'rgb_topic' : 'pepper_robot/camera/front/image_raw'
}
pio = pepper_test(params)
motion_service=pio.Motion#不知道onKeyboardEvent的调用机理但又想传motion_service进去那就只能先弄出一个全局变量出来了
tab_service   =pio.tab

def main():
    while True:
        origin=c.recv(1024)
        #print c.recv(1024)#到时就这样用c接受
        str_group=origin.split(',')
        try:
            o_pitch=float(str_group[0])
            o_yaw=float(str_group[1])
            p_pitch=o_pitch*-2.5
            p_yaw=(o_yaw-0.1)*15/7
            motion_service.setStiffnesses("Head", 1.0)
            motion_service.angleInterpolation(
                ["HeadYaw"],
                [p_yaw],
                [0.3],######################################################时间
                True,
            )
            #motion_service.setStiffnesses("Head", 1.0)
            motion_service.angleInterpolation(
                ["HeadPitch"],
                [p_pitch],
                [0.3],######################################################时间
                True,
            )
        except ValueError:
            continue

if __name__ == "__main__":
    main()
