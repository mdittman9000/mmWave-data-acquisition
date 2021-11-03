%{
* angle_val_68xx.m 
*
* This file is used to calculate the elevation and azimuth index for 68xx   
* TI family of devices.
*
* Copyright (C) {2021} Texas Instruments Incorporated - http://www.ti.com/ 
* ALL RIGHTS RESERVED 
*                                                                                                                                                                                                                                                                     
%}

function [azim_idx, elev_idx]=angle_val_68xx_fss(x_ang)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to find azimuth index and elevation index based
% x_ang input for 68xx antenna. 
%
% INPUT:-
% x_ang : Holds indices for whic azimuth, elevation is to be estimated
%
% OUTPUTS:-
% azim_idx : Holds the azimuth index for input x_ang.
%
% elev_idx : Holds the elevation index for input x_ang.

    NUM_ANGLE_BINS=32;
	x_ang_2d=[ -x_ang([1 4 5 8]);
		   x_ang([2 3 6 7]);
		   0 0 -x_ang([9 12]);
		   0 0 x_ang([10 11]);];

	a=(fft2(x_ang_2d,NUM_ANGLE_BINS,NUM_ANGLE_BINS));
	
    [~, r, c]=max2d(abs(a));
	r=r-1;
	c=c-1;
	if(c>NUM_ANGLE_BINS/2-1)
        c=c-NUM_ANGLE_BINS;
	end
	if(r>NUM_ANGLE_BINS/2-1)
        r=r-NUM_ANGLE_BINS;
	end
	
	elev_idx=r;
	azim_idx=c;



