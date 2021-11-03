function procData = ExtractFeatureVectors(antenna_type, numChirpsPerFrame, numADCSamplesPerChirp, frame_duration, adc_file_name, output_file)
    % In general we use one tx per chirp config.
    procData = 1;
    
    numChirpsPerFrame = str2double(numChirpsPerFrame);
    numADCSamplesPerChirp = str2double(numADCSamplesPerChirp);
    frame_duration = str2double(frame_duration);
    
    if strcmp(antenna_type, 'fss')
        chirpConfigsPerChirp = 2;
    elseif strcmp(antenna_type, '14xx')
        chirpConfigsPerChirp = 3;
    elseif strcmp(antenna_type, '68xx_fss')
        chirpConfigsPerChirp = 3;
    elseif strcmp(antenna_type, '63xx_fss')
        chirpConfigsPerChirp = 3;	
    end

    chirp_design = populate_chirp_design(numADCSamplesPerChirp,chirpConfigsPerChirp,numChirpsPerFrame, antenna_type);
    chirp_design.MIN_RANGE_BIN = 2;
    chirp_design.MAX_RANGE_BIN = 8;
    frameSizeBytes = numChirpsPerFrame*numADCSamplesPerChirp * 12 * 4;
    

    size = dir(adc_file_name);
    size = size.bytes;
    Number_of_Frames = floor(size / frameSizeBytes);

    GestureRecog_Extract(adc_file_name, Number_of_Frames,chirp_design, frame_duration,output_file);
end 

function [radar_datax]=GestureRecog_Extract(adc_file_name, Number_of_Frames, cD, frame_duration,output_file)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is the main function from which gesture feature extraction
% starts after data from .bin files is arranged properly. Here, some complex 
% or hybrid features for calculation is also taken into account.
% 
% INPUTS:-
% adc_file_name : Holds the adc_file_name under processing.
% 
% feature_file_name : Holds the feature file name of .bin file name under
% process.
%
% Number_of_Frames : Holds the total number frames from a .bin file.
%
% cD : This struct holds all the fields related to chirp Design.
%
% OUTPUT:-
% Finally fetaure-vector data under the fvData for all the bin files in the
% form of mat files is stored.

% Open the file and read the data.
fileID = fopen(adc_file_name,'r');
LEN_CORR = 20;

%% memory allocation; 
dop_ave = zeros(Number_of_Frames,1,'single'); dop_ave_pos = zeros(Number_of_Frames,1,'single'); 
dop_ave_neg = zeros(Number_of_Frames,1,'single'); range_ave = zeros(Number_of_Frames,1,'single'); 
num_points = zeros(Number_of_Frames,1,'single'); azim_wt_mean = zeros(Number_of_Frames,1,'single'); 
elev_wt_mean = zeros(Number_of_Frames,1,'single'); azim_wt_disp = zeros(Number_of_Frames,1,'single'); 
elev_wt_disp = zeros(Number_of_Frames,1,'single'); dop_azim_corr = zeros(Number_of_Frames,1,'single'); 

%% Main loop

for frameIdx = 1:Number_of_Frames
    radar_data = readframeData(fileID, cD,'DCA1000');
    [dop_ave(frameIdx),  dop_ave_pos(frameIdx), dop_ave_neg(frameIdx), ...
        range_ave(frameIdx), num_points(frameIdx),azim_wt_mean(frameIdx), ...
        elev_wt_mean(frameIdx), azim_wt_disp(frameIdx), ...
        elev_wt_disp(frameIdx)]= gesture_processing(radar_data,cD);
    
    if mod(frameIdx, 100) == 0
        disp(['Processsed ' num2str(frameIdx) ' frames.']);
    end

    if frameIdx >= LEN_CORR
        frameIdxTmp=(frameIdx-LEN_CORR+1):frameIdx;
        dop_azim_corr(frameIdx)= ComputeHybridMetrics(dop_ave(frameIdxTmp), azim_wt_mean(frameIdxTmp));
    end
    
end

fclose(fileID);

close all;

time_stamps = 0:frame_duration / (Number_of_Frames - 1) :frame_duration;

