%{
* max2d.m
*
* This file is used to find the maximum value of 2D-matrix.    
* 
*
* Copyright (C) {2021} Texas Instruments Incorporated - http://www.ti.com/ 
* ALL RIGHTS RESERVED 
*                                                                                                                                                                                                                                                                     
%}

function [value,row,colomn]=max2d(x)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function reutrns the maximum element in a 2-D matrix 'x' and 
% its position (row & colomn)
%
%
% INPUT:-
% x: Holds the vector whose maximum value is to be found out
%
% OUTPUTS:-
% value: Hold the highest value element of x
%
% row: Holds the row corresponding to the value
%
% colomn: Holds the column corresponding to the value
%
% By: Abdulrahman Ikram Siddiq
% Kirkuk - IRAQ
% Wednsday Nov.9th 2011 10:23 PM

[w,j]=max(x);
[value,i]=max(w);
colomn=i;
row=j(i);