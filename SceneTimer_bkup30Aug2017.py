# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:09:14 2017

@author: Emmett Krupczak

Have Streams7 record from all devices, starting a new scene every n seconds. 

"""

import SPython
import datetime as dt
import time

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


def setStopCondition(vidDevList, count, trigger = "time"):
    """
    Takes a frame count (trigger = "frames")
    or a time count in milliseconds (trigger = "time")
    """
    # Set a recording condition to stop recording after 
    # nFrames number of frames.  First, remove all previous
    # stopping conditions. Next, set a stopping condition on 
    # all video devices that stops a recording after nFrames.  
    rarscErr = sRemoveAllRecordStoppingConditions()
    for i in range(0, len(vidDevList)):
        if trigger == "frames":
            arscErr = sAddRecordStoppingCondition(vidDevList[i], rscSTOP_ON_FRAME_COUNT, 0, 0, count)
        elif trigger == "time":
            arscErr = sAddRecordStoppingCondition(vidDevList[i], rscSTOP_AFTER_TIME, 0, 0, count)
        else: print("ERROR. INVALID TRIGGER")

    print('All video devices will stop after ' + str(nFrames) + ' frames')
    
    
def recordScene(vidDevList):
    """
    Record a scene and return its handle
    Adapted from Levi
    """
    # start a recording. Pause program execution until
    # the recording is finished.
    print('Recording....')
    rErr = sRecord(swoWAIT_TO_FINISH)
    
    # get the handle of the current active scene.  This
    # should be the scene we just recorded.
    hScene = sGetActiveScene()
    return hScene

def nameScene(hScene, vidDevList):
    """
    Print number of frames and scene start time
    Name scene after start time
    Adapted from Levi
    """
    # Get the number of frames recorded from the current movie,
    # the active scene, and all devices. Print this
    # to the screen.
    for i in range(0, len(vidDevList)):
    	numFramesRecorded = sGetNumRecordedFrames(0, hScene, vidDevList[i])
    	print(str(numFramesRecorded) + ' Frames Recorded on ' + sGetName(vidDevList[i]))
    
    # Get the start time of the recorded scene to set the 
    # scene name.  First get the Scene start time in Streams
    # time (number of 100 nanoseconds since Jan, 1 1601).
    # next convert it into standard unix time (seconds 
    # since Jan 1, 1970). Then convert unix time to a 
    # date and time string. Print the date and time of the
    # start of the scene.
    streamsSceneTime = sGetSceneStartTime(hScene)
    pythonSceneTime = sConvertStreamsToPythonTime(streamsSceneTime)
    pythonSceneTimeString = time.ctime(pythonSceneTime)
    print('The active scene started on ' + sGetTimeString(streamsSceneTime))
    
    # construct a string that is hhmmss from the date
    # and time string.  Print this to the screen.  Next
    # set the name of the recorded scene in the active movie to 
    # hhmmss of the start of the scene.
    sceneName = pythonSceneTimeString[11:13] + pythonSceneTimeString[14:16] + pythonSceneTimeString[17:19]
    print('Active scene name set to ' + sceneName)
    ssnErr = sSetSceneName(0, hScene, sceneName)

def compute_runtime(length, buffer):
    """
    Takes a length as a time delta and a buffer in seconds 
    Returns number of miliseconds equal to length - buffer
    """
    return (length.total_seconds() - buffer)*1000


if __name__ == "__main__":
    starttime = dt.datetime(2017, 8, 29, 17, 0, 0)
    stoptime = dt.datetime(2017, 8, 30, 7, 0,0)
    sceneTime = dt.timedelta(seconds = 30)
#    runtime = 30*60*60*2 #30fps, two hour increments
    runtime = compute_runtime(dt.timedelta(minutes = 2), 30)
    
    vidDevList = groupDevices()
    setStopCondition(vidDevList, runtime, trigger = "time")
    waittime = (starttime-dt.datetime.today()).total_seconds()
    if waittime>0:
        print("Waiting "+str(waittime)+" sec to start")
        time.sleep(waittime)
    
    while starttime < dt.datetime.today() < stoptime:
        hScene = recordScene(vidDevList)
        nameScene(hScene, vidDevList)
        print("Scene recorded at"+str(dt.datetime.today()))
#        print(dt.datetime.today())
    
    