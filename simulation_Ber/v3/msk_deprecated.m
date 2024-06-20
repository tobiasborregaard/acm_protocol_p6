clear;
ebnodB = (0:10); % Link SNR interval
ebno = 10.^(ebnodB / 10);
berEst = zeros(size(ebnodB));
frameSize = 100; % Symbols per frame
S = [0 0; 1 0; 0 1; 1 1];


for n = 1:length(ebno)

    numErrs = 0;
    numBits = 0;

    while numErrs < 200 && numBits < 1e8
        rng("default");
        U = randi([0, 1], 5, 1); % Random bit message
        U(1) = 0;
        U(end) = 0;
        
        % Map to symbol constellation
        X = zeros(length(U), 2);
        iter = 1;
        for i = 1:length(U)
            switch U(i)
                case 0
                    X(i, :) = S(iter, :);
                case 1
                    iter = iter + 1;
                    X(i, :) = S(iter, :);
            end
            if iter == 4
                iter = 1;
            end
        end

        % AWGN channel
        N0 = 1 / ebno(n);
        W = (sqrt(N0/2)) * randn(size(X));
        Y = X + W;

        % Maximum likelihood decoding of trellis path
        Vhat = zeros(size(U));
        for i = 1:length(Y) - 1
            Z1 = Y(i, 2) - Y(i+1, 2);
            Z2 = Y(i, 1) + Y(i+1, 1);
            Vhat(i) = Z1 - Z2 < 0;
            
        end
        % Create a vector with indices shifted with +1 to the right
        VhatShift = zeros(size(Vhat));
        VhatShift(1:end-1) = Vhat(2:end);
        
        Uhat = bitxor(Vhat, VhatShift);

        

        nErrors = biterr(U, Uhat);

        numErrs = numErrs + nErrors;
        numBits = numBits + frameSize;
    end
    % Calculate the BER for Eb/N0 index
    berEst(n) = numErrs / numBits;
end
% Theorectical probabibility of error
berMSK = qfunc(sqrt(2.*ebno));
% BER plot
semilogy(ebnodB, berMSK);
hold on
semilogy(ebnodB, berEst, '*');
legend('MSK', 'Estimate')
title('Theoretical Bit Error Rate');
xlabel('Eb/No (dB)');
ylabel('BER');
xlim([0, 11])
ylim([10e-8, 10e-1])
grid on;
