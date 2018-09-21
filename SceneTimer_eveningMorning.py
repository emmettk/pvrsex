# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:09:14 2017
Modified from SceneTimer_loopSleep.py on 18 Sep 2018.

@author: Emmett Krupczak

Have Streams7 record from all devices, starting a new scene every n seconds. 
Use Streams time rather than system time
If the wait before recording is greater than 1 hr, recalibrate the pause at 30 min and 5 min before the start time.

Add a loop to the sleep so the script can be killed at any time (Streams only allows a script to be killed after finishing current line)
This may subsume the 30 min and 5 min checks. 

Allow for both evening and morning run times to be set.

Version 20 Sep 2018 - No longer calls them "evening" and "morning" runs
"""

import SPython
import datetime as dt
import time
import math

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


def setStopCondition(vidDevList, count, trigger = "ms"):
    """
    Takes a frame count (trigger = "frames")
    or a time count in milliseconds (trigger = "ms")
    """
    # Set a recording condition to stop recording after 
    # nFrames number of frames.  First, remove all previous
    # stopping conditions. Next, set a stopping condition on 
    # all video devices that stops a recording after nFrames.  
    rarscErr = sRemoveAllRecordStoppingConditions()
    for i in range(0, len(vidDevList)):
        if trigger == "frames":
            arscErr = sAddRecordStoppingCondition(vidDevList[i], rscSTOP_ON_FRAME_COUNT, 0, 0, count)
        elif trigger == "ms":
            arscErr = sAddRecordStoppingCondition(vidDevList[i], rscSTOP_AFTER_TIME, 0, count, 0)
        else: print("ERROR. INVALID TRIGGER")

    print('All video devices will stop after ' + str(count) + ' '+ trigger)
    
    
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

def make_starttime_list(starttime, stoptime, scenetime, pausetime = dt.timedelta(minutes = 0)):
    """
    Return a list of start times using the first start time, stop time, and scene time
    Accepts datetimes and time delta for scene time
    """
    startlist = [starttime]
    while startlist[-1]+scenetime+pausetime < stoptime:
        startlist.append(startlist[-1]+scenetime+pausetime)
    return startlist

def get_current_time_from_Streams():
    current = sGetCurrentTime()
#    print("streamstime", current)
    python = sConvertStreamsToPythonTime(current)
#    print("python time", python)
    dttime= dt.datetime.fromtimestamp(python)
#    print("datetime", dttime)
    return dttime
    

def wait_to_start(starttime):
    #update current time
    today = get_current_time_from_Streams()
    print("\nChecking wait time.")
    print("The current time from Streams is "+str(today))
    print("The current system time is "+str(dt.datetime.today()))
    #Check how far we are from start
    waittime = (starttime-today).total_seconds()
    if waittime>0:
        if waittime > 60:
            print("Waiting "+str(waittime/60)+" min to start")
        elif waittime > 3600:
            print("Waiting "+str(waittime/3600)+" hr to start")
        else: print("Waiting "+str(waittime)+" sec to start")
    if waittime>= 60*60: ## an hour
        print("Wait time will be updated again at approximately "+str(starttime-dt.timedelta(seconds = 60*30)))
        sleep_loop(waittime - 60*30) ## check 30 minutes before end of wait time
        wait_to_start(starttime)
    elif waittime >=  60*20: ## 20 min
        print("Wait time will be updated again at approximately "+str(starttime - dt.timedelta(seconds = 60*5))) 
        sleep_loop(waittime-60*5) ## check 5 minutes before end of waittime 
        wait_to_start(starttime)
    elif waittime>0:
        sleep_loop(waittime)
        
def sleep_loop(waittime, increment = 5):
    """
    waittime - time to pause total
    increments to pause for each time - script can be broken in Streams with this frequency
    """
    for pause in range(0, int(math.floor(waittime/increment))):
#        print(pause, pause*increment, dt.datetime.today())
        time.sleep(increment)
#    print(pause, pause*(increment+1), dt.datetime.today())
    time.sleep(waittime%increment)
#    print("end", dt.datetime.today())
        
def run(starttime, stoptime, scenetime, pausetime = dt.timedelta(minutes = 0), buffertime = 30):
    """ 
    perform a camera run starting at starttime, ending at stoptime, with scenes of length scenetime
    and delays between scenes of length pausetime + buffertime
    Note: 30 seconds is about the minimum buffertime for Streams7 to fully close and reopen a scene
    """

    runtime = compute_runtime(scenetime, buffertime)
    startlist = make_starttime_list(starttime, stoptime, scenetime, pausetime)

    print("Start time list: " + str(startlist))
    vidDevList = groupDevices()
    setStopCondition(vidDevList, runtime, trigger = "ms")    
    
    print("Start time: " + str(starttime))
    print("Stop time: "+ str(stoptime))
    
    #### Wait to start
    wait_to_start(starttime)

    ### Start at specified times
    ### For sub-minute runs, this will jump the gun. (if, eg, the run starts at 15:00:00 and ends at 15:00:34, this check will show that current time rounded to a minute still equals 15:00:00 and it restarts)
    current = get_current_time_from_Streams()
#    print("entering loop", current)
    print("\nPreparing to record at "+str(current))
    while starttime <= current <= stoptime:
#        print(current, dt.datetime.today())
        now = dt.datetime.combine(current, dt.time(current.hour, current.minute))
        if now in startlist:
            print("Scene recording triggered at " + str(get_current_time_from_Streams()))
            hScene = recordScene(vidDevList)
            nameScene(hScene, vidDevList)
            print("Scene recording complete at "+str(get_current_time_from_Streams()))
        current = get_current_time_from_Streams()


if __name__ == "__main__":

### Run 1
    starttime1 = dt.datetime(2018, 9, 20, 8, 10, 0)
    stoptime1 = starttime1 +dt.timedelta(hours = 1, minutes = 50)
    scenetime1 = dt.timedelta(hours = 1, minutes = 50)
    pausetime1 = dt.timedelta(minutes = 0)
    buffertime1 = 30 #seconds between runs

### Run 2
    starttime2 = dt.datetime(2018, 9, 20, 9, 0, 0)
    stoptime2 = starttime2 +dt.timedelta(hours = 8, minutes = 0)
    scenetime2 = dt.timedelta(hours = 2, minutes = 0)
    pausetime2 = dt.timedelta(minutes = 0)
    buffertime2 = 30 #seconds between runs

### Do the first run 
    run(starttime1, stoptime1, scenetime1, pausetime1, buffertime1)

### Do the second run 
    run(starttime2, stoptime2, scenetime2, pausetime2, buffertime2)


       
