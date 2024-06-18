ebnodB = -10:0.02:20;
ebno = 10.^(ebnodB / 10);
RSrate = {[223,255],[239, 255]};
Conrate = {'1/2', '2/3','3/4', '5/6', '7/8'};
berEstTable = table([], {}, {}, {}, [], 'VariableNames', {'EBNO', 'Mod', 'RateRS', 'RateConv', 'BerEst'});
MODS = {'2FSK','4FSK','MSK'};


for iter=2:2
    for lne=1:length(RSrate)
        rateRS = RSrate{lne}(1, :);
        frameSize = rateRS(1)*8; % Symbols per frame

        for lncot = 1:length(Conrate)
            rateConv = Conrate{lncot};
            tempResults = cell(length(ebno), 5);  % Temporary storage for results

            berEst = zeros(length(ebno));
            tic;

            for n = 1:length(ebno)
                if mod(n,2)==0
                
                    fprintf('Step: %1.0f, type: %1.0f, rateRS: %s, rateConv: %s ', ebnodB(n), iter, mat2str(rateRS), mat2str(rateConv));

                    numErrs = 0;
                    numBits = 0;
                    while numErrs < 200 && numBits < 1e7
                        U = 0;
                        Uhat = 0;
                        k = 0 ;
                        switch iter
                            case 1
                                [U, Uhat, k] = fsk2(ebno(n), frameSize, rateConv, rateRS);
                            case 2
                                [U, Uhat, k] = fsk4(ebno(n), frameSize, rateConv, rateRS);
                            case 3
                                [U, Uhat, k] = msk(ebno(n), frameSize, rateConv, rateRS, 2);
                        end

                        nErrors = biterr(U, Uhat);

                        numErrs = numErrs + nErrors;
                        numBits = numBits + frameSize;


                    end
                    berEst(n) = numErrs / numBits;
                    fprintf('Ber %6.2e, Lapsed Time %6.2f\n', berEst(n),toc);
                    if berEst(n) < 1e-5 && berEst(n) ~= 0
                            break;
                    end
                    if berEst(n) == 0
                        break;
                    end
                end

            end
            % Create a table row and add it to the berEstTable
            for idx = 1:length(ebno)
                newRow = table(ebnodB(idx), {MODS{iter}}, {mat2str(rateRS)}, {mat2str(rateConv)}, berEst(idx), ...
                    'VariableNames', {'EBNO', 'Mod', 'RateRS', 'RateConv', 'BerEst'});
                berEstTable = [berEstTable; newRow];

            end
        end
    end

end


for iter= 2:2
    frameSize = rateRS(1)*500;
    for n=1:length(ebno)

        numErrs = 0;
        numBits = 0;
        estBeR = 1;
        fprintf('Step: %d, type: %d \n', ebnodB(n), iter);


        while (numErrs < 200) & (numBits < 1e7)
            U = 0;
            Uhat = 0;
            k=0;
            switch iter
                case 1
                    U = randi([0 1], frameSize, 1);
                    Uhat = BFSKMOD(ebno(n),U);
                    k = 1;
                case 2
                    U = randi([0, 1], frameSize, 1);


                    Uhat = MFSKMOD(ebno(n), U);
                    k = 2;
                case 3
                    U = randi([0 1], frameSize, 1)';

                    Uhat = MSKMOD(ebno(n), U, 2);
                    k = 1;
            end
            nErrors = biterr(U, Uhat,'overall');
            numErrs = numErrs + nErrors;
            numBits = numBits + frameSize;

            estBeR = numErrs / numBits;
        end


        newRow = table(ebnodB(n), {MODS{iter}}, {"1"}, {"1"}, estBeR, ...
            'VariableNames', {'EBNO', 'Mod', 'RateRS', 'RateConv', 'BerEst'});
        try
            berEstTable = [berEstTable; newRow];

        catch exception
            disp('Error appending to table:');
            disp(exception.message);
            disp('Inspect newRow:');
            disp(newRow);
            disp('Inspect berEstTable:');
            disp(berEstTable.Properties.VariableTypes);
        end
        if estBeR < 1e-5 && estBeR ~= 0
            break;
        end


    end
