####################################################################################################
#Code from Sudharshan and TI for connecting COM Ports and sending Configuration file (need to test)
####################################################################################################
import struct
import sys
import serial
import binascii
import time
import numpy as np
import math

class uartParserSDK():
    """
    find various utility functions here for connecting to COM Ports, send data, etc...
    connect to com ports
    Call this function to connect to the comport.
    This takes arguments self (intrinsic), uartCom, and dataCom. No return, but sets internal variables in the parser object.
    """

    def __init__(self):
        """
        Initialize a uart_parser
        """
        self.capon3D = 0
        self.aop = 0
        #self.uartCom = serial.Serial()
        #self.dataCom = serial.Serial()
        self.cfg = None

    def connect_com_ports(self, uartCom, dataCom):
        """
        Connect the COM Ports
        :param uartCom: Uart Port value or folder
        :param dataCom: dataCom value or folder
        :return:
        """

        # Set the uartCom as a serial object
        # For linux this will end up looking like ... serial.Serial('/dev/ttyS1', 19200, timeout=1)
        self.uartCom = serial.Serial(uartCom, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.3)
        self.dataCom = serial.Serial(dataCom, 921600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.025)
        print(self.uartCom.name + " Connected")
        print(self.dataCom.name + " Connected")

    def get_cfg(self, path):
        """
        Get the cfg file
        :param path:
        :return:
        """

        # Set the file pointer to the file indicated by the path and enable it as read
        self.cfg = open(path, 'r')

    def send_cfg(self):
        """
        Send the chirp configuration file to the antenna
        :param cfg: The file pointer of the chirp congiruation
        :return: None
        """

        print("Sending config file...")

        # For every line in the config file
        for line in self.cfg:
            print(line)
            #time.sleep(.1)
            self.uartCom.write(line.encode())
            ack = self.uartCom.readline()
            print(ack)
        time.sleep(3)
        self.uartCom.reset_input_buffer()
        self.uartCom.close()
    
    
####################################################################################################
#Camera Code developed by us (Team 4 from MSU)
####################################################################################################
import numpy as np
import os
import time
import cv2

