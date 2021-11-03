%{
* extract_features.m
*
* This file is used to extract and return the features from range-doppler heatmap.    
*
* Copyright (C) {2021} Texas Instruments Incorporated - http://www.ti.com/ 
* ALL RIGHTS RESERVED 
*                                                                                                                                                                                                                                                                     
%}

function [dop_ave, num_points, range_ave, dop_ave_pos, dop_ave_neg]=extract_features(radar_data_RDI,min_range_idx1,max_range_idx1,thresh,thresh_numpoints)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to extract features from 2D range-doppler heatmap
% like doppler average, range average etc.
%
% INPUTS:-
% radar_data_RDI : Holds the values of range-Doppler heatmap across the
% 1st antenna.
%
% min_range_idx1 : Holds values of minimum range bin.
%
% max_range_idx1 : Holds values of maximum range bin.
%
% thresh : Holds the threshold value for finding the points which are
% significant above a certain magnitude.
%
% thresh_numpoints : Holds the number of points above a certain threshold
% in range Doppler heatmap.
%
% OUTPUTS:-
% dop_ave : Holds the value of Doppler average to be returned after calculation.  
%
% num_points : Holds the number of threshold points above a cetain threshold   
% to be returned after calculation.
% 
% range_ave : Holds the range average values to be returned after calculation. 
%
% dop_ave_pos : Holds the value of Doppler positive average to be returned after calculation.  
%
% dop_ave_neg : Holds the value of Doppler negative average to be returned after calculation.


RDI_log=(radar_data_RDI);
RDI_log(:,1:2)=0;
RDI_log(:,end-1:end)=0;
RDI_log=fftshift(RDI_log,2);

num_doppler_bins=size(RDI_log,2);
zero_doppler_bin=ceil(num_doppler_bins/2);
dop_ave=0;
dop_ave_pos=0;
dop_ave_neg=0;
range_ave=0;
mag_sum=0;
mag_sum_pos=0;
mag_sum_neg=0;
num_points=0;

for	range_idx = min_range_idx1:max_range_idx1
    x=RDI_log(range_idx,:);
    thresh_idx = find(x>thresh);
    idx_pos_dop = thresh_idx(thresh_idx<zero_doppler_bin);
    idx_neg_dop = thresh_idx(thresh_idx>zero_doppler_bin);
    
    num_points=num_points+length(find(x>thresh_numpoints));
    dop_ave=dop_ave+sum((thresh_idx-zero_doppler_bin).*x(thresh_idx));
    mag_sum=mag_sum+sum(x(thresh_idx));
    mag_sum_pos=mag_sum_pos+sum(x(idx_pos_dop));
    mag_sum_neg=mag_sum_neg+sum(x(idx_neg_dop));
    range_ave=range_ave+sum((range_idx-1)*x(thresh_idx));
        
    dop_ave_pos=dop_ave_pos+sum((idx_pos_dop-zero_doppler_bin).*x(idx_pos_dop));
    dop_ave_neg=dop_ave_neg+sum((idx_neg_dop-zero_doppler_bin).*x(idx_neg_dop));
end

if(mag_sum>0)
    dop_ave=dop_ave/mag_sum;
    range_ave=range_ave/mag_sum;
end
if(mag_sum_pos>0)
    dop_ave_pos=dop_ave_pos/mag_sum_pos;
end
if(mag_sum_neg>0)
    dop_ave_neg=dop_ave_neg/mag_sum_neg;
end

