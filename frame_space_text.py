# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 13:49:12 2017

@author: ekrupczak on LaVision

Check time separation between frames from UTC file

"""
import pandas as pd
import datetime as dt
from fractions import Fraction

if __name__ == "__main__":
    camera = "tower_EO_12mm"
#    camera = "pier_EO_08mm"
#    camera = "tower_IR_16mm"
#    camera = "pier_IR_09mm"
    
    run = r"20170926_1000_towerEO_pierEO/"
#    run = r"20170926_1100_pierIR_pierEO/"
#    run = r"20170926_1200_towerIR_pierIR/"
#    run = r"20170926_1300_towerIR_towerEO/"
    
    path = r"D:/RSEX17_TIFF/0926/"+run+camera
    print("Processing",run[0:8]+run[9:13]+"_"+camera+".utc")

    utc = pd.read_csv(path+"/"+run[0:8]+run[9:13]+"_"+camera+".utc", sep = " ")
    
    utc = utc.rename(columns ={"#":"file", "of":"raw", "Frames:":"date",utc.columns[3]:"time"})
    utc = utc[["raw", "date", "time"]]
    utc["datetime"] = utc.time.apply(lambda x: dt.datetime.strptime(x[:-4]+x[-3:], "%H:%M:%S:%f"))
#    utc["minute"] = utc.raw.apply(lambda x: str(x)[-10:-9])
#    utc["sec"] =utc.raw.apply(lambda x: str(x)[-9:])
#    utc["min"] = utc.raw.apply(lambda x: int(str(x)[-9:])/60*10**7)
#    utc["timedelta"] = utc.us - utc.us.shift(1)
    utc["timedelta"] = utc.datetime - utc.datetime.shift(1)
#    print(utc.head())
    print("mean", utc.timedelta.mean().microseconds, "us.", "min", utc.timedelta.min().microseconds, "us.", 
          "max", utc.timedelta.max().microseconds, "us.", "std", utc.timedelta.std().microseconds, "us.")
    print("Frames occur every", Fraction(utc.timedelta.mean().microseconds/10**6).limit_denominator(1000), "second")