vector_data = [time_stamps(:),dop_ave(:),dop_ave_pos(:),dop_ave_neg(:),range_ave(:),num_points(:),azim_wt_mean(:),...
                elev_wt_mean(:),dop_azim_corr(:),azim_wt_disp(:),elev_wt_disp(:)];
            
%vector_data = normalize(vector_data, 1);

%vector_data = [time_stamps(:), vector_data];

            
cHeader = {'Time (Sec)' 'dop_avg' 'dop_ave_pos' 'dop_ave_neg' 'range_ave' 'num_points' 'azim_wt_mean',...
                'elev_wt_mean' 'dop_azim_corr' 'azim_wt_disp' 'elev_wt_disp'};
commaHeader = [cHeader;repmat({','},1,numel(cHeader))]; %insert commaas
commaHeader = commaHeader(:)';
textHeader = cell2mat(commaHeader);
textHeader = textHeader(1:end-1);

fid = fopen(output_file,'w');
fprintf(fid,'%s\n',textHeader);
fclose(fid);
            
dlmwrite(output_file, vector_data,'-append');
end

function  radar_data = readframeData(fileID, cD, capturecard)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to extract radar data from .bin files and use it
% for further processing.
%
% INPUTS:-
% fileID : Holds the file ID number.
%
% cD : This struct holds fields related to Chirp Design.
%
% capturecard : Holds the capture card type used.
%
% OUTPUT:-
% radar_data : Holds the data arranged in form of no. of antennas x no. of
% ADC samples x no. of chirps

radar_data = fread(fileID,cD.total_samples_per_frame,'int16=>single');
adcOut = radar_data(2:2:end) + 1j*radar_data(1:2:end);
out = reshape(adcOut,  cD.Samples_Per_ChirpConfig, cD.Number_of_real_channels/2 * cD.ChirpConfigs_Per_Chirp, cD.Chirps_Per_Frame);

% adcOut data is in the dimension of (numADCSamples, numChirps,
% numRXChannel* numTXChannel)
radar_data = permute(out, [2, 1, 3]);

% if strcmp(capturecard,'TSW1400')
%     % TSW1400 converts ADC data to offset binary. Convert it back to 2's
%     % complement.
%     radar_data = fread(fileID,cD.total_samples_per_frame,'uint16=>single')-single(2^15);
% 
% elseif strcmp(capturecard,'DCA1000')
%     radar_data = fread(fileID,cD.total_samples_per_frame,'int16=>single');
%     radar_data = reshape(radar_data, 4, []);
%     %The following line converts the data to  Rx0I0, Rx0Q0, Rx0I1, Rx0Q1, ... 
%     radar_data = radar_data([1 3 2 4],:); 
% end
% 
% radar_data = reshape(radar_data, 2*(cD.Samples_Per_ChirpConfig+cD.num_prefix_samples+cD.num_suffix_samples), cD.Number_of_real_channels/2 * cD.ChirpConfigs_Per_Chirp, cD.Chirps_Per_Frame);
% 
% % Convert the data to complex
% radar_data_real = radar_data(1:2:end, :, :);    radar_data_imag = radar_data(2:2:end, :, :);
% radar_data = radar_data_real + 1i*radar_data_imag;
% 
% % convert the dimensions to virtual antennas, adc samples, chirps per
% % frame.
% radar_data = permute(radar_data, [2,1,3]);
% radar_data = radar_data(:,cD.num_prefix_samples+[1:cD.Samples_Per_ChirpConfig],:,:);
% 
% radar_data = squeeze(radar_data);
    

end

function chirpDesign = populate_chirp_design(Samples_Per_ChirpConfig,ChirpConfigs_Per_Chirp,Chirps_Per_Frame, antenna_type)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function is used to populate the chirp design and calculate
% parameters related to the chirp design.
%
% INPUTS:-
% Samples_Per_ChirpConfig: Holds the number of ADC samples as per chirp
% configuration.
%
% ChirpConfigs_Per_Chirp: Holds the number of chirps per chirp before a
% slight delay.
%
% Chirps_Per_Frame: Holds the number of chirps per frame.
%
% antenna_type: Holds the type of antenna used based on which some
% parameters might slightly vary.
%
% OUTPUT:-
% chirpDesign: Holds the struct with variables related to chirp design
% which will be calculated and returned.

