### Export only
### Exports the current Streams7 video as TIFF files
### Author: Emmett Krupczak using code borrowed from Levi ("SPythonTestMultiCamsStartTimeScript")
### 14 Jun 2017

import SPython

exportPath = "C:\\StreamsExportTest2\\VideoExportTest\\"

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
    for i in range(1, len(vidDevList)):
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

def exportScene(vidDevList, exportPath, fileType = "TIFF"):
    """
    From Levi's code.
    Exports current scene as TIFF files to location given by exportPath
    """
    hExport = sFindInstalledFilterByName(ftFILE, fileType)

    # make a word with flags for exporting.  This is done by
    # XORing the various desired flags together.  In this
    # case there will be a new file for each frame, and the
    # export progress meter will show.
    exportFlags = EXPORT_SEPARATE_FILES_PER_FRAME | EXPORT_SHOW_PROGRESS_METER

    expMovieName, expSceneName = getActive(verbose = False)
    print('Start Export: ' + sGetTimeString(sGetCurrentTime()))
    for i in range(0, len(vidDevList)):
        expDevName = sGetName(vidDevList[i])
        expFName = exportPath + expMovieName + '_' + expSceneName + '_' + expDevName + '_'
        print(expFName)
        eErr = sExport([vidDevList[i]], hExport, expFName, xmENTIRE_SCENE, exportFlags)
    print('End Export: ' + sGetTimeString(sGetCurrentTime()))

def main():
    print("Running video export test script.")
    vidDevList = groupDevices()
    print("Devices identified and grouped")
    getActive()
    exportScene(vidDevList, exportPath)

if __name__ == "__main__":
    main()