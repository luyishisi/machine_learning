#!/usr/bin/env python
#encoding=utf-8

import Image,ImageEnhance,ImageFilter
import Data

DEBUG = False

def d_print(*msg):
    global DEBUG
    if DEBUG:
        for i in msg:
            print i,
        print
    else:
        pass

def Get_Num(l=[]):
    min1 = []
    min2 = []
    for n in Data.N:
        count1=count2=count3=count4=0
        if (len(l) != len(n)):
            print "Wrong pic"
            exit()
        for i in range(len(l)):
            if (l[i] == 1):
                count1+=1
                if (n[i] == 1):
                    count2+=1
        for i in range(len(l)):
            if (n[i] == 1):
                count3+=1
                if (l[i] == 1):
                    count4+=1
        d_print(count1,count2,count3,count4)

        min1.append(count1-count2)
        min2.append(count3-count4)
    d_print(min1,"\n",min2)
    for i in range(10):
        if (min1[i] < = 2 or min2[i] <= 2):
            if ((abs(min1[i] - min2[i])) < 10):
                return i
    for i in range(10):
        if (min1[i] <= 4 or min2[i] <= 4):
            if (abs(min1[i] - min2[i]) <= 2):
                return i

    for i in range(10):
        flag = False
        if (min1[i] <= 3 or min2[i] <= 3):
            for j in range(10):
                if (j != i and (min1[j] < 5 or min2[j] &lt;5)):
                    flag = True
                else:
                    pass
            if (not flag):
                return i
    for i in range(10):
        if (min1[i] <= 5 or min2[i] <= 5):
            if (abs(min1[i] - min2[i]) <= 10):
                return i
    for i in range(10):
        if (min1[i] <= 10 or min2[i] <= 10):
            if (abs(min1[i] - min2[i]) <= 3):
                return i

#end of function Get_Num

def Pic_Reg(image_name=None):
    im = Image.open(image_name)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.show()
                    #all by pixel
    s = 12          #start postion of first number
    w = 10          #width of each number
    h = 15          #end postion from top
    t = 2           #start postion of top
    im_new = []
    #split four numbers in the picture
    for i in range(4):
        im1 = im.crop((s+w*i+i*2,t,s+w*(i+1)+i*2,h))
        im_new.append(im1)

    s = ""
    for k in range(4):
        l = []
        #im_new[k].show()
        for i in range(13):
            for j in range(10):
                if (im_new[k].getpixel((j,i)) == 255):
                    l.append(0)
                else:
                    l.append(1)

        s+=str(Get_Num(l))
    return s
print Pic_Reg("./images/22.jpeg")
