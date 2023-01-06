import random
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
    ll_left = 2
    ll_right = -1
    ll_upper = 2
    ll_lower = -1
    in_file = open('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\labels\\' + image_name[:-3] + 'txt')  # xml文件路径
    #out_file = open('C:/Users/Administrator/Desktop/mydata/labels/' + image_name[:-3] + 'txt', 'w')  # 转换后的txt文件存放路径
    f = open('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\labels\\' + image_name[:-3] + 'txt')
    img = cv2.imread('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\images\\' + image_name[:-3] + 'jpg')
    imgg = Image.open('D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\images\\' + image_name[:-3] + 'jpg')
    #imgg = imgg.convert('L')
    print(img.shape)
    y, x = img.shape[0], img.shape[1]
    copyy = imgg.copy()

    txt_text = f.read()

    result_num = 0
    n_count = 0
    sp1 = list(txt_text.split('\n'))
    f.close()
    for line in sp1:
     print("new line")
     #print(line)
     number = list(line.split(' '))

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
     ll_left = min(ll_left, left)
     ll_right = max(right, ll_right)
     ll_upper = min(ll_upper, upper)
     ll_lower = max(ll_lower, lower)
     if cls == -1:
         continue
     if  (cls % 9) > 5:
         box = (left * x, upper * y, right * x, lower * y)
         roi = imgg.crop(box)
         #roi = roi.resize((24, 24))
         print(roi.size)
         n_count += 1
         n_str = str(n_count)
         roi.save('D:\\zanghaomin\\mydata\\negative\\' + image_name[:-4] + '_2021_' + n_str + '_negative' + '.bmp', 'bmp')
         continue
     else:
         box = (int(left * x),int( upper * y), int(right * x), int(lower * y))
         roi = imgg.crop(box)
         print("cls=", cls)
         roi = Image.new('RGB', roi.size, color=(0, 0, 0))

         copyy.paste(roi, box)

     result_num += 1
     #copyy=copyy.resize((24, 24))
     str_num = str(result_num)
     #copyy.save("D:\\zanghaomin\\pp\\"+ image_name[:-4] + '_train_big_' + str_num + '.bmp','bmp')
     copyy.save('D:\\zanghaomin\\mydata\\negative\\' + image_name[:-4] + '_2021_big_' + str_num + '.bmp','bmp')
     print("cls=", cls)
     result_num += 1
     str_num = str(result_num)
     print("ll_left=", ll_left)
     print("ll_right=", ll_right)
     print("ll_upper=", ll_upper)
     print("ll_lower=", ll_lower)
    if result_num >= 0:
        imgg = copyy.copy()
        while n_count <= 10:
            n_right = random.uniform(0.4, 0.8)
            n_left = random.uniform(0.2, n_right-0.1)
            n_upper = random.uniform(0.2, 0.4)
            n_lower = random.uniform(n_upper+0.1, 0.8)
            print(n_left, n_right, n_upper, n_lower)
            box = (n_left * x, n_upper * y, n_right * x, n_lower * y)
            roi = imgg.crop(box)
            #roi = roi.resize((24, 24))
            print(roi.size)
            n_count += 1
            n_str = str(n_count)
            roi.save('D:\\zanghaomin\\mydata\\negative\\' + image_name[:-4] + '_2021_' + n_str + '_negative' + '.bmp', 'bmp')
    copyy.close()
    imgg.close()
    roi.close()
wd = getcwd()

for image_path in glob.glob("D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\labels\\*.txt"):
  #image_path = 'D:\\zanghaomin\\DJI ROCO\\2021-RMUC-0417-0916\\2021-RMUC-0417-0916\\labels\\515.txt'
  image_name = image_path.split('\\')[-1]
  convert_annotation(image_name)
