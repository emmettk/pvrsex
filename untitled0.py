# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:48:14 2017

@author: LaVision
Move tiffs in a certain range to dropbox
This is just roughly copied from console
"""

dropbox = r"C:\Users\LaVision\Dropbox\20171005_ripcurrent_1015-1025"
pier = r"C:\Users\LaVision\Dropbox\20171005_ripcurrent_1015-1025\pier_EO_08mm"
tower = r"C:\Users\LaVision\Dropbox\20171005_ripcurrent_1015-1025\tower_EO_12mm"
p1 = 13467
p2 = 22468
t1 = 4488
t2 = 7489
pierpath = r'D:/RSEX17_TIFF/1005/201710051000/pier_EO_08mm/'
towerpath = r'D:/RSEX17_TIFF/1005/201710051000/tower_EO_12mm/'
pierfiles = os.listdir(pierpath)
import os
pierfiles = os.listdir(pierpath)
towerfiles = os.listdir(towerpath)
pierfiles[0]
pierfiles = [file for file in pierfiles if ".TIF" in file]
towerfiles = [file for file in towerfiles if ".TIF" in file]
file[-10:-4]
towerfiles[0][-10:-4]
towerfiles[0][-10:-3]
towerfiles[0][-9:-4]
pier10min = [file for file in pierfiles if int(file[-9:-4]) in range(p1,p2)]
pier10min = [file for file in pierfiles if int(file[-9:-4]) in range(p1,p2+1)]
tower10min = [file for file in towerfiles if int(file[-9:-4]) in range(t1, t2+1)]
from shutil import copyfile
for file in pier10min:
    copyfile(pierpath+file, pier+"/"+file)
for file in tower10min:
    copyfile(towerpath+file, tower+"/"+file)