end




timestamp = datetime('now', 'Format', 'yyyy_MM_dd-HH_mm');
filename = sprintf('4FSK2%s.csv', char(timestamp));
writetable(berEstTable, filename);
%
% % Theorectical BER expressions
% berfsk2 = qfunc(sqrt(ebno));
% bermsk = qfunc(sqrt(2.*ebno));
% berfsk4Bit = 0.5 * (3 * qfunc(sqrt(ebno)));
%
% % BER plot
% % semilogy( ...
% %     ebnodB, berfsk4Bit, ...
% %     ebnodB, berEstTable.fsk4,'*', ...
% %     ebnodB, berfsk2, ...
% %     ebnodB, berEstTable.fsk2, '*');
% % grid on
%
% semilogy( ...
%     ebnodB, bermsk, ...
%     ebnodB, berEstTable.msk,'*');
% grid on


% Gaussian filtered ebn0 degradation of 0.4 dB



function [U, Uhat, k] = fsk2(ebno, frameSize, conv,rscod)
k = 1; % Bits per symbol
U = randi([0, 1], frameSize, 1); % Random bit message
RconX = concatCoder(rscod,conv,U);


demodud = BFSKMOD(ebno,RconX);


Uhat = concatDecoder(rscod,conv,demodud);
end

function [U, Uhat, k] = fsk4(ebno, frameSize, conv, rscod)
k = 2; % Bits per symbol
% Generate random bits and encode them
U = randi([0, 1], frameSize, 1);
RconX = concatCoder(rscod,conv,U); % Convolutional encoding


demodBits = MFSKMOD(ebno,RconX);
% Viterbi decoding of the received bits
decodedBits = concatDecoder(rscod,conv,demodBits);

Uhat = decodedBits;
end


function [U, Uhat, k] = msk(ebno, frameSize, conCod, rscod, T)
k=1;
U = randi([0 1], frameSize, 1)'; % Random bit message

RconX = concatCoder(rscod, conCod, U)';
Vhat = MSKMOD(ebno,RconX,T);

% Decoding using concatenated decoder
Uhat = concatDecoder(rscod, conCod, Vhat)';
end

%
%
% function berTable = berToFile(berTable, berEst, iter)
% % Add new data to columns
% colName = {'fsk2', 'fsk4', 'msk'};
% berTable.(colName{iter}) = berEst';
% % Save as a .csv file at last iteration with a timestamp
% if iter == 4
%     timestamp = datetime('now', 'Format', 'yyyy_MM_dd-HH_mm');
%     filename = sprintf('berEstimationTable_%s.csv', char(timestamp));
%     writetable(berEstTable, filename);
% end
%
% end


function CONCATenc = concatCoder(RSC,CONVC,MSG)
RS_msg = RSCoder(RSC,MSG,8);

CONCATenc = ConvCoder(CONVC,RS_msg);

end


function CONCATdec = concatDecoder(RSC,CONVC,MSG)

binmsg=ConvDecoder(CONVC,MSG);

CONCATdec = RSdecoder(RSC,binmsg,8);

end


function RScodedx = RSCoder(RSC, MSG, m)
n = RSC(2);
k = RSC(1);
% Calculate the total number of bits needed to form k symbols, each m bits long
totalBitsNeeded = k * m;

% Initial padding to ensure MSG length is a multiple of m for symbol formation
if length(MSG) < totalBitsNeeded
    padSize = totalBitsNeeded - length(MSG);
    MSG = [MSG; zeros(padSize, 1)];  % Pad with zeros
end