lightSpeed = 3e8; %m/s

% We conly use complex data.
is_real = 0;
% Basic Chirp parameters.
cD.Samples_Per_ChirpConfig = Samples_Per_ChirpConfig;
cD.ChirpConfigs_Per_Chirp = ChirpConfigs_Per_Chirp;
cD.Chirps_Per_Frame = Chirps_Per_Frame;

cD.num_prefix_samples=0;
cD.num_suffix_samples=0;

if is_real == 1
    cD.Number_of_real_channels = 4; % 8 real channels, 4 complex channels.
else
    cD.Number_of_real_channels = 8; % 8 real channels, 4 complex channels.
end
cD.Number_of_cmplx_channels = 4;
cD.frame_periodicity_sec = 8e-3;

if strcmp(antenna_type, 'fss')
    
    cD.Sample_Rate_Hz = 2.0e6;
    cD.Slope_Hz = 100e12;
    cD.Chirp_repetition_period_sec = 400e-6;
    cD.Start_Frequency_Hz = 77e9;
    
elseif strcmp(antenna_type, '14xx')
    cD.Sample_Rate_Hz = 2.350e6;
    cD.Slope_Hz = 99.987e12;
    cD.Chirp_repetition_period_sec = (84 + 34 + (2*(7 + 34)))*1e-6;
    cD.Start_Frequency_Hz = 60.6e9;

elseif strcmp(antenna_type, '68xx_fss') || strcmp(antenna_type, '63xx_fss')
    cD.Sample_Rate_Hz = 2.350e6;
    cD.Slope_Hz = 99.987e12;
    cD.Chirp_repetition_period_sec = (84 + 34 + (2*(7 + 34)))*1e-6;
    cD.Start_Frequency_Hz = 60.6e9;    
end

cD.lambda = lightSpeed/(cD.Start_Frequency_Hz);


% Some derived parameters.
cD.range_resolution = ((cD.Sample_Rate_Hz/cD.Samples_Per_ChirpConfig)/cD.Slope_Hz)*(lightSpeed/2);
cD.vel_resolution = ((1/cD.Chirp_repetition_period_sec)/cD.Chirps_Per_Frame)*(cD.lambda/2);
cD.range_axis = (0:cD.Samples_Per_ChirpConfig-1)*cD.range_resolution;
cD.vel_axis = (-Chirps_Per_Frame/2:cD.Chirps_Per_Frame/2-1)*cD.vel_resolution;

% no windowing in range
cD.window_1D = ones(cD.Number_of_cmplx_channels*cD.ChirpConfigs_Per_Chirp,cD.Samples_Per_ChirpConfig,cD.Chirps_Per_Frame);
cD.window_2D = permute(repmat(hann(cD.Chirps_Per_Frame),1,cD.Samples_Per_ChirpConfig,cD.Number_of_cmplx_channels*cD.ChirpConfigs_Per_Chirp),[3,2,1]);

% Compute the total number of samples per frame.
cD.total_samples_per_frame = cD.Number_of_real_channels*(cD.Samples_Per_ChirpConfig+cD.num_prefix_samples+cD.num_suffix_samples)*cD.ChirpConfigs_Per_Chirp*cD.Chirps_Per_Frame;

% Set parameters for chirp design.
cD.RANGE_FFT_SCALING = 1; 
cD.DOPPLER_FFT_SCALING = 1;
cD.NUM_CHIRP_SCALING= 256/cD.Chirps_Per_Frame;
cD.numVirtualChanels =(cD.Number_of_cmplx_channels*cD.ChirpConfigs_Per_Chirp); 
cD.angleFFTScaleFac = (cD.RANGE_FFT_SCALING * cD.DOPPLER_FFT_SCALING)/(cD.numVirtualChanels*cD.Samples_Per_ChirpConfig*cD.Chirps_Per_Frame);

cD.MIN_RANGE_BIN = 2;
cD.MAX_RANGE_BIN = 8;

cD.antenna_type = antenna_type;
cD.BINS_TO_SUPPRESS = 5;
cD.NUM_BINS_FOR_WT_ANGLE = 50;

cD.calibParams = single(ones(12,1));

cD.calibParams = transpose(cD.calibParams);

chirpDesign = cD;
end