# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 16:14:22 2017

@author: ekrupczak on LaVision

Divide tiffs up into subfolders with maximum number of files per folder
This allows them to be imported into DaVis which seems unwilling to import more than about 10000 files at a time.

Or pull all tiffs from specified folder between start and end file numbers
"""
import os
import math
import re

def divide_tiffs(path, max_per_folder = 10000):
    """
    Divides all tiffs in path into subfolders with up to max_per_folder files per subfolder
    """
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


def unpack_folders(path):
    """
    Undoes divide_tiffs by unpacking all files in subfolders into the main folder
    """
    for folder in [f for f in os.listdir(path) if "." not in f]:
        print("unpacking", folder)
        for file in os.listdir(path+"/"+folder):
            os.rename(path+"/"+folder+"/"+file, path+"/"+file)
        print("deleting empty folder", folder)
        os.rmdir(path+"/"+folder)
        
def pull_nth_tiff(path, n):
    """
    Pulls every nth tiff into a separate folder
    Designed for reading into DaVis
    Run 'unpack folders' after to undo this action
    """
    tiffs = [file for file in os.listdir(path) if '.tif' in file.lower()]
    print(len(tiffs), "tiffs in ", path)
    newdirname = r"\every_"+str(n)+"th_tiff"
    os.mkdir(path+newdirname)
    for tiff in tiffs[0::n]:
        os.rename(path+r"\\"+tiff, path+newdirname+"\\"+tiff)
    print("Every", str(n)+"th tiff put in ", path+newdirname)
    print("Folder contains ", len(os.listdir(path+newdirname)), "files")
    
    
def pull_tiffs_in_range(path, start, stop):
    """
    Pull all tiffs between file number start and file number stop. 
    Assumes tiff names are formatted as follows: tiff_name_00001.tif
    """
    tiffs = [file for file in os.listdir(path) if '.tif' in file.lower()]
    print(len(tiffs), "tiffs in ", path)
    newdirname = r"\tiffs_in_range"+str(start)+"_"+str(stop)
    os.mkdir(path+newdirname)
    for tiff in tiffs:
        filenum = int(re.findall("(?:_)([0-9]+)(?:_grayscale\.tif|\.TIF)", tiff)[0])
#        print(filenum, filenum > start, filenum < stop)
        if start<=filenum<=stop:
#            print(filenum, tiff)
            os.rename(path+r"\\"+tiff, path+newdirname+"\\"+tiff)
    print("Files placed in",path+newdirname)
    print("Folder contains", len(os.listdir(path+newdirname)))

    
        
        
if __name__ == "__main__":
    
    ##2.5 hz
#    n = 2 ##tower EO
#    n = 6 ##pier EO
    
    ## ~2hz 
#    n = 8 ##pier EO (1.875hz)
    
    ##1.5 hz
#    n = 3 #tower EO (1.66 hz)
    
    ##1 hz
#    n = 15 ##pier EO
#    n = 30 ##tower IR / pier IR
#    n = 5 ## tower EO   

    ## 0.66 Hz
#    n = 8 ##tower EO (0.625 Hz)
    
    ##0.5 Hz
 #   n = 30 #pier EO
    
    ##0.33 Hz
    n = 15 #tower EO
    
    ##0.166 Hz
#    n = 30 #tower EO
#
    
#    camera = "tower_EO_12mm"
#    camera = "pier_EO_08mm"
#    camera = "tower_IR_16mm"
#    camera = "pier_IR_09mm"
    
#    run = r"20170926_1000_towerEO_pierEO/"
#    run = r"20170926_1100_pierIR_pierEO/"
#    run = r"20170926_1200_towerIR_pierIR/"
#    run = r"20170926_1300_towerIR_towerEO/"
#    
#    path = r"D:/RSEX17_TIFF/0926/"+run+camera
    
#    path = r'D:/RSEX17_TIFF/1005/201710051000/'+camera+"/tiffs_in_range4488_7488"
    #path = r'D:\RSEX17_TIFF\1015\201710151610\201710151610_tower_color'
#    path = r'D:\RSEX17_TIFF\1005\201710051000\tower_1015_1025'
#    path = r'D:\RSEX17_TIFF\1005\201710051000\tower_EO_12mm_range_4488_7488_grayscale'
#    path = r'D:\RSEX17_TIFF\1005\201710051000\pier_EO_08mm'
    path = r'D:\RSEX17_TIFF\1005\201710051000\tower_EO_12mm'
#    path = r'E:\RSEX17_TIFF\1005\201710051000\pier_EO_08mm\tiffs_in_range13464_22464'
#    path = r'D:\RSEX17_TIFF\1015\201710151610\201710151610_tower_grayscale'
    
#    path = r"D:/RSEX17_TIFF/1013/201710131200/"+camera
    
#    divide_tiffs(path, max_per_folder = 20*10**3)
#    print("Tiffs divided")
#    path = r'D:\RSEX17_TIFF\1005\201710051000\tower_EO_12mm_range_4488_7488_grayscale'
    unpack_folders(path)
#    pull_nth_tiff(path, n)
    
#    path = r'D:/RSEX17_TIFF/1005/201710051000/tower_EO_12mm'
#    unpack_folders(path)
#    
#    path = r"D:\RSEX17_TIFF\1005\201710051000\tower_EO_12mm_every_2th_tiff_grayscale"
#    pull_tiffs_in_range(path, 4488, 7488)
#    pull_tiffs_in_range(path, 13464, 22464)

#    path = path+"\every_"+str(n)+"th_tiff"
#    unpack_folders(path)
    
#    path = r'E:\RSEX17_TIFF\1005\201710051000\pier_EO_08mm\tiffs_in_range13464_22464'
#    pull_nth_tiff(path, n)