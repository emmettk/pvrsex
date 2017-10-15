# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 09:25:11 2017

@author: ekrupczak at LaVision

Take a utc file and return the frame number closest to a chosen time

"""
import pandas as pd
import datetime as dt


def find_closest_frame(utc, timestamp):
    """
    Takes timestamp as datetime object, returns the frame number corresponding to the cloest frame to that time
    Briefly sets the index to datetime column, then sets it back
    """
    index_holder = utc.index
    utc.index = utc.datetime
    closest_loc = utc.index.get_loc(timestamp, method = "nearest")
    utc.index = index_holder
    return closest_loc


if __name__ == "__main__":
    path = r'D:/RSEX17_TIFF/1005/201710051000/pier_EO_08mm/'
    utc_file = '201710051000_pier_EO_08mm.utc'
    
#    path = r'D:/RSEX17_TIFF/1005/201710051000/tower_EO_12mm/'
#    utc_file = '201710051000_tower_EO_12mm.utc'
    date = dt.date(2017, 10, 5)
    utc = pd.read_table(path+utc_file, sep = ' ')
    utc = utc.rename(columns ={"#":"file", "of":"raw", "Frames:":"date",utc.columns[3]:"time"})
    utc = utc[["raw", "date", "time"]]
    utc["datetime"] = utc.time.apply(lambda x: dt.datetime.combine(date, dt.datetime.strptime(x[:-4]+x[-3:], "%H:%M:%S:%f").time()))   
    
#    index = find_closest_frame(utc, dt.datetime(2017, 10, 5, 10, 2))

    timelist = [dt.time(10, 2), dt.time(10, 8), dt.time(10, 12), dt.time(10, 15), dt.time(10, 18), 
                dt.time(10, 25), dt.time(10, 32), dt.time(10, 42), dt.time(11, 9), dt.time(11, 17), 
                dt.time(11, 19), dt.time(11, 25), dt.time(11, 27), dt.time(11, 35)]
    
    datetimelist = [dt.datetime.combine(date,file) for file in timelist]
    
    df = pd.DataFrame(columns = ["frame_index_num"])
    for dtl in datetimelist:
        df.loc[dtl] = find_closest_frame(utc, dtl)
        
    scaling_constant = 2
    
    ##Frame number is x, sampled every nth frame, so new frame number is x/n, rounded
    
    df["davis_image_num"] = df.frame_index_num.apply(lambda x: round(x/scaling_constant))
    df.index.rename("datetime", inplace = True)
    df.to_csv(path+utc_file[:-4]+"_rip_current_frame_numbers.csv")