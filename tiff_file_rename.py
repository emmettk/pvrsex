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
from pytz import timezone

def rename(files_to_rename, runlength, camera, timestamp = False):
    """
    if timestamp = True, takes a file with a name like "'Movie1_Streams7_Recording_2017-09-26_10_55_11_tower_EO_12mm_00000_09.26.2017_14.00.02.591.tif'
    and renames them to EST: "201709261000_tower_EO_12mm_00000_100002591.tif"
    if timestamp = False, takes files with a name like "Movie1_Streams7_Recording_2017-09-18_11_59_33_tower_EO_12mm__00023.tif" 
    and renames them to "201709181000_tower_EO_12mm_00023.tif"
    """

    for file in files_to_rename:
        enddate = dt.datetime.strptime(re.findall("(?:Streams7_Recording_)([0-9]{4}-[0-9]{2}-[0-9]{2})", file)[0], "%Y-%m-%d")
        endtime = dt.datetime.strptime(re.findall("(?:Streams7_Recording_[0-9]{4}-[0-9]{2}-[0-9]{2}_)([0-9]{2}_[0-9]{2}_[0-9]{2})", file)[0], "%H_%M_%S")
#        filenumber = re.findall("(?:_)([0-9]+)(?:\.TIF)", file)[0]
        search = "(?:_"+camera+"_)([0-9]{5})(?:_|\.TIF|\.tif)"
#        print(file, search)
        filenumber = re.findall(search, file)[0]
#        print(file, filenumber)
        end = dt.datetime.combine(enddate.date(), endtime.time())
        start = end - runlength
        filename = dt.datetime.strftime(start, "%Y%m%d%H%M")+'_'+camera+'_'+str(filenumber)+'.tif'
        if timestamp:
            search2 = "(?:_"+filenumber+"_)(.+)(?:\.tif|\.TIF)"
            time = re.findall(search2, file)
            if len(time) > 0:
                framedt = dt.datetime.strptime(time[0], "%m.%d.%Y_%H.%M.%S.%f").replace(tzinfo = timezone("UTC"))
                framedt = framedt.astimezone(timezone("America/Puerto_Rico"))##Atlantic Standard Time: UTC-4
#                print(file, framedt)
                filename = filename[:-4]+"_"+dt.datetime.strftime(framedt, "%H%M%S%f")[:-3]+".tif"
        print("Renamining", file, "to", filename)
        os.rename(path+"/"+file, path+"/"+filename)



if __name__ == "__main__":
    print("Timestamps appended are in the format: HHMMSSmmm (miliseconds: 02.123sec = 02123)")
#    camera = "tower_EO_12mm"
#    camera = "pier_EO_08mm"
#    camera = "tower_IR_16mm"
    camera = "pier_IR_09mm"
    
#    run = r"20170926_1000_towerEO_pierEO/"
#    run = r"20170926_1100_pierIR_pierEO/"
    run = r"20170926_1200_towerIR_pierIR/"
#    run = r"20170926_1300_towerIR_towerEO/"
    
    path = r"D:/RSEX17_TIFF/0926/"+run+camera
    
#    date = dt.date(2017, 9, 19)
#    path = r"E:/RSEX17_TIFF/"+dt.datetime.strftime(date, "%m%d")+r"/"+camera
#    path = r"D:/RSEX17_TIFF/0926/20170926_1000_towerEO_pierEO/"+camera
#    path = r"D:/RSEX17_TIFF/0926/20170926_1200_pierIR_pierEO/"+camera

#    path = r"D:/RSEX17_TIFF/testdir"
    
    files = os.listdir(path)
    
    files_to_rename = [file for file in files if "Streams7_Recording" in file]
    tiffs = [file for file in files_to_rename if ".tif" in file]
    
    ## Assumes 2 hr nominal runs with 30 sec spacers
#    runlength = dt.timedelta(hours = 1, minutes= 59, seconds = 30)
    runlength = dt.timedelta(minutes = 55)
    rename(tiffs, runlength, camera, timestamp = True)
    
    
    
