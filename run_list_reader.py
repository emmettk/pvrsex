# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:37:55 2017

@author: ekrupczak on LaVision

Import file run list in human-readable text file (which has some specific extra tabs for lines of different widths)
and save as a csv that can be read by eg Excel
"""
import pandas as pd

path = r"C:\Users\LaVision\Dropbox\PVRSEX17\RSEX17_run_list.txt"
pathout = r"C:\Users\LaVision\Dropbox\PVRSEX17\RSEX17_run_list.csv"

names = ['Date', 'Start', 'Length', 'Sled', 'RAID0', 'RAID1', 'RAID2', 'RAID3',
       'tower_IR_16mm', 'Unnamed: 9', 'pier_IR_08mm', 'Unnamed: 11',
       'tower_EO_12mm', 'Unnamed: 13', 'pier_EO_09mm', 'Unnamed: 15', 'Notes']

runlist = pd.read_csv(path, sep = "\t", skiprows = [0,1], error_bad_lines = False, dtype = "object", names = names, engine = 'python' )
runlist = runlist.drop(labels = [col for col in runlist.columns if "Unnamed" in col], axis = 1)

runlist.to_csv(pathout, index = False)

##Read the csv we just made back in and make sure it looks okay
runfile1 = pd.read_csv(pathout, dtype = "object")


##Now we have a dataframe from which we can print some useful stuff
#runfile1.loc[runfile1.Date.apply(lambda x: x == "1015")][["Date", "Start"]+[col for col in runfile1.columns if "mm" in col]]