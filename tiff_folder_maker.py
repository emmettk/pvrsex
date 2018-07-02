# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 19:08:14 2018

@author: ekrupczak on LaVision

Script to make folders for storing tiffs

"""
import os
import datetime as dt
import pandas as pd

def make_tiff_folders(path_to_tiffs, start_time_list, camera_name):
    '''
    Makes tiff folders in path_to_tiffs of the following format: 
        <TIFF_Folder>/MMDD/YYYYMMDD/YYYYMMDD_camera_name
    Makes one folder for each time in the start_time_list
    start_time_list should be a list of datetime objects
    '''
    for time in start_time_list:
        
        path = (path_to_tiffs + '/'+ time.strftime('%m%d')+'/'
                +time.strftime('%Y%m%d%H%M')+'/'
                +time.strftime('%Y%m%d%H%M')+'_'+camera_name)
        if not os.path.isdir(path):
            print("Making", path)
            os.makedirs(path)
        else: print("Already Exists:", path)
        
        
if __name__ == "__main__":
    path_to_tiffs = 'D:/RSEX17_TIFF'
    camera_name = 'towerEO'
    start_time_list = pd.date_range(start = dt.datetime(2017,10,16,14,30), end = dt.datetime(2017,10,17,15,00), freq = '30T' )
    #start_time_list = pd.date_range(start = dt.datetime(2017,10,20,8,30), end = dt.datetime(2017,10,20,11,30), freq = '30T' )
    make_tiff_folders(path_to_tiffs, start_time_list, camera_name)