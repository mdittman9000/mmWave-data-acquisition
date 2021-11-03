# import struct
# import numpy as np
# import time
# import numpy.matlib
# import matplotlib.pyplot as plt

# fin = open("C:\\Users\\a0491594\\Desktop\\Data_Capture_Source\\data\\Top-to-bottom_swipe\\Top-to-bottom_swipe_07_07_2021_10_14_00\\adcRawData.bin",'rb')
# #fin = open("C:\\ti\\mmw_industrial_classification\\TI_Classification\\Gesture_Detection\\TrainingCollateral\\Hand_Gesture_Recognition\\Train\\rawData\\dd_gesture1_l2r_trail1.bin",'rb')

# #Unpack one frames worth of samples
# num_chirps = 128 #32
# num_samples = 64 #256
# num_antennas = 12 #12
# samples_per_frame = num_chirps * num_samples * num_antennas * 2
# frame = 0
# time = 0

# stillData = True

# fig, ax = plt.subplots(nrows=1)

# while True:
#     if stillData:
#         data = np.zeros(samples_per_frame)
#         for i in range(samples_per_frame):
#             try:
#                 data[i] = struct.unpack('h',fin.read(2))[0]
#             except:
#                 stillData = False
#                 break
        
#         frame = frame + 1
#         time = time + .035

#         data = data  - (data >=  2**15) * 2**16

#         data_real = data[1::2]
#         data_imag = np.multiply(data[::2], 1.0j)
#         data = data_real + data_imag

#         data = np.reshape(data,(num_samples, num_antennas, num_chirps), order="F")
#         data = np.moveaxis(data,0,1)

#         radar_data_1dfft = np.rint(np.fft.fft(data,axis=1))

#         hann_window = np.reshape(np.matlib.repmat(np.hanning(num_chirps),num_samples,num_antennas),(num_antennas,num_samples,num_chirps))
#         window_velocity = np.multiply(radar_data_1dfft,hann_window)

#         radar_data_2dfft = np.rint(np.fft.fft(window_velocity,axis=2))

#         radar_data_range_velo = np.rint(np.sum(abs(radar_data_2dfft)**2,axis=0)) #np.rint(abs(radar_data_2dfft[:,0]))
#         radar_data_range_velo = np.roll(radar_data_range_velo, int(num_chirps / 2))
        


        
#         #The following line converts the data to  Rx0I0, Rx0Q0, Rx0I1, Rx0Q1, ... 

#         # data = np.reshape(data,(samples_per_frame // 4, 4))
#         # data[:,[1,2]] = data[:,[2,1]]
#         # data = np.transpose(data)

#         # #Shape into radar cube
#         # data = np.reshape(data,(num_samples * 2 ,num_antennas, num_chirps), order="F")

#         # #Convert into complex number
#         # data_real = data[::2,:,:]
#         # data_imag = np.multiply(data[1::2,:,:], 1.0j)
#         # data = data_real + data_imag

#         # #permute dimensions
#         # data = np.moveaxis(data,0,1)

#         # #Compute Range FFT
#         # radar_data_1dfft = np.rint(np.fft.fft(data,axis=1))

#         # #Window velocity data
#         # hann_window = np.reshape(np.matlib.repmat(np.hanning(num_chirps),num_samples,num_antennas),(num_antennas,num_samples,num_chirps))
#         # window_velocity = np.multiply(radar_data_1dfft,hann_window)

#         # #Compute Velocity FFT
#         # radar_data_2dfft = np.rint(np.fft.fft(window_velocity,axis=2))

#         # #Computer Range Velocity Matrix
#         # #To Do: This might be wrong
#         # radar_data_range_velo = np.rint(abs(radar_data_2dfft[0])) #np.rint(np.sum(radar_data_2dfft,axis=0))

#         # #Zero out lower velocity bins 
#         # radar_data_range_velo[:,0:5] = 0
#         # radar_data_range_velo[:,-5:] = 0

        
#         ax.pcolormesh(radar_data_range_velo)
#         plt.title(str(time))
#         plt.draw()
#         plt.pause(0.01)
#     else:
#         break


# # data = np.zeros(samples_per_frame)
# # for i in range(samples_per_frame):
# #     data[i] = struct.unpack('h',fin.read(2))[0]

# # #The following line converts the data to  Rx0I0, Rx0Q0, Rx0I1, Rx0Q1, ... 
# # data = np.reshape(data,(samples_per_frame // 4, 4))
# # data[:,[1,2]] = data[:,[2,1]]
# # data = np.transpose(data)

# # #Shape into radar cube
# # data = np.reshape(data,(128,12,128), order="F")

# # #Convert into complex number
# # data_real = data[::2,:,:]
# # data_imag = np.multiply(data[1::2,:,:], 1.0j)
# # data = data_real + data_imag

# # #permute dimensions
# # data = np.moveaxis(data,0,1)

# # #Compute Range FFT
# # radar_data_1dfft = np.rint(np.fft.fft(data,axis=1))

# # #Window velocity data
# # hann_window = np.reshape(np.matlib.repmat(np.hanning(128),64,12),(12,64,128))
# # window_velocity = np.multiply(radar_data_1dfft,hann_window)

# # #Compute Velocity FFT
# # radar_data_2dfft = np.rint(np.fft.fft(window_velocity,axis=2))

# # #Computer Range Velocity Matrix
# # #To Do: This might be wrong
# # radar_data_range_velo = np.rint(abs(radar_data_2dfft[0])) #np.rint(np.sum(radar_data_2dfft,axis=0))

# # #Zero out lower velocity bins 
# # radar_data_range_velo[:,0:5] = 0
# # radar_data_range_velo[:,-5:] = 0

# # RDIlog = np.fft.fftshift(radar_data_range_velo, axes=1)

# # num_doppler_bins = RDIlog.shape[1]
# # zero_doppler_bin = num_doppler_bins // 2

# # x = RDIlog[1]


# # num_points = (RDIlog > 2000).sum()
# # dop_ave = np.multiply((np.arange(-63,65)),x).sum()
# # dop_neg = np.multiply((np.arange(-63,1)),x[0:zero_doppler_bin]).sum()
# # dop_pos = np.multiply((np.arange(0,64)),x[zero_doppler_bin:num_doppler_bins]).sum()
# # rang_avg = np.multiply(1,x).sum()

# # print(num_points,dop_ave,dop_neg,dop_pos,rang_avg)