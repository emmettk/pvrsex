## Example file from Streams7
## Modified by Emmett Krupczak
## 14 Jun 2017


import SPython
print "Starting Export Script"
import sys
from sys import *
import math
from math import *
import time
from time import *

# Reduce the video by (Set to 1 for all video, set to 3 for 1/3 of video, etc.)
nReduceFactor = 3

# Choose the pathname
#szPathName = "C:\\Test\\AVIS\\"
szPathName = "C:\\StreamsExportTest2\\ReducedVideoTest\\"

# Get the active scene
hActiveScene = 0
hScene = sFindFirstScene(0, 0)
while (hScene):
	if (sIsSceneActive(hScene)):
		hActiveScene = hScene
		hScene = 0
	else:
		hScene = sFindNextScene()

# Get the movie name
szCurMovieName = sGetMovieName(0)

# Get the scene name
szCurSceneName = sGetSceneName(hActiveScene)
print "Scene name", szCurSceneName

# Go through all of the devices in this scene and make a "video" list and extract the last sound device
SoundDev = 0
VideoDevList = []

hDevice = sFindFirstDevice(0, hActiveScene)
while (hDevice):
	CurType = sGetDeviceDataType(hDevice, 1)
	if (CurType == tdVIDEO):
		VideoDevList.append(hDevice)
	if (CurType == tdSOUND):
		SoundDev = hDevice
		print "Found sound"
	hDevice = sFindNextDevice()

# Get the AVI export options
hFileFilter = sFindInstalledFilterByName(ftFILE, "AVI")

sShowFilterDialog(hFileFilter, fdtEXPORT, "")

# For each video device, export to AVI
nNumVideoDev = 0 
nNumVideoDev = len(VideoDevList)

# Select all frames for sound export to AVI
if (SoundDev != 0):
	NumSoundFrames = sGetNumRecordedFrames(0, hActiveScene, SoundDev)
	sSetDeviceViewerSelection(SoundDev, 0, NumSoundFrames - 1, 0)

for nVidIndex in xrange(nNumVideoDev):

	szDevName = sGetName(VideoDevList[nVidIndex])
	szFileName = szPathName + szCurMovieName + "_" + szCurSceneName + "_" + szDevName + ".AVI"

	DevList = []
	DevList.append(VideoDevList[nVidIndex])
	DevList.append(SoundDev)

	dwFlags = EXPORT_SHOW_PROGRESS_METER | EXPORT_USE_CONVERSION

	# Select only 1 of every 'nReduceFactor' video images
	sSetDeviceViewerSelection(VideoDevList[nVidIndex], -1, -1, 0)
	nNumImagesRecorded = sGetNumRecordedFrames(0, hActiveScene, VideoDevList[nVidIndex])
	for nImageIndex in xrange(nNumImagesRecorded):
		if (fmod(nImageIndex,nReduceFactor) == 0):
			sSetDeviceViewerSelection(VideoDevList[nVidIndex], nImageIndex, -1, 1)

	print "Starting to export file ", szFileName
	bRet = sExport(DevList, hFileFilter, szFileName, xmVIEWER_SELECTION, dwFlags)
	sleep(2)
	print "Finished exporting file ", szFileName

print "Finished Exporting: ", bRet