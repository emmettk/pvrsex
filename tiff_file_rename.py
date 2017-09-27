# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:00:30 2017

@author: PVAquire

TIFF file renamer

Takes files with a name like "Movie1_Streams7_Recording_2017-09-18_11_59_33_tower_EO_12mm__00023.tiff" and renames them to "201709181000_tower_EO_12mm_00023.tif"

Same code skeleton as Export_VL_file_rename but applied to each file. 
"""
import os
import datetime as dt
import re


date = dt.date(2017, 9, 19)
camera = "tower_EO_12mm"

path = r"E:/RSEX17_TIFF/"+dt.datetime.strftime(date, "%m%d")+r"/"+camera

files = os.listdir(path)

files_to_rename = [file for file in files if "Streams7_Recording" in file]

## Assumes 2 hr nominal runs with 30 sec spacers
runlength = dt.timedelta(hours = 1, minutes= 59, seconds = 30)

for file in files_to_rename:
    enddate = dt.datetime.strptime(re.findall("(?:Streams7_Recording_)([0-9]{4}-[0-9]{2}-[0-9]{2})", file)[0], "%Y-%m-%d")
    endtime = dt.datetime.strptime(re.findall("(?:Streams7_Recording_[0-9]{4}-[0-9]{2}-[0-9]{2}_)([0-9]{2}_[0-9]{2}_[0-9]{2})", file)[0], "%H_%M_%S")
    filenumber = re.findall("(?:_)([0-9]+)(?:\.TIF)", file)[0]
    end = dt.datetime.combine(enddate.date(), endtime.time())
    start = end - runlength
    filename = dt.datetime.strftime(start, "%Y%m%d%H%M")+'_'+camera+'_'+str(filenumber)+'.tif'
    print("Renamining", file, "to", filename)
    os.rename(path+"/"+file, path+"/"+filename)

