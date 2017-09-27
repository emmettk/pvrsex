# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:08:33 2017

@author: PVAquire

Check for jitters in camera by comparing correlation between pairs of images
"""
import os
import shutil
import pandas as pd
import numpy as np
from PIL import Image
import pylab as plt

#sourcepath = "E:\\RSEX17_TIFF\\0919\\tower_EO_12mm\\"
sourcepath = "E:\\FiberLineTest\\B34_EO\\"
sourcepath = "E:\\PierJitterTest\\20170923_pierIR\\"
#sourcepath = "E:\\RSEX17_TIFF\\0919\\tower_EO_12mm\\"
#subdir = ["A12_EO", "A12_IR", "A34_EO", "A34_IR", "B34_EO", "B34_IR"]

tiffs = [file for file in os.listdir(sourcepath)]




#### Make a dataframe with the correlation coefficients for all adjacent tiff pairs

corrcoeffs = pd.DataFrame(columns = ["filename", "corrcoeff"])
threshold = 0.9 ## Correlation coefficient less than 0.9 indicates a jitter

### Prevent duplicate loading of each frame so it goes faster
im = Image.open(sourcepath + tiffs[0])
imarray = np.array(im)
imflat = imarray.flatten()

t = 1
while t in range(1, len(tiffs)):
#    print("Loading", t-1, "and", t)
    im2 = Image.open(sourcepath+tiffs[t])
    imarray2 = np.array(im2)
    imflat2 = imarray2.flatten()
    c = np.corrcoef(imflat, imflat2)[1,0]
    corrcoeffs.loc[t] = [tiffs[t], c]
#    if c < threshold:
    print("Finished", t-1, "and", t, "with corr coeff", c)
    imflat = imflat2
    t +=1

##### Get the corrupted tiff file names and write them to a text file

corrupted_df = corrcoeffs.loc[corrcoeffs["corrcoeff"]<threshold]

### There will be two poorly correlated frame pairs for each corrupted frame; 
### the first number of each pair is the corrupted frame itself. 
### So take every other line of the data frame. 
corrupted_frames = corrupted_df.iloc[::2,:]

corrupted_frames.insert(0, "frame", corrupted_frames.index)

### Write the corrupted frame list to a file
logpath = sourcepath + "corrupted_frames_log\\"
if not os.path.exists(logpath): os.mkdir(logpath)

corrcoeffs.to_csv(logpath+"correlation_coefficients.csv")
corrupted_frames.to_csv(logpath+"corrupted_frames_list.csv")

##Display corrupted frames in the console and copy corrupted frames to directory
print("Corrupted frames:")
for f in corrupted_frames["filename"]: 
    plt.figure()
    plt.title(f)
    plt.imshow(np.array(Image.open(sourcepath+f)))
    shutil.copy2(sourcepath+f, logpath)
    

