%% M-ARY FSK
clear
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

gauss = psdGaussian(T(2), fs, 0.25, t)'; 
gauss = 10*log10(gauss/max(gauss));
plot(freq, gauss)


% disp(gmskdB(find(f==12.5e3))); % View difference to approximate T3
% fsk = mfskPow(1/(11700*0.5), 1, 4, freq);
% fsk = fsk / max(fsk);
% fsktes = 10*log10(fsk);
% plot(freq, fsktes)

grid on

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

% GMSK vs MSK
f3 = figure;
hold on
plot(freq, gauss);
plot(freq, mskdB(:, 1));
legend('GMSK (BT=0.25)', 'MSK')
xlabel('Hz1');
ylabel('Power spectral density [dB]');
xlim([0 50e3]);
grid on
fontsize(f3, scale=1.5)  % 120%
% print('mskSpectra.pdf', '-dpdf', '-bestfit'); % Save as PDF 

hold off

% Adjusted GMSK vs MSK
f4 = figure;
hold on
plot(freq, gmskdB(:, 2));
plot(freq, mskdB(:,2))
legend('GMSK (BT=0.25)', 'MSK')
xlabel('Hz');
ylabel('Power spectral density [dB]');
xlim([0 100e3]);
grid on
fontsize(f4, scale=1.5) 
hold off

% f5 = figure;
% BT = [0.1 0.25 0.7, 1];
% t = -5:0.01:5;
% hold on
% for i=1:length(BT)
%     pulse = impulseResponse(t, BT(i), 1);
%     plot(t, pulse);
% end 
% legend('BT = 0.1', 'BT = 0.25', 'BT = 0.7', 'BT = 1');
% xlabel('Time [s]')
% fontsize(f5, scale=1.2)  % 120%
% grid on
% 
% % print('mskPulse.pdf', '-dpdf', '-bestfit'); % Save as PDF 
% hold off



%% Functions

% Periodegram of the Gaussian impulse response to compute power spectral
% density (PSD)
function psdx = psdGaussian(T, fs, BT, t)

B = 1/T * BT; % Half-power bandwidth

% Gaussian impulse response, Proakis - Communication System Engineering
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

% Pulse plot with varying BT
function g = impulseResponse(t, BT, T)
    B = 1/T .* BT; % Half-power bandwidth
    
    % Gaussian impulse response, Proakis - Communication System Engineering
    fac1 = (t - (T/2));
    fac2 = (t + (T/2));
    g = (qfunc(2*pi*B.*(fac1./(log(2)^0.5))) - qfunc(2*pi*B.*(fac2./(log(2)^0.5))));

end

% Expression found in Proakis
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


