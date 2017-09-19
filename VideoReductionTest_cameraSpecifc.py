### Reduces the video and exports only every nth frame
### Exports the current Streams7 scene as TIFF files
### Author: Emmett Krupczak 
### using code borrowed from Levi ("SPythonTestMultiCamsStartTimeScript")
### and example code ("ExportMultiStreamFileReducedVideo")
### 14 Jun 2017

## 27 Jun 2017
## Choose n for each camera.

#### Things to add to this script
### Tell how long it took to export (is this 1/3 faster exporting every 3rd image, etc)
### Give a warning before adding duplicate images 


import SPython
from math import *
import os

def groupDevices():
    """
    From Levi's code.
    Get the handle for all devices in the system.
    The 0, 0 means we are not looking for a device in any
    particular movie or scene.  Just devices in the main
    Streams device list.  Each new video device will be
    added to a video device list.    
    
    Returns this video device list
    """
    vidDevList = [] # make an empty list
    GPSDev = 0
    hDev = sFindFirstDevice(0, 0)
    while hDev:
        curType = sGetDeviceDataType(hDev, 0)
        devName = sGetName(hDev)
        if curType == tdVIDEO:
            vidDevList.append(hDev)
            print('Found video device ' + devName)
        if curType == tdGPS:
            GPSDev = hDev
            print('Found GPS device ' + devName)
        hDev = sFindNextDevice()

    # Select all the video devices found above.
    sdErr = sSelectDevice(vidDevList[0], 1)
    for i in range(1, len(vidDevList)):h
        sdErr = sSelectDevice(vidDevList[i], 0)

    # print all video devices selected
    for i in range(0, len(vidDevList)):
        if sIsDeviceSelected(vidDevList[i]):
            print('Device ' + sGetName(vidDevList[i]) + ' selected for video')

    # Group all selected devices
    gsdErr = sGroupSelectedDevices('VideoGroup')
    return vidDevList

def getActive(verbose = True):
    """
    verbose = True: Prints active movie and scene name
    returns movie name, scene name
    """
    activeScene = sGetActiveScene()
    activeMovie = sGetActiveMovie()
    if verbose: 
        print("Scene: "+sGetSceneName(activeScene))
        print("Movie: "+ sGetMovieName(activeMovie))
    return sGetMovieName(activeMovie), sGetSceneName(activeScene)

def getActiveScene():
    """
    Get the active scene
    Copied from Streams7 example; seems overly complicated
    Why not use sGetActiveScene()?
    """
    hActiveScene = 0
    hScene = sFindFirstScene(0, 0)
    while (hScene):
    	if (sIsSceneActive(hScene)):
    		hActiveScene = hScene
    		hScene = 0
    	else:
    		hScene = sFindNextScene()
    return hActiveScene

def exportScene(vidDevList, exportPath, fileType = "TIFF", nReduceFactor = 3, nReduceDict = {}):
    """
    Adapted from Levi's code and example code
    Exports current scene as TIFF files to location given by exportPath
    nReduceFactor is the period with which to export frames (eg 3 means every third frame, etc)
    """
    hExport = sFindInstalledFilterByName(ftFILE, fileType)

    # make a word with flags for exporting.  This is done by
    # XORing the various desired flags together.  In this
    # case there will be a new file for each frame, and the
    # export progress meter will show.
    exportFlags = EXPORT_SEPARATE_FILES_PER_FRAME | EXPORT_SHOW_PROGRESS_METER

    expMovieName, expSceneName = getActive(verbose = False)
    print('Start Export: ' + sGetTimeString(sGetCurrentTime()))
    for device in vidDevList:
        if sGetName(device) in nReduceDict.keys():
            nReduceFactor = nReduceDict[sGetName(device)]
        print("Exporting every " + str(nReduceFactor)+"th frame")
