import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob
import numpy
import cv2
from PIL import Image
def convert_annotation(image_name):
    print(image_name)
    in_file = open('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\labels\\' + image_name[:-3] + 'txt')  # xml文件路径
    #out_file = open('C:/Users/Administrator/Desktop/mydata/labels/' + image_name[:-3] + 'txt', 'w')  # 转换后的txt文件存放路径
    f = open('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\labels\\' + image_name[:-3] + 'txt')
    img = cv2.imread('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\images\\' + image_name[:-3] + 'jpg')
    imgg = Image.open('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\images\\' + image_name[:-3] + 'jpg')
    #imgg=imgg.convert('L')
    print(img.shape)
    y, x = img.shape[0], img.shape[1]

    #print(x, y)
    #cv2.imshow("hyyy", img)
    #cv2.waitKey(2000)
    txt_text = f.read()
    #print("all")
    #print(txt_text)
    result_num = 0
    #print("sp1")
    sp1 = list(txt_text.split('\n'))
    #print(sp1)
    for line in sp1:
     print("new line")
     #print(line)
     number = list(line.split(' '))
     #print("number line")
     #print(number)

    #root = numpy.fromstring(txt_text)

    #cls = root.text
     count = 1
     cls = -1
     ld_x=1.0
     ld_y=1.0
     lt_x=1.0
     lt_y=1.0
     rt_x=1.0
     rt_y=1.0
     rd_y=1.0
     rd_x=1.0
     for i in number:
        #print("new_data")
        if i == '':
            #print('A space')
            continue
        if count == 1:
            cls = int(i)
        if count == 2:
            lt_x = float(i)
        if count == 3:
            lt_y = float(i)
        if count == 4:
            ld_x = float(i)
        if count == 5:
            ld_y = float(i)
        if count == 6:
            rt_x = float(i)
        if count == 7:
            rt_y = float(i)
        if count == 8:
            rd_x = float(i)
        if count == 9:
            rd_y = float(i)
        count += 1
        #print(float(i))
     if cls == -1 or (cls % 9) > 5:
         f.close()
         continue
     #print(cls, lt_x, lt_y, ld_x, ld_y, rt_x, rt_y, rd_x, rd_y)
     left = min(min(lt_x, ld_x), min(rt_x, rd_x))
     left = max(0, left)
     left = min(1, left)
     right = max(max(lt_x, ld_x), max(rt_x, rd_x))
     right = max(0, right)
     right = min(1, right)
     upper = min(min(lt_y, ld_y), min(rt_y, rd_y))
     upper = max(0, upper)
     upper = min(1, upper)
     lower = max(max(lt_y, ld_y), max(rt_y, rd_y))
     lower = max(0, lower)
     lower = min(1, lower)
     box = (left*x, upper*y, right*x, lower*y)
     roi = imgg.crop(box)
     #out_file = open('C:/Users/Administrator/Desktop/mydata/labels/' + image_name[:-3] + 'jpg', 'w')
     #roi.show()
     print("cls=", cls)
     roi = roi.resize((24, 24))
     print(roi.size)
     result_num+=1
     str_num = str(result_num)
     roi.save('D:/zanghaomin/mydata/labels/' + image_name[:-4] + '_2021_' + str_num + '.bmp', 'bmp')
     f.close()
     #cv2.waitKey(2000)
     #roi.close()
     #cv2.destroyAllWindows()
    imgg.close()
    roi.close()
wd = getcwd()

for image_path in glob.glob("D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\labels\\*.txt"):
#image_path = 'D:\\zanghaomin\\DJI ROCO\\sps\\train\\label\\0076.txt'
     image_name = image_path.split('\\')[-1]
     convert_annotation(image_name)
