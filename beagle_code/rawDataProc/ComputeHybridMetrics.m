%{
* ComputeHybridMetrics.m 
*
* This file is used to calculate the doppler azimuth correlation by invoking   
* the compute_corr.m function.
*
* Copyright (C) {2021} Texas Instruments Incorporated - http://www.ti.com/ 
* ALL RIGHTS RESERVED 
*                                                                                                                                                                                                                                                                     
%}
function [dop_azim_corr]=ComputeHybridMetrics(dop,azim_angle)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to compute hybrid features across the extracted
% features like correlation between them (eg: doppler-azimuth-correlation,
% doppler-elevation-correlation etc.)
%
% INPUTS:-
% dop: Holds the doppler values of 20-frames under consideration
%
% azim_angle: Holds the azimuth weighted mean vaues of 20-frames under
% consideration.
%
% OUTPUTS:-
% dop_azim_corr: Holds the Doppler Azimuth Correlation value of 20-frames
% taken together.

dop_azim_corr=compute_corr(dop,azim_angle);  
   
   

function [z]= compute_corr(x,y)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to find the correlation between two features.
%
% INPUTS:-
% x: Feature-1 whose correlation is to be calculated
% y: Feature-2 whose correlation is to be calculated
%
% OUTPUT:-
% z: Output correlation of x and y

z=sum((x-mean(x)).*(y-mean(y)))/sqrt(sum(abs(x-mean(x)).^2))/sqrt(sum(abs(y-mean(y)).^2));