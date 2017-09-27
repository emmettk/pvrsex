# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:20:16 2017

@author: ekrupczak on PVAquire

Mislabeled the fiber line test files as 0924 instead of 0923. 
Fixing this.
"""

import os
import re

sourcepath = "E:\\FiberLineTest\\"
subdir = ["A12_EO", "A12_IR", "A34_EO", "A34_IR", "B34_EO", "B34_IR"]

for d in subdir:
    path = sourcepath + d + "\\corrupted_frames_log\\"
    for f in [file for file in os.listdir(path) if "20170924" in file]:
        filename = re.findall("(?:20170924)(.*)", f)[0]
        newfilename = "20170923"+filename
        os.rename(path+f,path+newfilename)
    print("renamed", path)

