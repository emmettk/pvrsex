# SPythonTestMultiCamsStartTimeScript.py
# Written Oct 15, 2016 by Levi Gorrell
# This version modified by Emmett Krupczak
# Updated 14 Jun 2017
# Last updated 29 Aug 2017

# ======================================
# This is a script used to test recording at a certain time
# with multiple devices on the DVR.  This script will find
# all active devices and then wait until the time
# specified by the variables YEAR, MONTH, DAY, HOUR, 
# MINUTE, SECOND to take video with a set number of 
# frames (defined by nFrames) on all video devices. If
# the start time is past, recording starts immediatly. 
# When done, the active scene is renamed hhmmss of the 
# start of the scene and all video from the active scene 
# is exported to TIFF files in a set directory (defined 
# by expPath)  
# ========================================

# Import Libraries
import SPython
import time
from datetime import date
import sys

# set the time to sample for


# set the number of frames to sample for
nFrames = 100

# Set the export path name
#expPath = 'd:\\10181900\\'
expPath = 'c:\\StreamsExportTest3\\'

# Input the date and time to wait for.  All inputs are
# integer values.
YEAR = 2017
MONTH = 8
DAY = 29
HOUR = 9
MINUTE = 46
SECOND = 0

# Create a date object for the date given above.  Get the
# day of the week and day of the year for the time tuple.
d = date(YEAR, MONTH, DAY)
WEEKDAY = d.weekday()
YEARDAY = d.toordinal() - date(YEAR, 1, 1).toordinal() + 1

# Create the needed time tuple and get the time in seconds.
# The time in seconds is a floating point number.
timeTuple = (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, WEEKDAY, YEARDAY, -1)
startSeconds = time.mktime(timeTuple)

# Convert the time in seconds of the start date and time to
# streams time (number of 100 nanoseconds from Jan 1 1601).
# have streams compute the date string from the streams time
# and print it to verify that it is the same start date and
# time as inputted above.
streamsStartSeconds = sConvertPythonToStreamsTime(startSeconds)
print('Starting on ' + sGetTimeString(streamsStartSeconds))

# get the handle for all devices in the system.
# The 0, 0 means we are not looking for a device in any
# particular movie or scene.  Just devices in the main
# Streams device list.  Each new video device will be
# added to a video device list.
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
        print('Frame Rate' + sGetRecordFrameRateValue(vidDevList[i])) 

# Group all selected devices
gsdErr = sGroupSelectedDevices('VideoGroup')

# Set a recording condition to stop recording after 
# nFrames number of frames.  First, remove all previous
# stopping conditions. Next, set a stopping condition on 
# all video devices that stops a recording after nFrames.  
rarscErr = sRemoveAllRecordStoppingConditions()
for i in range(0, len(vidDevList)):
	arscErr = sAddRecordStoppingCondition(vidDevList[i], rscSTOP_ON_FRAME_COUNT, 0, 0, nFrames)
print('All video devices will stop after ' + str(nFrames) + ' frames')

# Compute the number of seconds to wait until the start time.
# The current time is taken from the current streams time.
# Need to multiply by 10^-7 to go from 100 nanosecond
# intervals to seconds.  Print how many seconds to wait.
secondsDiff = float(streamsStartSeconds - sGetCurrentTime()) * 1e-7
print('waiting for ' + str(secondsDiff) + ' seconds')

# Wait until the start time, unless the start time is already
# past.  If the start time is past, start now.
if secondsDiff >= 0:
	time.sleep(secondsDiff)

# start a recording. Pause program execution until
# the recording is finished.
print('Recording....')
rErr = sRecord(swoWAIT_TO_FINISH)

# get the handle of the current active scene.  This
# should be the scene we just recorded.
hScene = sGetActiveScene()

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

# Get the handle of the TIFF file exporting filter.
# print the filter name to the screen
hExport = sFindInstalledFilterByName(ftFILE, 'TIFF')
filtName = sGetName(hExport)
print('Using Export Filter ' + filtName)

# Get movie name and scene name for constructing the
# export file name
expMovieName = sGetMovieName(0)
expSceneName = sGetSceneName(hScene)

# make a word with flags for exporting.  This is done by
# XORing the various desired flags together.  In this
# case there will be a new file for each frame, and the
# export progress meter will show.
exportFlags = EXPORT_SEPARATE_FILES_PER_FRAME | EXPORT_SHOW_PROGRESS_METER

# Export all frames in the active scene from the 
# listed devices.  with sExport, only the active scene
# is exported from.
print('Start Export: ' + sGetTimeString(sGetCurrentTime()))
for i in range(0, len(vidDevList)):
	expDevName = sGetName(vidDevList[i])
	expFName = expPath + expMovieName + '_' + expSceneName + '_' + expDevName + '_'
	print(expFName)
	eErr = sExport([vidDevList[i]], hExport, expFName, xmENTIRE_SCENE, exportFlags)
print('End Export: ' + sGetTimeString(sGetCurrentTime()))