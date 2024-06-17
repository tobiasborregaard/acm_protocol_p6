%% M-ARY FSK
clear
close all
clc

% The non-adjusted spectra for modulation schemes are saved
T_old = 1/25e3;
fs = 2^17; % Sample rate
ts = 1/fs; 
t = 0:ts:1-ts; % Time vector
freq = 0:fs/length(t):fs/2;

% 4FSK 
h = 1; % Modulation index (0.5 is MSK)
fsk4dB = zeros(length(freq), 2);


T = [T_old 1/5.855e3]; % Symbol period (NB. 2 bits/symbol for 4FSK)
TG1 = 1/19e3; % Gaussian symbol period 
psdx = psdGaussian(TG1, fs, 0.25, t); % Gaussian filter PSD

for iter = 1:2
    fsk4 = mfskPow(T(iter), h, 4, freq);
    fsk4dB(:,iter) = 10 * log10(fsk4 / max(fsk4));
end 

gfsk4Pow = psdx' .*  mfskPow(TG1, h, 4, freq);
gfsk4PowdB = 10 * log10(gfsk4Pow / max(gfsk4Pow));


% 2FSK
T = [T_old 1/12262];
TG2 = 1/21.13e3;
fsk2dB = zeros(length(freq), 2);

for iter=1:2
    fsk2 = mfskPow(T(iter), h, 2, freq);
    fsk2dB(:,iter) = 10 * log10(fsk2 / max(fsk2));
end

psdx = psdGaussian(TG2, fs, 0.25, t); 
gfsk2 = psdx' .*  mfskPow(TG2, h, 2, freq);
gfsk2dB = 10 * log10(gfsk2 / max(gfsk2));

% MSK 
T = [T_old 1/24525];
TG3 = [T(2) 1/30.42e3]; % To create a comparison for GMSK

mskdB = zeros(length(freq), 2);
gmskdB = zeros(length(freq), 2);

for iter = 1:2
    msk = mfskPow(T(iter), 0.5, 2, freq);
    mskdB(:,iter) = 10 * log10(msk / max(msk));
    psdx = psdGaussian(TG3(iter), fs, 0.25, t); 
    gmsk = psdx' .*  mfskPow(TG3(iter), 0.5, 2, freq);
    gmskdB(:,iter) = 10 * log10(gmsk / max(gmsk));
end 


%% Amateur radio requirements

% GMSK (25 kHz band requirements)
attenuation = [10 58 65]; 
freq = [12.5e3 30e3 56.25e3]; 

% Solves for F(x) - attenuation = 0
base = @(T) 10*log10(mfskPow(T, 0.5, 2, 0));
msk = @(T, f) 10*log10(mfskPow(T, 0.5, 2, f));
psdx_func = @(T, f) 10*log10(psdGaussian(T, fs, 0.25, 1/f));

F = @(T) arrayfun(@(f, a) psdx_func(T, f) * (msk(T, f) - base(T) - a), freq, attenuation);
options = optimoptions('fsolve','Display','iter');
[T_sym, att] = fsolve(F, 1/20e3, options);
bitrate = 1/T_sym;
disp(bitrate) 
disp(bitrate/25e3)  % spectral efficiency


%% Required plots
close all

% % Non adjusted spectra
% f1 = figure;
% hold on
% plot(freq, mskdB(:,1));
% plot(freq, fsk2dB(:,1));
% plot(freq, fsk4dB(:,1));
% legend('MSK', '2FSK', '4FSK')
% xlabel('Hz');
% ylabel('Power spectral density [dB]');
% xlim([0 60e3]);
% grid on
% % fontsize(f1, scale=1.5)  
% % print('nonadjustedSpectra.pdf', '-dpdf', '-bestfit'); % Save as PDF 
% hold off
% 
% % Adjusted spectra
% f2 = figure;
% hold on
% plot(freq, mskdB(:,2));
% plot(freq, fsk2dB(:,2));
% plot(freq, fsk4dB(:,2));
% legend('MSK', '2FSK', '4FSK')
% xlabel('Hz');
% ylabel('Power spectral density [dB]');
% xlim([0 60e3]);
% grid on
% % fontsize(f2, scale=1.5)  
% % print('adjustedSpectra.pdf', '-dpdf', '-bestfit'); % Save as PDF 
% hold off


%% Functions

% Periodogram of Gaussian pulse
function psdx = psdGaussian(T, fs, BT, t)

B = 1/T * BT; % Half-power bandwidth

% Gaussian impulse 
fac1 = (t - (T/2));
fac2 = (t + (T/2));
g = (qfunc(2*pi*B*(fac1./(log(2)^0.5))) - qfunc(2*pi*B*(fac2./(log(2)^0.5))));

% PSD estimation 
N = length(g);
xdft = fft(g);
xdft = xdft(1:N/2+1);
psdx = (1/(fs*N)) * abs(xdft).^2;

psdx(2:end-1) = 2*psdx(2:end-1);
end 

% Gaussian impulse response
function g = impulseResponse(t, BT, T)
    B = 1/T .* BT; % Half-power bandwidth
    fac1 = (t - (T/2));
    fac2 = (t + (T/2));
    g = (qfunc(2*pi*B.*(fac1./(log(2)^0.5))) - qfunc(2*pi*B.*(fac2./(log(2)^0.5))));
end

% M-ary PSD 
function fsk4Pow = mfskPow(T, h, M, f)
m = 1:M;
n = 1:M;
An = sinc(f'*T-h*((2 * n - 1 - M)/2));
Am = sinc(f'*T-h*((2 * m - 1 - M)/2));

beta = (sin(M*pi*h)) / (M * sin(pi*h));
sum1 = sum(An.^2, 2);

sum2 = 0;
for n_idx = 1:M
    for m_idx = 1:M
        alpha = pi * h * (n_idx + m_idx - 1 - M);
        B = (cos(2*pi*f'*T-alpha) - beta * cos(alpha)) ./ (1 + beta^2 - 2 * beta * cos(2*pi*f'*T));
        sum2 = sum2 + B .* An(:,n_idx) .* Am(:, m_idx);
    end
end

fsk4Pow = T * ((1 / M) * sum1 + (2 / M^2) * sum2);
end


