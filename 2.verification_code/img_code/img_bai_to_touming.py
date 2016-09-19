from PIL import Image

def transPNG(srcImageName,dstImageName):
    img = Image.open(srcImageName)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = list()
    for item in datas:
        if item[0] >220 and item[1] > 220 and item[2] > 220:
            newData.append(( 255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(dstImageName,"PNG")

if __name__ == '__main__':
    transPNG("2.png","3.png")
