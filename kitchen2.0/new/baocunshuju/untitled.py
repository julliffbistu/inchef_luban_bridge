# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:19:49 2020

@author: lifu_
"""

import codecs

s = u'亚像素精度：\r\n'  #u表示读取中文，\r\n为换行符
f = codecs.open("uvlogs.txt",'w','utf-8')
for i in range(100):
    f.write(str(i*100)+ '\t')
    f.write(str(i)+'\r\n') #\r\n为换行符
f.close()