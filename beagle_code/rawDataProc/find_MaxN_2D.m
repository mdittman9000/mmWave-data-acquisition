%{
* find_MaxN_2D.m
*
* This file is used to find the top N magnitude values of the input matrix.    
*
* Copyright (C) {2021} Texas Instruments Incorporated - http://www.ti.com/ 
* ALL RIGHTS RESERVED 
*                                                                                                                                                                                                                                                                     
%}
function [idx]=find_MaxN_2D(y,N)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to find the top N magnitude values of input matrix
%
% INPUTS:-
% y: Range-Doppler heatmap values whose top N magnitude values are to be
% found and arranged in descending order.
%
% N: Holds the value of number of top values to be selected from
% Range-Doppler heatmap.
%
% OUTPUT:-
% idx: Holds the value of the top N magnitude values and their
% corresponding indices.

[a b]=sort(y(:),'descend');
b=b(1:N);

idx=[mod(b,size(y,1)),floor(b/size(y,1))+1];

idx1=find(idx(:,1)==0);

idx(idx1,1)=size(y,1);
idx(idx1,2)=idx(idx1,2)-1;
