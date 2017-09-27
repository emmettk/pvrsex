# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 10:16:24 2017

@author: ekrupczak

Finds and renames Streams7 VL files after export
Rounds to the nearest minute. Usually a 2 hr run but adjustable
"""

import os
import datetime as dt
import re


date = dt.date(2017, 9, 26)

path = r"D:/RSEX17/"+dt.datetime.strftime(date, "%m%d")

files = os.listdir(path)

files_to_rename = [file for file in files if "Streams7_Recording" in file]

runlength = dt.timedelta(hours = 1, minutes= 59, seconds = 30)

for file in files_to_rename:
    enddate = dt.datetime.strptime(re.findall("(?:Streams7_Recording_)([0-9]{4}-[0-9]{2}-[0-9]{2})", file)[0], "%Y-%m-%d")
    endtime = dt.datetime.strptime(re.findall("(?:Streams7_Recording_[0-9]{4}-[0-9]{2}-[0-9]{2}_)([0-9]{2}_[0-9]{2}_[0-9]{2})", file)[0], "%H_%M_%S")
    end = dt.datetime.combine(enddate.date(), endtime.time())
    start = end - runlength
    filename = dt.datetime.strftime(start, "%Y%m%d%H%M")+'.vl'
#    print(file, filename)
    print("Renamining", file, "to", filename)
    os.rename(path+"/"+file, path+"/"+filename)

