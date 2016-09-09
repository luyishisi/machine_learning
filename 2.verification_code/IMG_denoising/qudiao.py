#coding:utf-8
import sys,os
from PIL import Image,ImageDraw

#二值数组
t2val = {}
def twoValue(image,G):
    for y in xrange(0,image.size[1]):
        for x in xrange(0,image.size[0]):
            g = image.getpixel((x,y))
            if g > G:
                t2val[(x,y)] = 1
            else:
                t2val[(x,y)] = 0

# 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image,N,Z):

    for i in xrange(0,Z):
        t2val[(0,0)] = 1
        t2val[(image.size[0] - 1,image.size[1] - 1)] = 1
        print image.size[0]#宽
        print image.size[1]#高
        for x in xrange(1,image.size[0] - 1 ):
            for y in xrange(1,image.size[1] - 1):

                nearDots = 0
                L = t2val[(x,y)]
                if L == t2val[(x - 1,y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1,y)]:
                    nearDots += 1
                if L == t2val[(x- 1,y + 1)]:
                    nearDots += 1
                if L == t2val[(x,y - 1)]:
                    nearDots += 1
                if L == t2val[(x,y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1,y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1,y)]:
                    nearDots += 1
                if L == t2val[(x + 1,y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x,y)] = 1

def pIx(self):
    data = self
    #图片的长宽
    w = self.size[1]
    h = self.size[0]

    #data.getpixel((x,y))获取目标像素点颜色。
    #data.putpixel((x,y),255)更改像素点颜色，255代表颜色。

    try:
        for x in xrange(1,w-1):
            if x > 1 and x != w-2:
                #获取目标像素点左右位置
                left = x - 1
                right = x + 1

            for y in xrange(1,h-1):
                #获取目标像素点上下位置
                up = y - 1
                down = y + 1

                if x <= 2 or x >= (w - 2):
                    data.putpixel((x,y),255)

                elif y <= 2 or y >= (h - 2):
                    data.putpixel((x,y),255)

                elif data.getpixel((x,y)) == 0:
                    if y > 1 and y != h-1:

                        #以目标像素点为中心点，获取周围像素点颜色
                        #0为黑色，255为白色
                        up_color = data.getpixel((x,up))
                        down_color = data.getpixel((x,down))
                        left_color = data.getpixel((left,y))
                        left_down_color = data.getpixel((left,down))
                        right_color = data.getpixel((right,y))
                        right_up_color = data.getpixel((right,up))
                        right_down_color = data.getpixel((right,down))

                        #去除竖线干扰线
                        if down_color == 0:
                            if left_color == 255 and left_down_color == 255 and \
                                right_color == 255 and right_down_color == 255:
                                data.putpixel((x,y),255)

                        #去除横线干扰线
                        elif right_color == 0:
                            if down_color == 255 and right_down_color == 255 and \
                                up_color == 255 and right_up_color == 255:
                                data.putpixel((x,y),255)



                    #去除斜线干扰线
                    if left_color == 255 and right_color == 255 \
                            and up_color == 255 and down_color == 255:
                        data.putpixel((x,y),255)
                else:
                    pass

                #保存去除干扰线后的图片
                data.save("test.png","png")
    except:
        return False

def saveImage(filename,size):
    image = Image.new("1",size)
    draw = ImageDraw.Draw(image)

    for x in xrange(0,size[0]):
        for y in xrange(0,size[1]):
            draw.point((x,y),t2val[(x,y)])

    image.save(filename)

image = Image.open("./1.png").convert("L")
#pIx(image)
twoValue(image,130)
clearNoise(image,2,1)
saveImage("./5.png",image.size)
