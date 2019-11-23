#!/usr/bin/python
# -*- coding:utf-8 -*-

import SH1106
import time
import config
import traceback
import threading
import Queue
import signal
import sys

import RPi.GPIO as GPIO

from PIL import Image,ImageDraw,ImageFont

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

GPIO.setmode(GPIO.BCM) 
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

usertime = {
        "Henri": 1800,
        "Rhea": 1800
}

q = Queue.Queue();

def timedraw():

    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()

    while 42:
        times = q.get()
        try:
            image1 = Image.new('1', (disp.width, disp.height), "WHITE")
            draw = ImageDraw.Draw(image1)
            font = ImageFont.truetype('Font.ttf', 16)

            top=0
            for name in times:
                draw.text((0,top), name, font = font, fill = 0)
                sec=times[name];
                tstring='{:02}:{:02}:{:02}'.format(sec // 3600, sec % 3600 // 60, sec % 60)
                draw.text((50,top), tstring, font = font, fill = 0)
                top+=20

            disp.ShowImage(disp.getbuffer(image1))

        except IOError as e:
            print(e)


if __name__ == "__main__":
    timedrawth=threading.Thread(target=timedraw)
    timedrawth.daemon=True
    timedrawth.start()

    q.put(usertime.copy());

    while 42:
        change=False
        if not GPIO.input(KEY1_PIN): 
            usertime["Rhea"]-=1;
            change=True
        if not GPIO.input(KEY2_PIN): 
            usertime["Henri"]-=1;
            change=True

        if change == True:
            q.put(usertime.copy());

        time.sleep(1);

