# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:08:33 2017

@author: PVAquire

Check for jitters in camera by comparing correlation between pairs of images
"""
import os
import pandas as pd
import numpy as np
from PIL import Image

sourcepath = "E:\\RSEX17_TIFF\\0917\\tower_EO_12mm_16bitdepth\\"
tiffs = [file for file in os.listdir(sourcepath)]

corrcoeffs = pd.DataFrame(columns = ["corrcoef"])

im = Image.open(sourcepath + tiffs[0])
imarray = np.array(im)
imflat = imarray.flatten()

t = 1
while t in range(1, len(tiffs)):
#    print("Loading", t-1, "and", t)
#    im = Image.open(sourcepath+tiffs[t-1])
    im2 = Image.open(sourcepath+tiffs[t])
    imarray2 = np.array(im2)
    imflat2 = imarray2.flatten()
    c = np.corrcoef(imflat, imflat2)[1,0]
    corrcoeffs.loc[t] = c
    print("Finished", t-1, "and", t, "with corr coeff", c)
    imflat = imflat2
    t +=1
    
#im = Image.open("E:\\RSEX17_TIFF\\0918\\tower_EO_12mm\\Movie1_Streams7_Recording_2017-09-18_11_59_33_tower_EO_12mm__00000.tif")
#im2 = Image.open("E:\\RSEX17_TIFF\\0918\\tower_EO_12mm\\Movie1_Streams7_Recording_2017-09-18_11_59_33_tower_EO_12mm__00001.tif")
#imarray = np.array(im)
#imarray2 = np.array(im2)
#imflat = imarray.flatten()
#imflat2 = imarray2.flatten()
#np.corrcoef(imflat, imflat2)