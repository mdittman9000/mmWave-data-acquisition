%{
* fss_angle_weighted_average.m
*
* This file is used to calculate angle related features after applying angle-FFT.      
*
* Copyright (C) {2021} Texas Instruments Incorporated - http://www.ti.com/ 
* ALL RIGHTS RESERVED 
*                                                                                                                                                                                                                                                                     
%}

function [azim_wt_mean, elev_wt_mean,azim_wt_disp,elev_wt_disp]=fss_angle_weighted_average(radar_data_2dFFT,radar_data_range_vel_zero,num_samples,antenna_type, calib_params)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to calculate and return the angle related features to
% the gestures like azimuth weighted mean, elevation weighted mean etc.
%
% INPUTS:-
% radar_data_2dFFT : Holds the range-Doppler values after 2D-FFT across all
% the antennas till the maximum range bin.
%
% radar_data_range_vel_zero : Holds the range-Doppler values after 2D-FFT 
% across the 1st antenna alone till the maximum range bin.
% 
% num_samples : Holds value for number of bins while taking angle component
% 
% antenna_type : Holds the type of antenna(eg:63xx, 68xx)
%
% calib_params : Holds the calibration parameters for the antenna.
%
% OUTPUTS:-
% azim_wt_mean : Holds the values to be returned of Azimuth Weigted Mean
% after calculation.
%
% elev_wt_mean : Holds the values to be returned of Elevation Weigted Mean
% after calculation.
%
% azim_wt_disp : Holds the values to be returned of Azimuth Weigted
% Displacement after calculation.
%
% elev_wt_disp : Holds the values to be returned of Elevation Weigted 
% Displacement after calculation.

max_idx=find_MaxN_2D(radar_data_range_vel_zero,num_samples);

azim_idx = zeros(size(max_idx,1),1); 
elev_idx = zeros(size(max_idx,1),1); 
wt = zeros(size(max_idx,1),1);
ang_vec = zeros(size(max_idx,1),12);

for(ik=1:size(max_idx,1))
	xid=max_idx(ik,1);
	yid=max_idx(ik,2);
	
	ang_vec_in = transpose(radar_data_2dFFT(:,xid,yid));
	ang_vec(ik,:) = ang_vec_in;
    if strcmp(antenna_type, 'fss')
        [azim_idx(ik),  elev_idx(ik)] = angle_val_fss(ang_vec_in.*calib_params);
    elseif strcmp(antenna_type, '14xx')
        [azim_idx(ik),  elev_idx(ik)] = angle_val_14xx(ang_vec_in.*calib_params);
    elseif strcmp(antenna_type, '68xx_fss')
        [azim_idx(ik),  elev_idx(ik)] = angle_val_68xx_fss(ang_vec_in.*calib_params);
    elseif strcmp(antenna_type, '63xx_fss')
        [azim_idx(ik),  elev_idx(ik)] = angle_val_63xx_fss(ang_vec_in.*calib_params);
    end
	wt(ik)=radar_data_range_vel_zero(xid,yid);
end

azim_wt_mean=(sum(azim_idx.*wt))/sum(wt);
elev_wt_mean=(sum(elev_idx.*wt))/sum(wt);

azim_wt_disp=  sum(((azim_idx-azim_wt_mean).^2).*wt)/sum(wt);
elev_wt_disp=  sum(((elev_idx-elev_wt_mean).^2).*wt)/sum(wt);