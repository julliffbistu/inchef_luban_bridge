# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:01:31 2020

@author: lifu_
"""

import cv2
import codecs
import numpy as np

IMG = cv2.imread('back.png')

f = codecs.open('uvlogs.txt', mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8’编码读取
line = f.readline()   # 以行的形式进行读取文件
list1 = []
list2 = []
while line:
    a = line.split()
    b = a[0:1]   # 这是选取需要读取的位数
    c = a[1:2]
    list1.append(b)  # 将其添加在列表之中
    list2.append(c)
    
    line = f.readline()
f.close()

for i in range(len(list1)):
    
    print(list1[i],list2[i])
    cv2.circle(IMG, (np.int32(list1[i]), np.int32(list2[i])), 4, (0,0,255), -1)

cv2.imshow("back",IMG)
cv2.waitKey(0)