from PIL import Image
import os
from pylab import *

im = array(Image.open('2.png').convert('L')) # 读取图像到数组中
figure()
# 新建一个图像
# 不使用颜色信息
gray()

contour(im, origin='image')
axis('equal')
axis('off')
figure()
hist(im.flatten(),50)
show()
save('end.png')
