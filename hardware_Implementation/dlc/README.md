# Data link controller
The data link controller is structured over multiple files.  
- `protocol.py` contains the protocol structure and the main function of the controller.  
- `packet.py` packs incoming data to the correct packet and handles FEC.
  - FEC is only implemented as stub functions to emulate the changes in packet size.
- `gnuradio_interface.py` handles network connections with the PHY GNU Radio implementation.
- `MODCOD.json` contatins the look-up-table with MODCODs.
- gnuradio_test folder, has the PHY layer stub used in the module test.