filename = 'video.avi'
frames_per_second = 24.0
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def start_video_acquisition():
    """
    Function that starts video acquisition. This will serve as the entry point
    to the camera data
    :return: None
    """
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def start_video_acquisition_timed(seconds=10):
    """
    Function that starts video acquisition. This will serve as the entry point
    to the camera data
    :param seconds: The number of seconds to capture video for (Default value of 10 seconds)
    :return: None
    """

    # Get the current time
    start_time = time.time()

    # Store the elapsed time
    elapsed_time = time.time() - start_time

    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

    # While the amount of time passed is less than how long we want to record video for
    while elapsed_time < seconds:

        # Capture the frame
        ret, frame = cap.read()

        # Write the frame to the screen (not necessary for Released version)
        out.write(frame)

        # Font for time
        font = cv2.FONT_HERSHEY_SIMPLEX

        # What is the current time?
        current_time = time.gmtime(time.time())

        # Format the time
        current_time_formatted = str(time.strftime("%Y-%m-%d %H:%M:%S", current_time))

        cv2.putText(frame, current_time_formatted, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Show the frame on the screen
        cv2.imshow('frame', frame)

        # Calculate the time elapsed
        elapsed_time = int(time.time() - start_time)

        # Allow for break key (testing on windows)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def configure_fpga(json_file_path):
    """
    API function to call from interface to configure the fpga with a given json_file
    Special notes : This function does not properly format the json_file_path. It is assumed
    that all paths passed to this function are well-formed
    :param json_file_path: The json file the use to configure the fpga
    :return: None
    """

    print("Configuring fpga...")
    os.system("./DCA1000EVM_CLI_Control fpga " + json_file_path)
    time.sleep(1)

# Individual functions that can be used to configure the board


def record_delay(json_file_path):
    """
    API function to call from interface to configure the record delay with a given json_file
    Special notes : This function does not properly format the json_file_path. It is assumed
    that all paths passed to this function are well-formed
    :param json_file_path: The json file the use to configure the record delay
    :return: None
    """

    print("Configuring record delay...")
    os.system("./DCA1000EVM_CLI_Control record " + json_file_path)
    time.sleep(1)


def start_record(json_file_path):
    """
    API function to call from interface to start a radar record with a given json file
    Special notes : This function does not properly format the json_file_path. It is assumed
    that all paths passed to this function are well-formed
    :param json_file_path: The json file the used to start a record
    :return: None
    """

    print("Starting record")
    os.system("./DCA1000EVM_CLI_Control start_record " + json_file_path)
    time.sleep(1)


def stop_record(json_file_path):
    """
    API function to call from interface to stop a radar record with a given json file
    Special notes : This function does not properly format the json_file_path. It is assumed
    that all paths passed to this function are well-formed
    :param json_file_path: The json file the used to stop a record
    :return: None
    """

    print("Stopping record")
    os.system("./DCA1000EVM_CLI_Control stop_record " + json_file_path)
    time.sleep(1)
# In order to have a proper startup sequence 3 commands from the CLI must be called. fpga, record, start_record
# Instead of using the above individual commands, minus the stop_record command. The startup sequence can be
# called


def radar_record_start(json_file_path):
    """
    Function to intitiate the startup sequence of a radar record
    Special notes : This function does not properly format the json_file_path. It is assumed
    that all paths passed to this function are well-formed
    :param json_file_path: The json file the used to stop a record
    :return:
    """

    # FPGA

    print("Resetting AR device...")
    os.system("./DCA1000EVM_CLI_Control reset_ar_device " + json_file_path)

    print("Configuring fpga...")
    os.system("./DCA1000EVM_CLI_Control fpga " + json_file_path)
    time.sleep(1)

    # Record delay
    print("Configuring record delay...")
    os.system("./DCA1000EVM_CLI_Control record " + json_file_path)
    time.sleep(1)

    # Start_record
    print("Starting record...")
    os.system("./DCA1000EVM_CLI_Control start_record " + json_file_path)
    time.sleep(1)

    print("Starting camera record...")
    start_video_acquisition_timed()
    


def connect_com_ports(uartCom, dataCom):
	"""
	Connect the COM Ports
	:param uartCom: Uart Port value or folder
	:param dataCom: dataCom value or folder
	:return:
	"""

	# Set the uartCom as a serial object
	# For linux this will end up looking like ... serial.Serial('/dev/ttyS1', 19200, timeout=1)
	connected_uartCom = serial.Serial(uartCom, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.3)
	connected_dataCom = serial.Serial(dataCom, 921600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.025)
	print(connected_uartCom.name + " Connected")
	print(connected_dataCom.name + " Connected")

	return connected_uartCom

def get_cfg(path):
     """
     Get the cfg file
     :param path:
     :return:
     """

     # Set the file pointer to the file indicated by the path and enable it as read
     cfg = open(path, 'r')
     return cfg

def send_cfg(cfg, uartCom):
     """
     Send the chirp configuration file to the antenna
     :param cfg: The file pointer of the chirp congiruation
     :return: None
     """

     print("Sending config file...")

     # For every line in the config file
     for line in cfg:
	print(line)
	time.sleep(.1)
        uartCom.write(line.encode())
        ack = uartCom.readline()
        print(ack)
        #time.sleep(3)
	
     uartCom.reset_input_buffer()
     uartCom.close()


def send_sensor_start(uart_port):
    start = "sensorStart"
    uart_port.write(start.encode(encoding = 'UTF-8'))
    ack = uart_port.readline()
    print(ack)

def send_sensor_stop(uart_port):
    stop = "sensorStop"
    uart_port.write(stop.encode(encoding = 'UTF-8'))
    ack = uart_port.readline()
    print(ack)

# Testing

# Create a uartParserSDK objec


# Create a uartParserSDK object
# new_parser = uartParserSDK()

# Connect its com ports (these are for my pc only)
# new_parser.connect_com_ports("/dev/ttyACM0", "/dev/ttyACM1")

# Get the config file from the path (This path is true on my pc only)
# new_parser.get_cfg("/home/debian/chirp.cfg")

# Send the config file to the board
# new_parser.send_cfg()
