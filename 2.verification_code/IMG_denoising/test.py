#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import os
import sys
import time
import math
import json
import Image
import ImageFilter
#from pytesser import *
import struct
import socket
import random
import MySQLdb
import requesocks
import threading

reload(sys)
sys.setdefaultencoding('utf-8')
Type = sys.getfilesystemencoding()

# session = requesocks.session()

Table = "AS_10212_24_copy"
Table_result = Table + "_result"
Table_check = "BJ_ALL_landmark_check"
HOST, USER, PASSWD, DB, PORT = '192.168.1.28','panghuihui','PHH@aiwen&521322', "IP_BJ", 3306
# HOST, USER, PASSWD, DB, PORT = '171.15.132.56', 'panghuihui', 'PHH@aiwen&521322', 'BJ_ISPCollect', 33306
# HOST, USER, PASSWD, DB, PORT = 'localhost', 'root', 'PHH@aiwen', 'BJ_ISP', 3306
THREAD_COUNT = 10
schedule = 0


def ConnectDB():
    "Connect MySQLdb and Print version."
    connect, cursor = None, None
    while True:
        try:
            connect = MySQLdb.connect(
                host=HOST, user=USER, passwd=PASSWD, db=DB, port=PORT, charset='utf8')
            cursor = connect.cursor()
            break
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
    return connect, cursor


class HandleLandmark(threading.Thread):
    """docstring for HandleLandmark"""

    def __init__(self, lock, ThreadID, tasklist, Total_TaskNum):
        super(HandleLandmark, self).__init__()
        self.lock = lock
        self.ThreadID = ThreadID
        self.tasklist = tasklist
        self.Total_TaskNum = Total_TaskNum

    def run(self):

        global schedule
        connect, cursor = ConnectDB()
        self.lock.acquire()
        print "The Thread tasklist number :", len(self.tasklist)
        self.lock.release()

        for (id, minip_num, maxip_num, district) in self.tasklist:
            self.lock.acquire()
            time_Now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print "Tread-%s:" % self.ThreadID, time_Now, "Already Completed:[%s] ,Also remaining:[%s]" % (schedule, self.Total_TaskNum - schedule)
            self.lock.release()
            cursor.execute("select ip_num, district from Beijing_result_landmark where mark is null and ip_num between %s and %s;"
                % (minip_num, maxip_num))
            rows = cursor.fetchall()
            for (ip_num, landdistrict) in rows:
                if district == landdistrict:
                    cursor.execute(
                        "update Beijing_result_landmark set mark=1 where ip_num=%s;" % ip_num)
                    # connect.commit()
                else:
                    cursor.execute(
                        "update Beijing_result_landmark set mark=0 where ip_num=%s;" % ip_num)
                connect.commit()
            self.lock.acquire()
            schedule += 1
            self.lock.release()
        connect.close()


def Measure_Distance(lon1, lat1, lon2, lat2):
    EARTH_RADIUS = 6371137.0
    lat1 = format(float(lat1), '.8f')
    lon1 = format(float(lon1), '.8f')
    lat2 = format(float(lat2), '.8f')
    lon2 = format(float(lon2), '.8f')
    if lat1 == lat2 and lon1 == lon2:
        return 0
    lat1_radian = math.radians(float(lat1))
    lon1_radian = math.radians(float(lon1))
    lat2_radian = math.radians(float(lat2))
    lon2_radian = math.radians(float(lon2))
    tempresult = math.cos(lon1_radian - lon2_radian) * math.cos(lat1_radian) * \
        math.cos(lat2_radian) + math.sin(lat1_radian) * math.sin(lat2_radian)
    # tempresult_string = str(tempresult)

    distance = EARTH_RADIUS * math.acos(tempresult)
    distance = format(float(distance), '.4f')
    return distance


def Thread_Handle(taskList, Total_TaskNum):

    global THREAD_COUNT
    lock = threading.Lock()
    WorksThread = []
    every_thread_number = len(taskList) / THREAD_COUNT
    if every_thread_number == 0:
        THREAD_COUNT = len(taskList)
        every_thread_number = 1

    for i in range(THREAD_COUNT):
        if i != THREAD_COUNT - 1:
            source_list = taskList[
                i * every_thread_number: (i + 1) * every_thread_number]
            Work = HandleLandmark(lock, i, source_list, Total_TaskNum)
        else:
            source_list = taskList[i * every_thread_number:]
            Work = HandleLandmark(lock, i, source_list, Total_TaskNum)
        Work.start()
        WorksThread.append(Work)
    for Work in WorksThread:
        Work.join()


def main():
    img = Image.open('yanzheng.png')
    # img = img.filter(ImageFilter.CONTOUR)
    img=img.convert('L')
    img.save('01.png','PNG')
    (width, hight) = img.size
    # img=img.convert('RGB')
    print width,hight
    for i in range(width):
        for j in range(hight):
            dat = img.getpixel((i,j))
            if dat < 70:
                img.putpixel((i,j),255)
            if j < 5 or j > hight-5:
                img.putpixel((i,j),255)
            if i <5 or i > width-5:
                img.putpixel((i,j),255)
    for i in range(width):
        for j in range(hight):
            dat = img.getpixel((i,j))
            if dat < 150:
                img.putpixel((i,j),0)
    img.show()
    img.save("02.png", "PNG")
    str = image_to_string(img)
    print str


if __name__ == '__main__':

    print "The Program start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start = time.time()
    main()
    print "The Program end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "[%s]" % (time.time() - start)
    # raw_input("输入任意键结束！！！".decode('utf-8').encode(Type))
