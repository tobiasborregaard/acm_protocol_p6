clear;
close all
ebnodB = (0:20);
ebno = 10.^(ebnodB/10);

% 2FSK (p. 416 Haykin)
berFSK2 = qfunc(sqrt(ebno)); 

%MSK
berMSK = qfunc(sqrt(2.*ebno));

% GMSK
alpha = 1.8; %
berGMSK = qfunc(sqrt(alpha*ebno)); % BT = 0.3

% 4FSK
M = 4;
berFSK4 = (M-1)*qfunc(sqrt(ebno));
berFSK4 = 0.5*berFSK4; % Es to Eb conversion (2 bits per symbol)

% 8FSK
berFSK8 = 7*qfunc(sqrt(ebno));
berFSK8 = 1/3*berFSK8;

%8PSK
ber8PSK = 2*qfunc(sqrt(2*ebno)*sin(pi/8));
ber8PSK = 1/3*ber8PSK;

% BER plots
f2 = figure;
semilogy(ebnodB, berMSK, ebnodB, ber8PSK, ebnodB, berFSK2, ebnodB, berGMSK, ebnodB, berFSK4, ebnodB, berFSK8);
legend('MSK/BPSK/QPSK', '8PSK', '2FSK', 'GMSK', '4FSK', '8FSK')
xlabel('Eb/N0 [dB]');
ylabel('BER');
xlim([0 20])
ylim([10e-8 10e-1])
grid on;