% Convert the padded binary message into m-bit symbols
symbols = bi2de(reshape(MSG(1:totalBitsNeeded), m, []).', 'left-msb');

% Convert symbols to a Galois field array for GF(2^m)
MSG_gf = gf(symbols, m);
if size(MSG_gf, 1) > 1
    MSG_gf = MSG_gf.';  % Transpose to make it a row vector
end

% Encode the message using Reed-Solomon
RSSYMBS = rsenc(MSG_gf, n, k);
% Convert the encoded message back to binary
Symbols = double(RSSYMBS.x);  % Note: 'RSSYMBS.x' might not be needed depending on MATLAB version
symbolsToBit = de2bi(Symbols, m, 'left-msb');
RScodedx = reshape(symbolsToBit.', [], 1);
end


function RSdecoder = RSdecoder(RSC, EncodedMSG, m)
n = RSC(2);
k = RSC(1);

% Ensure the encoded message has the right number of bits
if mod(length(EncodedMSG), m) ~= 0
    error('The length of the encoded message must be a multiple of the symbol size m.');
end

% Reshape the received bitstream into m-bit symbols
encodedSymbols = bi2de(reshape(EncodedMSG, m, []).', 'left-msb');

% Convert these symbols into a Galois field array
EncodedMSG_gf = gf(encodedSymbols, m);
if size(EncodedMSG_gf, 1) > 1
    EncodedMSG_gf = EncodedMSG_gf.';  % Transpose to make it a row vector
end


% Assuming [decodedMsg, errNum] = rsdec(encodedMsg_gf, n, k);
[~,~,DecodedMSG_gf] = rsdec(EncodedMSG_gf, n, k,'end');
DecodedMSG_gf = DecodedMSG_gf(1:k);

% If DecodedMSG_gf is a Galois field array, then to convert its symbols back to binary:
DecodedSymbols = de2bi(double(DecodedMSG_gf.x), m, 'left-msb');


% Reshape to form the original binary bitstream
RSdecoder = reshape(DecodedSymbols.', [], 1);
end


function CONVcodedx = ConvCoder(Conv,MSG)
% Define the trellis structure for the convolutional encoder
trellis = poly2trellis(7, [171 133]); % Constraint length and generators

% Initialize the puncture pattern matrix and vector
pPatternVec = [];

% Determine the puncturing pattern based on the codeRate
switch Conv
    case '1/2'
        pPatternMat = [1; 1]; % No puncturing, pass all bits
    case '2/3'
        pPatternMat = [1 0; 1 1]; % Define C1 and C2 pattern for 2/3 rate
    case '3/4'
        pPatternMat = [1 0 1; 1 1 0]; % Define C1 and C2 pattern for 3/4 rate
    case '5/6'
        pPatternMat = [1 0 1 0 1; 1 1 0 1 0]; % Define C1 and C2 pattern for 5/6 rate
    case '7/8'
        pPatternMat = [1 0 0 0 1 0 1 0; 1 1 1 1 0 1 0 0]; % Example pattern
    otherwise
        error('Unsupported code rate');
end

% Reshape the puncture pattern matrix into a vector if not empty
if ~isempty(pPatternMat)
    pPatternVec = reshape(pPatternMat.', [], 1);
end

% Create the convolutional encoder with the specified trellis and puncturing pattern
convEncoder = comm.ConvolutionalEncoder('TrellisStructure', trellis,'PuncturePatternSource','Property' ,'PuncturePattern', pPatternVec,'TerminationMethod','Truncated');
% Encode the data
CONVcodedx = convEncoder(MSG);
end


function CONVdecodedx = ConvDecoder(Conv, EncodedMSG)
% Define the trellis structure for the convolutional encoder
trellis = poly2trellis(7, [171, 133]); % Constraint length and generators

% Initialize the puncture pattern matrix and vector
pPatternVec = [];

% Determine the puncturing pattern based on the codeRate
switch Conv
    case '1/2'
        pPatternMat = [1; 1]; % No puncturing
    case '2/3'
        pPatternMat = [1 0; 1 1]; % Define C1 and C2 pattern for 2/3 rate
    case '3/4'
        pPatternMat = [1 0 1; 1 1 0]; % Define C1 and C2 pattern for 3/4 rate
    case '5/6'
        pPatternMat = [1 0 1 0 1; 1 1 0 1 0]; % Define C1 and C2 pattern for 5/6 rate
    case '7/8'
        pPatternMat = [1 0 0 0 1 0 1 0; 1 1 1 1 0 1 0 0]; % Example pattern
    otherwise
        error('Unsupported code rate');
end

% Reshape the puncture pattern matrix into a vector if not empty
if ~isempty(pPatternMat)
    pPatternVec = reshape(pPatternMat.', [], 1);
end
%disp(pPatternVec);

% Create the Viterbi decoder with the specified trellis and puncturing pattern
viterbiDecoder = comm.ViterbiDecoder('TrellisStructure', trellis,'PuncturePatternSource','Property' , 'PuncturePattern', pPatternVec, 'InputFormat', 'Hard', 'TerminationMethod', 'Truncated','TracebackDepth',5*7);

% Make sure EncodedMSG is in double precision format
EncodedMSG = double(EncodedMSG(:));

% Decode the encoded message
CONVdecodedx = viterbiDecoder(EncodedMSG);
end
function Uh = MSKMOD(ebno,U,T)
msgSz = length(U);

Unrz =  2*U - 1; % Conversion to NRZ

ai = kron(Unrz(1:2:end),ones(1,2*T));  % Even bits
aq = kron(Unrz(2:2:end),ones(1,2*T));  % Odd bits

ai = [ai zeros(1,T)  ]; % Pads with zero for matching dimensions
aq = [zeros(1,T) aq ];  % Adds delay of T for Q

% Transmitting waveform
ct = cos(pi*(-T:msgSz*T-1)/(2*T));
st = sin(pi*(-T:msgSz*T-1)/(2*T));
X = 1/sqrt(T)*(ai.*ct + 1i*aq.*st);

% Gaussian noise channel
N0 = 1 / ebno;
W = (sqrt(N0/2)) * (randn(1,msgSz*T+T) + 1i*randn(1,msgSz*T+T));
Y = X + W;

% Integration over symbol period
Ye = conv(real(Y).*ct,ones(1,2*T));
Yo = conv(imag(Y).*st,ones(1,2*T));

% Decoding
Uh = zeros(1,msgSz);
Uh(1:2:end) = Ye(2*T+1:2*T:end-2*T) > 0 ; % even bits
Uh(2:2:end) = Yo(3*T+1:2*T:end-T) > 0 ;  % odd bitskdemod(Y, nsamp, [], zeros(1, 1));

end

function uh = BFSKMOD(ebno,U)
X = [~U, U]; % Encoding

N0 = 1 / ebno; % Noise spectral density
W = (sqrt(N0/2)) * randn(size(X)); % Additive gaussian vector
Y = X + W;
uh=(Y(:, 1) - Y(:, 2)) < 0;% Maximum likelihood decoding

end


function Uh = MFSKMOD(ebno,U)
S = eye(4);

% Ensure numSymbols is an integer
numSymbols = ceil(length(U) / 2);  % Or use ceil and handle padding as shown above
if mod(length(U), 2) ~= 0
    U = [U; 0];  % Pad with zero if necessary
end
% Map encoded bits to symbols
% symbols = bin2dec(reshape(U, 2, []).', 'left-msb') + 1;
symbols =bit2int(U,2);
% Vector representation of symbols using identity matrix
X = zeros(numSymbols, 4);
X(sub2ind(size(X), (1:numSymbols)', symbols+1)) = 1;

% Add Gaussian noise
N0 = 1 / ebno;
W = sqrt(N0/2) * randn(size(X));
Y = X + W;

% ML decoding of constellation
Xhat = zeros(size(X));
for i = 1:numSymbols
    for j = 1:4
        Xhat(i, j) = dot(Y(i, :), S(:, j));
    end
end

% Find the most likely transmitted symbols
[~, maxIndex] = max(Xhat, [], 2);
decodedSymbols = maxIndex-1;
Uh = int2bit(decodedSymbols,2);
% Convert symbols back to bits
% Uh = dec2bin(decodedSymbols, 2, 'left-msb');



end

