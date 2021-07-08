import cv2
import glob
inputFile = r'G:\Pr_Yk'
outFile = r'G:\Pr_Yk\cs\\'
#筛选出glos图来
originalFile = glob.glob(inputFile + '\*glos.jpg')
#反相功能
def fan(img):
    height, width, channels = img.shape
    fanImg = img.copy()
    for i in range(height):
        for j in range(width):
            #反色公式[255, 255, 255] - [r, g, b]或255-img[i][j]
            fanImg[i, j] = (255 - img[i, j][0],255-img[i,j][1],255-img[i,j][2])
    return fanImg

#把originalFile筛选出的glos关键字的图片通通进行反相保存，到outFile位置。
for i in originalFile:
    img = cv2.imread(i)
    Fanimg = fan(img)
    outSaveName = i.split('\\')[-1]
    outSavePath = outFile+outSaveName

    cv2.imwrite(outSavePath,Fanimg)



