import xml.etree.ElementTree as ET

import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob

classes = ["car", "watcher"]
no_class = ["armor_1", "armor_2", "armor_3", "armor_4", "armor_5"]

def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_name):
    out_file = open('C:/Users/Administrator/Desktop/mydata/labels/' + image_name[:-3] + 'txt', 'w')  # 转换后的txt文件存放路径，自己修改
    f = open('D:/zanghaomin/DJI ROCO/robomaster_South China Regional Competition/image_annotation/' + image_name[:-3] + 'xml')# xml文件路径，根据自己的情况修改
    xml_text = f.read()
    #print(image_name)
    root = ET.fromstring(xml_text)
    f.close()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        #print(obj.find('pose'))
        #if obj.find('pose') != None:
         #cls_two = obj.find('pose').text
         #cls = cls + '_' + cls_two
        #elif cls == 'armor':
          #cls_two = obj.find('armor_class').text
          # cls_three = obj.find('armor_color').text
          # cls = cls + '_' + cls_two + '_' + cls_three
          #cls = cls + '_' + cls_two
        if cls == 'armor':
            if obj.find('pose') == None:
                cls_two= obj.find('armor_class').text
                cls = cls +'_'+ cls_two
                if cls =='armor_7':
                    cls= 'watcher'
        #if cls in no_class:
           # cls = 'car'
        if cls not in classes:
            #print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()

if __name__ == '__main__':

    for image_path in glob.glob("D:/zanghaomin/DJI ROCO/robomaster_South China Regional Competition/image/*.jpg"):  # 每一张图片都对应一个xml文件这里写xml对应的图片的路径
        image_name = image_path.split('\\')[-1]
        convert_annotation(image_name)
