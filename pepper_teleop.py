# -*- coding: utf-8 -*- # 
# by oldj http://oldj.net/ #  
#F:70
import pythoncom 
import pyHook  
import qi
import argparse
import sys
import socket
import time
import os 
import subprocess
#import cv2
#import itchat
import mp3play

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
        self.tts=self.session.service("ALTextToSpeech")

params = {
    'ip' : "10.3.100.39",
    'port' : 9559,
    'rgb_topic' : 'pepper_robot/camera/front/image_raw'
}
pio = pepper_test(params)
motion_service=pio.Motion#不知道onKeyboardEvent的调用机理但又想传motion_service进去那就只能先弄出一个全局变量出来了
tab_service   =pio.tab
tts           =pio.tts
clip=mp3play.load('D:/vs2017projects/oculus/Debug/success.mp3')
command=' '



def main():
    global command
    tab_service.hideImage()
    tab_service.showImage("http://s6.mogujie.cn/b2/bao/111114/qc6r_kqyuy6sekrbgercugfjeg5sckzsew_400x400.jpg_468x468.jpg")
    #itchat.auto_login()
    print "you can start now!"
    while command != 'k' and command != 'K':
        clip.play()
        command = raw_input()
        if  command == 'w' or command == 'W':
            motion_service.setStiffnesses("Head", 1.0) 
            motion_service.move(0.25,0,0)
        if  command == 's' or command == 'S':
            motion_service.setStiffnesses("Head", 1.0)
            motion_service.stopMove()
        if  command == 'a' or command == 'A':
            motion_service.setStiffnesses("Head", 1.0)  
            motion_service.move(0,0.25,0)
        if  command == 'd' or command == 'D':
            motion_service.setStiffnesses("Head", 1.0)
            motion_service.move(0,-0.25,0)
        if  command == 'q' or command == 'Q':
            motion_service.setStiffnesses("Head", 1.0)
            motion_service.move(0,0,0.5)
        if  command == 'e' or command == 'E':
            motion_service.setStiffnesses("Head", 1.0)
            motion_service.move(0,0,-0.5)
        '''if  command == 'f' or command == 'F':
            cap = cv2.VideoCapture("rtsp://192.168.3.66:6554/stream_1")
            ret, frame = cap.read()
            print cap.isOpened()
            time.sleep(5)
            name=str(time.time())+".jpg"
            cv2.imwrite(name,frame)
            users=itchat.search_friends(name=u'TanYing')
            userName = users[0]['UserName']
            itchat.send_image('D:/vs2017projects/oculus/Debug/'+name,toUserName=userName)'''
        if command == 'c' or command == 'C':
            tts.say("I need help!")
    tts.say("I have finished!")
    tab_service.hideImage()


 
if __name__ == "__main__":
    main()
