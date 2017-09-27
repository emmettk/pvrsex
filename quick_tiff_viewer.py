# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:39:12 2017

@author: ekrupczak on PVAquire

Quickly display in console all figures in directory
"""
import os
import numpy as np
from PIL import Image
import pylab as plt




def view_tiffs(tiffs, path):
    """
    Display tiffs in console
    """
#    tiffs = [file for file in os.listdir(path) if ".TIF" in file]

    for f in tiffs:
        plt.figure()
        plt.title(f)
        plt.imshow(np.array(Image.open(path+f)))
        
def rescale_tiffs(tiffs, path, savepath, bits = 10):
    """
    Rescale tiffs from X bits to 16 bits
    Save as new images
    """
#    tiffs = [file for file in os.listdir(path) if ".TIF" in file]

    for f in tiffs:
        img = np.array(Image.open(path+f))        
        imgrescale = img*2**(16-bits)
        result = Image.fromarray(imgrescale)
        result.save(savepath+"rescaled_"+f)
        
if __name__ == "__main__":
#    path = "E:\\FiberLineTest\\A34_EO\\corrupted_frames_log\\"
#    path = "E:\\PierJitterTest\\20170923_pierEO\\corrupted_frames_log\\"
#    tiffs = [file for file in os.listdir(path) if ".TIF" in file]
#    rescale_tiffs(tiffs, path, bits = 10) 
    
#    print("Number of corrupted frames: ", len(tiffs))


    path  = "E:\\PierJitterTest\\20170923_pierEO\\"
    tiffs = [file for file in os.listdir(path) if ".TIF" in file]
    tifflist = [t for t in tiffs if t[-9:-4] in [str(frame) for frame in range(14428, 14441)]]
    rescale_tiffs(tifflist, path, path+"corrupted_frames_log\\14428_14440\\", bits = 10)