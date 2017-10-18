# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:37:55 2017

@author: ekrupczak on LaVision

Import file run list in human-readable text file (which has some specific extra tabs for lines of different widths)
and save as a csv that can be read by eg Excel
"""
import pandas as pd
import os

def read_runfile_csv(computer = "LaVision"):
    """
    Reads a runfile csv that has already been made
    """
    if computer == "LaVision":
        ## LaVision pathway
        pathout = r"C:\Users\LaVision\Dropbox\PVRSEX17\RSEX17_run_list.csv"  
    elif computer == "PVAquire":
        ## PVAquire pathway
        pathout = r"C:\Users\PVAquire\Dropbox\PVRSEX17\RSEX17_run_list.csv"
       
    return pd.read_csv(pathout, dtype = "object")
    
def make_runfile_csv(computer = "LaVision"):
    """
    Make a csv from the text file listing runs
    Cleans up some tabs that are added for readability of the raw text file
    computer path options: LaVision, PVAquire
    """
    if computer == "LaVision":
        ## LaVision pathway
        path = r"C:\Users\LaVision\Dropbox\PVRSEX17\RSEX17_run_list.txt"
        pathout = r"C:\Users\LaVision\Dropbox\PVRSEX17\RSEX17_run_list.csv"  
    elif computer == "PVAquire":
        ## PVAquire pathway
        path = r"C:\Users\PVAquire\Dropbox\PVRSEX17\RSEX17_run_list.txt"
        pathout = r"C:\Users\PVAquire\Dropbox\PVRSEX17\RSEX17_run_list.csv"
       
    names = ['Date', 'Start', 'Length', 'Sled', 'RAID0', 'RAID1', 'RAID2', 'RAID3',
           'tower_IR_16mm', 'Unnamed: 9', 'pier_IR_08mm', 'Unnamed: 11',
           'tower_EO_12mm', 'Unnamed: 13', 'pier_EO_09mm', 'Unnamed: 15', 'Notes']
    
    runlist = pd.read_csv(path, sep = "\t", skiprows = [0,1], error_bad_lines = False, dtype = "object", names = names, engine = 'python' )
    runlist = runlist.drop(labels = [col for col in runlist.columns if "Unnamed" in col], axis = 1)
    
    runlist.to_csv(pathout, index = False)
    
    ##Read the csv we just made back in and make sure it looks okay
    return pd.read_csv(pathout, dtype = "object")
    

##Now we have a dataframe from which we can print some useful stuff
#runfile1.loc[runfile1.Date.apply(lambda x: x == "1015")][["Date", "Start"]+[col for col in runfile1.columns if "mm" in col]]

def check_RAID(computer = "LaVision"):
    """
    computer == LaVision: Check files in RAID 0 and RAID 1
    computer == PVAquire: Check files in RAID 2 and RAID 3
    """
    runfile1 = read_runfile_csv(computer)
    if computer == "PVAquire":
        RAID2 = r"E:\\RSEX17\\"
        RAID3 = r"F:\\RSEX17\\"
        log, raid2, raid3 = [], [], []
        
        for date in runfile1.Date.unique():
            print(date)
            log = runfile1.loc[runfile1.Date.apply(lambda x: x == date)][["Date", "Start"]+[col for col in runfile1.columns if "RAID" in col]]
            print(log)
            try:
                raid2 = os.listdir(RAID2+date)
                print("RAID2",raid2)
            except FileNotFoundError:
                raid2 = []
                print("RAID2: None")
            try:
                raid3 = os.listdir(RAID3+date)
                print("RAID3", raid3)
            except FileNotFoundError:
                raid3 = []
                print("RAID3: None")   
            if len(log) == len(raid2): print("Raid 2 has same number of files")
            if len(log) == len(raid3): print("Raid 3 has same number of files")
    elif computer == "LaVision":
        ## Check files in RAID 0 and RAID 1    
        RAID1 = r"E:\\RSEX17\\"
        RAID0 = r"D:\\RSEX17\\"
        log, raid0, raid1 = [], [], []
        
        for date in runfile1.Date.unique():
            print(date)
            log = runfile1.loc[runfile1.Date.apply(lambda x: x == date)][["Date", "Start"]+[col for col in runfile1.columns if "RAID" in col]]
            print(log)
            try:
                raid0 = os.listdir(RAID0+date)
                print("RAID0",raid0)
            except FileNotFoundError:
                raid0 = []
                print("RAID0: None")
            try:
                raid1 = os.listdir(RAID1+date)
                print("RAID1", raid1)
            except FileNotFoundError:
                raid1 = []
                print("RAID1: None")    
            if len(log) == len(raid0): print("Raid 0 has same number of files")
            if len(log) == len(raid1): print("Raid 1 has same number of files")
            
            
def update_runlist(runlist, date, RAID = "RAID0"):
    if RAID == "RAID0":
        path = "D"
    elif RAID == "RAID1": 
        path = "E"
    elif RAID == "RAID2":
        path = "E"
    elif RAID == "RAID3":
        path = "F"
    for i in runlist.loc[runlist.Date.apply(lambda x: x == date)].index:
        if "2017"+runlist.loc[i, "Date"]+runlist.loc[i, "Start"]+".vl" in os.listdir(path+":/RSEX17/"+date):
            print("2017"+runlist.loc[i, "Date"]+runlist.loc[i, "Start"]+".vl has been downloaded and logged in csv")
            runlist.loc[i, RAID] = "y"
                
if __name__ == "__main__":
    computer = "LaVision"
#    check_RAID(computer)
#    runlist = make_runfile_csv(computer)
    runlist = read_runfile_csv(computer)
#    update_runlist(runlist, "1017")
#    update_runlist(runlist, "1018")
#    runlist.to_csv(r"C:\Users\LaVision\Dropbox\PVRSEX17\RSEX17_run_list.csv", index = False)
            