"""
@file start.py

@author Michael Dittman

Start script to serve as a debug interface for the camera and radar acquisition modules


"""

import os
import time
import camera

# Print statements are currently placeholders for calls to the CLI executables

print("Starting FPGA Configuration...")
#os.system("DCA CALL")
time.sleep(3)

print("Setting up record delay...")
#os.system("DCA CALL")
time.sleep(3)

print("Starting Radar Acquisition...")
#os.system("DCA CALL")
time.sleep(3)

print("Starting Camera Acquisition")
camera.start_video_acquisition_timed()
