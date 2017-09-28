# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 16:14:22 2017

@author: ekrupczak on LaVision

Divide tiffs up into subfolders with maximum number of files per folder
This allows them to be imported into DaVis which seems unwilling to import more than about 10000 files at a time.
"""
import os
import math

def divide_tiffs(path, max_per_folder = 10000):
    tiffs = [file for file in os.listdir(path) if ".tif" in file]
    num_sub_dir = math.ceil(len(tiffs)/max_per_folder)
    print("Dividing", len(tiffs), "tiffs into", num_sub_dir, "directories")
    for i in range(1,num_sub_dir+1):
        os.mkdir(path+r"\tiffs_pt"+str(i).zfill(2))
        if i < num_sub_dir:
            for file in tiffs[max_per_folder*(i-1):max_per_folder*i]:
                os.rename(path+r"\\"+file, path+r"\tiffs_pt"+str(i)+r"\\"+file)
        elif i == num_sub_dir:
            for file in tiffs[max_per_folder*(i-1):]:
                os.rename(path+r"\\"+file, path+r"\tiffs_pt"+str(i)+r"\\"+file) 
        print("Directory", "tiffs_pt"+str(i), "populated")



if __name__ == "__main__":
#    camera = "tower_EO_12mm"
#    camera = "pier_EO_08mm"
#    camera = "tower_IR_16mm"
    camera = "pier_IR_09mm"
    
#    run = r"20170926_1000_towerEO_pierEO/"
#    run = r"20170926_1100_pierIR_pierEO/"
    run = r"20170926_1200_towerIR_pierIR/"
#    run = r"20170926_1300_towerIR_towerEO/"
#    
    path = r"D:/RSEX17_TIFF/0926/"+run+camera
    
#    path = r"D:\RSEX17_TIFF\0926\20170926_1300_towerIR_towerEO\tower_IR_16mm"
    divide_tiffs(path, max_per_folder = 20*10**3)
    print("Tiffs divided")