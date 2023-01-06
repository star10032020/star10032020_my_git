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
    imgg = Image.open(image_name)
    imgg=imgg.convert('L')
    imgg.save(image_name)
    imgg.close()
for image_path in glob.glob("D:\\zanghaomin\\mydata\\negative\\*.bmp"):
#image_path = 'D:\\zanghaomin\\DJI ROCO\\sps\\train\\label\\0076.txt'
     convert_annotation(image_path)
