# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:48:14 2017

@author: LaVision
Move tiffs in a certain range to dropbox
This is just roughly copied from console
"""
import os
from shutil import copyfile

dropbox = r"C:\Users\LaVision\Dropbox\20171005_ripcurrent_1015-1025"
pier = r"C:\Users\LaVision\Dropbox\20171005_ripcurrent_1015-1025\pier_EO_08mm"
tower = r"C:\Users\LaVision\Dropbox\20171005_ripcurrent_1015-1025\tower_EO_12mm"

## desired tiff range
p1 = 13467
p2 = 22468
t1 = 4488
t2 = 7489

pierpath = r'D:/RSEX17_TIFF/1005/201710051000/pier_EO_08mm/'
towerpath = r'D:/RSEX17_TIFF/1005/201710051000/tower_EO_12mm/'

#get tiffs only
pierfiles = [file for file in os.listdir(pierpath) if ".TIF" in file]
towerfiles = [file for file in os.listdir(towerpath) if ".TIF" in file]

# get tiffs within desired frame range
pier10min = [file for file in pierfiles if int(file[-9:-4]) in range(p1,p2+1)]
tower10min = [file for file in towerfiles if int(file[-9:-4]) in range(t1, t2+1)]

#for file in pier10min:
#    copyfile(pierpath+file, pier+"/"+file)
    
for file in tower10min:
    copyfile(towerpath+file, tower+"/"+file)