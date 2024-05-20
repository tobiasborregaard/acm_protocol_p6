% Load data
data = readtable('output.csv', 'HeaderLines', 1);
data.Properties.VariableNames = {'SNR', 'Modulation', 'RS', 'CONV', 'BER'};
MODS = {'2FSK','4FSK','MSK'};
RSrate = {[223,255],[239, 255],};
Conrate = {'1/2', '2/3','3/4', '5/6', '7/8'};



BERRatetable = table([], [], [],[],[],[],[], 'VariableNames', {'MODCOD','RS', 'CONV','GP','TP','SPECT','THR'});
data.CONV = strtrim(strrep(data.CONV, '''', ''));
data.RS = strtrim(strrep(data.RS, ' ', ''));
bitrates = [24525 30420; 12262 21130; 11710 38e3];


for a=1:length(MODS)
    modtype = MODS{a};

    for b=1:length(RSrate)
        rateRS = RSrate{b}(1, :);
        RSstring = sprintf('[%d%d]', rateRS(1), rateRS(2));

        for c=1:length(Conrate)
            rateConv = Conrate{c};

            filteredRows = ((matches(data.Modulation,modtype) ) & ...
                (matches(data.RS, RSstring)) & ...
                (matches(data.CONV, rateConv)));


            %Gaussian
            GGP=goodput(codeRate(rateRS,rateConv),bitrates,modtype,1);
            Gmodcod=mod2str(modtype,rateRS,rateConv,1);
            GTHR = findTHR(data,filteredRows,1);
            %noGaussian
            GP=goodput(codeRate(rateRS,rateConv),bitrates,modtype,0);
            modcod=mod2str(modtype,rateRS,rateConv,0);

            switch modtype
                case 'MSK'
                    TP = bitrates(1, 1);
                    GTP= bitrates(1, 2);
                    SPECT=GP/25e3;
                    GSPECT=GGP/25e3;
                case '2FSK'
                    TP = bitrates(2, 1);
                    GTP = bitrates(2, 2);
                    SPECT=GP/25e3;
                    GSPECT=GGP/25e3;
                case '4FSK'
                    TP = bitrates(3, 1);
                    GTP = bitrates(3, 2);
                    SPECT=GP/25e3;
                    GSPECT=GGP/25e3;
            end


            THR =findTHR(data,filteredRows,0);

            disp(modcod);
            ROW = table({modcod}, {RSstring},{rateConv},{GP},{TP},{SPECT},{THR}, ...
                'VariableNames', {'MODCOD','RS', 'CONV','GP','TP','SPECT','THR'});
            GROW = table({Gmodcod},{RSstring},{rateConv}, {GGP},{GTP},{GSPECT},{GTHR}, ...
                'VariableNames', {'MODCOD','RS', 'CONV','GP','TP','SPECT','THR'});

            BERRatetable = [BERRatetable; ROW];
            BERRatetable = [BERRatetable; GROW];


        end
    end
end

%uncoded
for g=1:length(MODS)
    modtype=MODS{g};
    filteredRows=((matches(data.Modulation, modtype)) & (matches(data.RS,'1')) & (matches(data.CONV,'1')));
    THR = findTHRU(data,filteredRows,0);
    GTHR = findTHRU(data,filteredRows,1);
    switch modtype
        case 'MSK'
            GP = bitrates(1, 1);
            GGP= bitrates(1, 2);
            SPECT=GP/25e3;
            GSPECT=GGP/25e3;
        case '2FSK'
            GP = bitrates(2, 1);
            GGP = bitrates(2, 2);
            SPECT=GP/25e3;
            GSPECT=GGP/25e3;
        case '4FSK'
            GP = bitrates(3, 1);
            GGP = bitrates(3, 2);
            SPECT=GP/25e3;
            GSPECT=GGP/25e3;
    end

    modcod = sprintf("%s Uncoded",modtype);
    Gmodcod = sprintf("g%s Uncoded",modtype);

    ROW = table({modcod}, {'1'},{'1'},{GP},{GP},{SPECT},{THR}, ...
        'VariableNames', {'MODCOD','RS', 'CONV','GP','TP','SPECT','THR'});
    GROW = table({Gmodcod},{'1'},{'1'}, {GGP},{GGP},{GSPECT},{GTHR}, ...
        'VariableNames', {'MODCOD','RS', 'CONV','GP','TP','SPECT','THR'});

    BERRatetable = [BERRatetable; ROW];
    BERRatetable = [BERRatetable; GROW];
end
% Assuming BERRatetable is initially populated with data as cells
% Loop through each cell in 'GP' and 'THR' to ensure proper formatting


% Sort and write to CSV
sortedBerTable = sortrows(BERRatetable,'THR');
writetable(sortedBerTable, 'thrTab.csv');



function res = mod2str(MOD,RS,CONV,gauss)
n = RS(2);
k = RS(1);
if gauss == 1
    res = sprintf('g%s [%d,%d] %s', MOD,n,k,CONV);

else
    res = sprintf('%s [%d,%d] %s', MOD,n,k,CONV);
end

end

function res = codeRate(RS,CONV)
convint = eval(CONV);
n = RS(2);
k = RS(1);
res = (k/n)*convint;
end

function Rb = goodput(codeRate,bitrates ,modulation, gauss)
switch modulation
    case 'MSK'
        Rb = codeRate*bitrates(1, gauss+1);
    case '2FSK'
        Rb = codeRate*bitrates(2, gauss+1);
    case '4FSK'
        Rb = codeRate*bitrates(3, gauss+1);
end
end

function res = findTHR(DATA, Rows, gaussian)
% Find the SNR threshold for BER = 10e-6 by interpolating between points where
% BER < 10e-6 and 10e-5 > BER > 10e-6
dat = DATA(Rows, :);
dat = sortrows(dat,'SNR');


if gaussian == 1
    gthr = 0.44; % Gaussian noise figure adjustment
    dat.SNR = dat.SNR + gthr;
end

% Find the point where BER < 10e-6
idx1 = find(dat.BER < 10e-6, 1, 'first'); % Adjust to find the last point below 10e-6 for better interpolation
if isempty(idx1)
    fprintf('No data point with BER < 10e-6 found.\n');
    res = NaN;
    return;
end
y1 = dat(idx1, :);

% Find the point where 10e-5 > BER > 10e-6
idx2 = find(dat.BER < 10e-5 & dat.BER > 10e-6, 1, 'last'); % Adjust to find the first point within the range for better interpolation
if isempty(idx2)
    fprintf('No data point with 10e-5 > BER > 10e-6 found.\n');
    res = NaN;
    return;
end
y2 = dat(idx2, :);

% Linear interpolation/extrapolation between the two points
m = (y2.BER - y1.BER) / (y2.SNR - y1.SNR); % Slope of the line
b = y1.BER - m * y1.SNR;                  % Intercept of the line

% Extrapolate to find SNR at BER = 10e-6
x = (10e-6 - b) / m; % Solve for x (SNR) when y (BER) = 10e-6

fprintf('Threshold for BER = 10e-6 at SNR = %f\n', x);
res = x;
end



function res = findTHRU(DATA, Rows, gaussian)
dat = DATA(Rows, :);
dat = sortrows(dat, 'SNR'); % Sort data by SNR for accurate interpolation

if gaussian == 1
    gthr = 0.44; % Gaussian noise figure adjustment
    dat.SNR = dat.SNR + gthr; % Adjust SNR values for Gaussian noise
end

% Split data into even and odd indexed subsets
evenData = dat(2:2:end, :); % Even-indexed rows
oddData = dat(1:2:end, :);  % Odd-indexed rows

% Interpolate to find SNR thresholds for both subsets
evenSNR = interpolateSNRThreshold(evenData);
oddSNR = interpolateSNRThreshold(oddData);

% Calculate and compare RMS errors for each interpolation to decide the best result
evenRMS = calculateRMS(evenData, evenSNR);
oddRMS = calculateRMS(oddData, oddSNR);

% Select the result with the lower RMS error
if evenRMS < oddRMS
    % fprintf('Using even-indexed data with lower RMS error: %f\n', evenRMS);
    res = evenSNR;
else
    % fprintf('Using odd-indexed data with lower RMS error: %f\n', oddRMS);
    res = oddSNR;
end
end

function snrThreshold = interpolateSNRThreshold(data)
% Linear interpolation to find SNR at BER = 10e-6
idx1 = find(data.BER < 10e-6, 1, 'last');
idx2 = find(data.BER < 10e-5 & data.BER > 10e-6, 1, 'first');

if isempty(idx1) || isempty(idx2)
    snrThreshold = NaN; % No suitable points found for interpolation
    return;
end

y1 = data(idx1, :);
y2 = data(idx2, :);
m = (y2.BER - y1.BER) / (y2.SNR - y1.SNR); % Slope of the line
b = y1.BER - m * y1.SNR;                  % Intercept of the line
snrThreshold = (10e-6 - b) / m;           % Solve for SNR when BER = 10e-6
end

function rms = calculateRMS(data, estimatedSNR)
% Calculate RMS error for the interpolation
estimatedBER = data.BER - 10e-6; % Calculate residuals for each point
rms = sqrt(mean((estimatedBER).^2)); % RMS of residuals
end



