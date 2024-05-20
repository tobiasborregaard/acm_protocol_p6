# ACM for the AAUSAT Ground Station
The project is a proposed adaptive controlled modulation (ACM) protocol for the AAU student space ground station. The source code features GNURadio implementation of different modulation and encoding schemes (MODCODs) compatible with the CC1101 satellite transceiver. The aim of the protocol is optimizing goodput in a satellite link by varying the MODCODs, when link conditions change the channel SNR. 

## Usage
The project elements are subdivided by folders. The [modCodPreset](modcodEstimations) are the simulated result of goodput and SNR threshold value at a constant bit error rate for the different MODCODs. [snr_change_over_pass](snr_change_over_pass) contains calculation of the change in channel SNR during an orbital pass from link budget estimates. Finally, the [hardwareImplementation](hardwareImplementation) has the PHY and DLC GNURadio code for the ACM protocol.

## Prerequisites 
**Software** \
Simulation: MATLAB (+ Communications Toolbox), Python \
Implementation: GNURadio companion

**Hardware** \
Ettus USRP X300 (with UBX160 daughterboard) \
https://www.ettus.com/all-products/x300-kit/ 

## Contact
Direct questions regarding the project to
cnielo21@student.aau.dk

## Contributors
- Jonas Ellegaard Jakobsen
- Tobias Reimer Borregaard
- Tobias Thelin Marburger
- Christian Kjærsgaard Nielsen