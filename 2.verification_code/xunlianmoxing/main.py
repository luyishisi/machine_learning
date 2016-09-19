#!/usr/bin/env python
#encoding=utf-8

import Image,ImageEnhance,ImageFilter
import sys

image_name = "./images/81.jpeg"
im = Image.open(image_name)
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
#im.show()
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

f = file("data.txt","a")
for k in range(4):
    l = []
    #im_new[k].show()
    for i in range(13):
        for j in range(10):
            if (im_new[k].getpixel((j,i)) == 255):
                l.append(0)
            else:
                l.append(1)

    f.write("l=[")

    n = 0
    for i in l:
        if (n%10==0):
            f.write("\n")
        f.write(str(i)+",")
        n+=1
    f.write("]\n")
