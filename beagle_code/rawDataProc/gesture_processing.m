%{
* gesture_processing.m
*
* This file is used to invoke functions for getting features from range-doppler      
* heatmap and also angle related features.
*
* Copyright (C) {2021} Texas Instruments Incorporated - http://www.ti.com/ 
* ALL RIGHTS RESERVED 
*                                                                                                                                                                                                                                                                     
%}

function [dop_ave,dop_ave_pos, dop_ave_neg, range_ave, num_points, ...
      azim_wt_mean, elev_wt_mean, azim_wt_disp, elev_wt_disp] = gesture_processing(radar_data, chirpDesign)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function does the FFT operations on arranged radar data by applying
% FFT's across no. of antennas, chirps and ADC samples based on the need to
% extract features.
%
% INPUTS:-
% radar_data : Holds the radar data values arranged in the form of no. of
% antennas x no. of ADC samples x no. of Chirps.
%
% chirpDesign : This struct has fields with respect to chirp design
% parameters.
%
% OUTPUTS:-
% dop_ave : Holds the Doppler Average values to be calculated and returned.
% 
% dop_ave_pos : Holds the Doppler Positive Average values to be calculated and returned.
%
% dop_ave_neg : Holds the Doppler Negative values to be calculated and returned.
%
% range_ave : Holds the Range Average values to be calculated and returned.
%
% num_points : Holds the calculated number of points above a certain
% threshold value.
%
% azim_wt_mean : Holds the azimuth weighted mean to be calculated and returned.
%
% elev_wt_mean : Holds the elevation weighted mean to be calculated and returned.
%
% azim_wt_disp : Holds azimuth weighted displacement value to be calculated
% and returned. 
%
% elev_wt_disp : Holds elevation weighted displacement value to be calculated
% and returned. 

% If there are multiple TX's being sequenced per chirp config, then rearrange the
% multiple TX's as virtual antennas
% radar_data dimensions : NUM_VIRTUAL_ANT x SAMPLES_PER_CHIRP x  NUM_CHIRPS x NUM_FRAMES

% 1D range-FFT across the 2nd dimensions (samples)
radar_data_1dFFT = round(fft(radar_data.*chirpDesign.window_1D,[], 2)/chirpDesign.RANGE_FFT_SCALING);

% 2D vel-FFT across the 3rd dimensions (chirps)
radar_data_2dFFT = round(fft(radar_data_1dFFT.*chirpDesign.window_2D,[], 3)/chirpDesign.DOPPLER_FFT_SCALING);


% Non-coherent integration across antennas (1st dimension)
% radar_data_range_vel has the dimensions (range x vel x frames)
radar_data_range_vel = round(squeeze(sum(abs(radar_data_2dFFT))));

% Zero out the lowest five velocity bins (both +ve and -ve). This is to
% avoid leakage from stationary objects affecting feature vectors. 
radar_data_range_vel_high_dopp = radar_data_range_vel;
radar_data_range_vel_high_dopp(:,1:chirpDesign.BINS_TO_SUPPRESS)=0;
radar_data_range_vel_high_dopp(:,end-chirpDesign.BINS_TO_SUPPRESS:end)=0;



% Setup the (fft magnitude) threshold for extracting the number of
% (significant) points in the 2D FFT output
thresh_num_points = 16000; %4000/chirpDesign.RANGE_FFT_SCALING/chirpDesign.NUM_CHIRP_SCALING

[dop_ave, num_points, range_ave, dop_ave_pos, dop_ave_neg] = extract_features(radar_data_range_vel_high_dopp,chirpDesign.MIN_RANGE_BIN,chirpDesign.MAX_RANGE_BIN,0,thresh_num_points);

%%%%%%%%%%%%%%%%start-angle-est-fss%%%%%%%%%%%%%%%%%%%%%%%%%
radar_data_2dFFT_scaled=floor(radar_data_2dFFT/2^6);

[azim_wt_mean, elev_wt_mean, azim_wt_disp, elev_wt_disp]= ...
    fss_angle_weighted_average(radar_data_2dFFT_scaled(:,1:chirpDesign.MAX_RANGE_BIN,:), ...
                                radar_data_range_vel_high_dopp(1:chirpDesign.MAX_RANGE_BIN,:), ...
                                chirpDesign.NUM_BINS_FOR_WT_ANGLE,chirpDesign.antenna_type, ... 
                                chirpDesign.calibParams);       
end