#        exportOneDevice(device, nReduceFactor, exportPath, fileType, expMovieName, expSceneName, hExport)
        expDevName = sGetName(device)
        nNumImagesRecorded = sGetNumRecordedFrames(0, getActiveScene(), device)
        print("Number of frames recorded: "+str(nNumImagesRecorded))
        imgsaved =0
        ## Set device viewer selection to empty for first image
        ## Causes the first frame to be saved, which should always be the case anyway
        sSetDeviceViewerSelection(device, 0, 0, 0)
        for nImageIndex in xrange(nNumImagesRecorded):
            if fmod(nImageIndex, nReduceFactor) == 0:
                imgsaved +=1
                ### Keep current selection
                sSetDeviceViewerSelection(device, nImageIndex, nImageIndex, 1)
        print("Frames saved after mod "+str(nReduceFactor)+": "+ str(imgsaved))  
        expFName = exportPath + expMovieName + '_' + expSceneName + '_' + expDevName + '_'
        print(expFName)
        eErr = sExport([device], hExport, expFName, xmVIEWER_SELECTION, exportFlags)
    print('End Export: ' + sGetTimeString(sGetCurrentTime()))
    
def exportOneDevice(device, nReduceFactor, exportPath, fileType, expMovieName, expSceneName, hExport):
    expDevName = sGetName(device)
    print("Exporting device "+expDevName)
    nNumImagesRecorded = sGetNumRecordedFrames(0, getActiveScene(), device)
    print("Number of frames recorded: "+str(nNumImagesRecorded))
    imgsaved =0
    ## Set device viewer selection to empty for first image
    ## Causes the first frame to be saved, which should always be the case anyway
    sSetDeviceViewerSelection(device, 0, 0, 0)
    for nImageIndex in xrange(nNumImagesRecorded):
        if fmod(nImageIndex, nReduceFactor) == 0:
            imgsaved +=1
            ### Keep current selection
            sSetDeviceViewerSelection(device, nImageIndex, nImageIndex, 1)
    print("Frames saved after mod "+str(nReduceFactor)+": "+ str(imgsaved))  
    expFName = exportPath + expMovieName + '_' + expSceneName + '_' + expDevName + '_'
    print(expFName)
    eErr = sExport([device], hExport, expFName, xmVIEWER_SELECTION, exportFlags)
    

def addExportDir(exportPath, inputok = True):
    """
    Confirms that chosen export directory exists and, if not, attempts to create it.
    If inputok == True, will offer a warning before adding files to a non-empty directory and give the opportunity to enter an alternative path
    Streams7 does not support console input
    """
    if not os.path.exists(exportPath):
        try:
            os.mkdir(exportPath)
            print("Made directory "+exportPath)
            return True
        except FileNotFoundError:
            print("Invalid Path")
            return False
    elif inputok and os.listdir(exportPath):
        addfiles = input("Warning: Directory "+exportPath+" is not empty. Would you like to continue? Type 'y' to add files to this directory, type 'n' to choose a new directory, type anything else to quit. ")
        if addfiles == "y":
            print("Adding files to "+exportPath)
        elif addfiles == "n":
            newpath = input("Please input a new directory path: ")
            ## Recursive step!
            addExportDir(newpath)
        else:
            print("Quitting")
            return False
    else:
        print("Export directory successfully chosen to be "+exportPath)
        return True
            
def main(exportPath, nReduceDict):
    print("Running video export test script.")
    if addExportDir(exportPath, inputok = False):
        vidDevList = groupDevices()
        print("Devices identified and grouped")
        getActive()
#        print("Exporting every "+str(nReduceFactor)+"th frame")
        exportScene(vidDevList, exportPath, fileType = "TIFF", nReduceDict = nReduceDict)

if __name__ == "__main__":
    exportPath = "C:\\StreamsExportTest2\\ReducedVideoTest10\\"
    nReduceDict = {"Tower_16mm": 100, "Pier_9mm": 200}
#    nReduceFactor = 300
    main(exportPath, nReduceDict = nReduceDict)
    
    
    
##################################################
## Notes and problems
### When running this in Stream7, it does not always update nReduceFactor appropriately. 
### Multiple runs will continue to use the old factor despite saving/reopening file
### This is caused by not clearing the viewer selection - set last argument (bKeepCurrentSelection) to False in SetDeviceViewerSelection before adding more images
