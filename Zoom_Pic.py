from PIL import Image
import os
import glob

#输入路径（筛选格式在下面）
inputFile = r'G:\Pr_Yk'
outFile =r'G:\\Pr_Yk\\cs\\'
#计算出等比缩放的尺寸
def scale(filePath, width=None, height=None):
    """指定宽或高，得到按比例缩放后的宽高

    :param filePath:图片的绝对路径
    :param width:目标宽度
    :param height:目标高度
    :return:按比例缩放后的宽和高
    """
    if not width and not height:
        width, height = Image.open(filePath).size  # 原图片宽高
    if not width or not height:
        _width, _height = Image.open(filePath).size
        height = width * _height / _width if width else height
        width = height * _width / _height if height else width
    return int(width), int(height)

#筛选出jpg图片
originalFile = glob.glob(inputFile + '\*.jpg')

for i in originalFile:
    #遍历出originalFile的jpg并等比缩放为512的图片
    img1 = Image.open(i).resize(scale(i,width=512))#改尺寸
    #搞出带文件名字的路径
    outSaveName = i.split('\\')[-1]
    outSavePath = outFile+outSaveName
    #保存
    img1.save(outSavePath)






