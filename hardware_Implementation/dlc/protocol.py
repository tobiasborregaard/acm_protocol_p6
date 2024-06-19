import logging
import json
import asyncio
import threading
import time
import numpy as np
from matplotlib.pylab import rand
from packet import *
from gnuradio_interface import *
import cmd
import subprocess
import glob
import os

# Setup logging
logging.basicConfig(level=logging.DEBUG, format=' %(levelname)s - %(message)s\n')

class Protocol:
    def __init__(self, Earth=None, Message=None):
        self.earth = Earth
        self.message = Message
        self.messageQueue = asyncio.Queue()
        self.ringBuff = bytearray(b'')
        self.received = 0
        with open('MODCOD.json') as f:
            self.MODCODS = json.load(f)
        self.modcod = self.MODCODS["1"]
        self.txmodcod = self.MODCODS["1"]
        self.ctrl = cmdSock()
        self.send = transmitSock()
        self.recv = recvSock()
        thread = threading.Thread(target=self.recv.run)
        thread.start()
        self.lastT = time.time()
        self.found = False
        self.txmaxLength = self.modcod['reed']['k']*(self.modcod["conv"]["n"] /self.modcod['conv']['k'])
        self.txmaxPayloadLength = self.modcod['reed']['n']
        self.rxmaxLength = self.modcod['reed']['k']*(self.modcod["conv"]["n"] /self.modcod['conv']['k'])
        self.txmaxPayloadLength = self.modcod['reed']['n']

        self.background_task = asyncio.create_task(self.syncByteRingBuffer())

    async def run_protocol(self):
        tasks = [
            asyncio.create_task(self.manage_communications()),
            asyncio.create_task(self.check_state()),
        ]
        while True:
            await asyncio.sleep(0.01)

    async def initialize_sockets(self):
        logging.info("Initializing sockets...")
        # First makesure not running 
        if self.ctrl is not None:
            del self.ctrl
        if self.send is not None:
            del self.send
        if self.recv is not None:
            del self.recv

        self.ctrl = cmdSock()
        self.send = transmitSock()
        self.recv = recvSock()
        thread = threading.Thread(target=self.recv.run)
        thread.start()
        self.background_task = asyncio.create_task(self.syncByteRingBuffer())

    async def manage_communications(self):
        while True:
            if self.messageQueue.empty():
                await asyncio.sleep(0.5)
            else:
                await self.msgQueue()
                await asyncio.sleep(0.01)

    async def check_state(self):

        while True:
            if time.time()-self.lastT >= 15: # 30 sec
                self.txupdateModcod(self.MODCODS["1"])
                self.updateModcod("1")
                # self.received = 0
                self.lastT = time.time()

                await asyncio.sleep(0.01)
            if self.received >= 10: 
                self.received = 0
                await self.setModcod()
                self.lastT = time.time()
                await asyncio.sleep(0.01)

            else:
                await asyncio.sleep(0.05)

    async def loadMSG(self, message):
        await self.chunkMessage(message)

    async def chunkMessage(self, message):
        if len(message) > self.txmaxPayloadLength:
            tempMSG = [message[i:i + int(self.txmaxPayloadLength)] for i in range(0, len(message), int(self.txmaxPayloadLength))]
            for i in tempMSG:
                await self.addtoQueue(bytes(i))
        else:
            await self.addtoQueue(message)

    async def addtoQueue(self, message):
        await self.messageQueue.put(message)

    async def msgQueue(self):
        message = await self.messageQueue.get()
        await self.sendMessage(message, acm=False)
        self.messageQueue.task_done()  # If needed

    async def syncByteRingBuffer(self):
        await asyncio.sleep(0.01)
        while True:
            if len(self.ringBuff) < 2 and not self.found:
                try:
                    if self.recv.dataqueue.empty():
                        await asyncio.sleep(0.1)
                    else:
                        data = self.recv.dataqueue.get()
                        self.ringBuff.append(data)
                        self.recv.dataqueue.task_done()
                except asyncio.TimeoutError:
                    logging.warning("Timeout waiting for data")
                    continue
            else:
                cache = bytes(self.ringBuff)
                index = self.findStartByte(cache)
                self.lastT = time.time()
                if index != -1:
                    self.found = True
                    msgCollect = self.ringBuff[:]
                    if int(self.rxmaxLength) == 1:
                        self.rxmaxLength = 255
                    retries = 100
                    
                    while len(msgCollect) <= int(self.rxmaxLength) + 3:
                        try:
                            data = self.recv.dataqueue.get(timeout=0.01)
                            msgCollect.append(data)
                            self.recv.dataqueue.task_done()
                            if self.recv.dataqueue.empty():
                                await asyncio.sleep(0.04)
                                continue                                
                        except Exception as e:
                            # logging.error(f"Error while collecting additional data: {e}")
                            retries -= 1
                            if retries == 0:
                                break
                            else:
                                continue
                    if index != 0:
                        msgCollect = self.extractAndShiftData(msgCollect, 0, index)
                    msgCollect = bytes(msgCollect)
                    await self.processReceivedMessage(msgCollect)
                    self.ringBuff.clear()
                    cache = bytes(self.ringBuff)
                    self.found = False
                else:
                    self.ringBuff[0] = self.ringBuff.pop(1)
                    self.found = False

    def findStartByte(self, bytestocheck):
        startbyte = 0xE9

        for i in range(1, len(bytestocheck)):
            data1, data2 = bytestocheck[i-1], bytestocheck[i]
            new_byte = data1

            for x in range(8):  
                if new_byte == startbyte:
                    return x  # Return index for start byte

                new_byte = ((new_byte << 1) | ((data2 >> (7-x)) & 1)) & 0xFF

            if new_byte == startbyte:
                return 0

        return -1

    def extractAndShiftData(self, Data, start_index, bit_shifts):
        shifted_data = []
        if start_index < len(Data):
            current_byte = Data[start_index]
            next_bits = 0

            if start_index + 1 < len(Data):
                next_bits = Data[start_index + 1]
            for i in range(start_index, len(Data) - 1):
                new_byte = ((current_byte << bit_shifts) | (next_bits >> (8 - bit_shifts))) & 0xFF
                shifted_data.append(new_byte)
                current_byte = Data[i + 1]
                if i + 2 < len(Data):
                    next_bits = Data[i + 2]
                else:
                    next_bits = 0

        return shifted_data

    async def processReceivedMessage(self, message):
        acm, msg = Framer(data=message).descramble()
        msg = Mail(rx=msg, modcod=self.modcod).mailman()

        if msg is None:
            logging.warning("Received message is None, skipping processing.")
            return  # Exit the function if msg is None

        if acm:
            try:
                decoded_msg = msg.decode()
                logging.info(f"ACM: {decoded_msg}")
                jsonMSG = json.loads(decoded_msg)
                self.txupdateModcod(jsonMSG)
                self.received = 0
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON from message: {e}")
            self.received = 0
        else:
            self.received += 1
            try:
                pass
                #logging.info(f"Received message: {msg}")
            except UnicodeDecodeError as e:
                logging.error(f"Error decoding message: {e}")

    async def sendMessage(self, message, acm):
        SENDmodcod = {"reed": self.txmodcod["reed"], "conv": self.txmodcod["conv"]}
        data = bytearray(Framer(data=Packet(Data=message, Modcod=SENDmodcod).postman(), acm=acm).scramble())
        self.send.send(data)

    async def generate_data_stream(self, num_packets):
        """ Generate a stream of '10' and load it into the message queue. """
        logging.info("Generating data stream...")
        packet_size = int(self.txmaxPayloadLength)
        for _ in range(num_packets):
            rand_packet = np.random.randint(0, 255, packet_size, dtype=np.uint8) # Generate a packet of random bytes
            rand_packet = rand_packet.tobytes()           
            await self.addtoQueue(rand_packet)  # Add the packet to the message queue
            await asyncio.sleep(0.01)  # Yield control to avoid blocking
        logging.info(f"Generated {num_packets} packets.")

    async def setModcod(self):
        snr = self.ctrl.getVar(instructions.snr)
        self.updateModcod(self.snrTHR(snr))
        message = json.dumps(self.modcod).encode()
        logging.info(f"Sending ACM: {message}")
        await self.sendMessage(message, acm=True)

    def updateModcod(self, modcodSET):
        logging.info(f"Setting modcod to {modcodSET}")
        self.modcod = self.MODCODS[modcodSET]
        if self.modcod["reed"]["n"] == "Uncoded":
            self.modcod["reed"]["n"] = 223
            self.modcod["reed"]["k"] = 255
            self.modcod["conv"]["n"] = 1
            self.modcod["conv"]["k"] = 1
        self.rxmaxLength = self.modcod['reed']['k']*(self.modcod["conv"]["n"] /self.modcod['conv']['k'])
        self.rxmaxPayloadLength = self.modcod['reed']['n']
        self.ctrl.setVar(instructions.modCodRecv, modcodSET)

    def txupdateModcod(self, modcodSET):
        self.txmodcod = modcodSET
        if self.txmodcod["reed"]["n"] == "Uncoded":
            self.txmodcod["reed"]["n"] = 1
            self.txmodcod["reed"]["k"] = 1
            self.txmodcod["conv"]["n"] = 1
            self.txmodcod["conv"]["k"] = 1
        self.txmaxLength = self.modcod['reed']['k']*(self.modcod["conv"]["n"] /self.modcod['conv']['k'])
        self.txmaxPayloadLength = self.modcod['reed']['n']
        self.ctrl.setVar(instructions.modCodTx, str(self.matchModcod(modcodSET)))

    def snrTHR(self, inSNR):
        if inSNR < self.MODCODS["1"]["THR"]:
            return "1"

        tempkey = 0
        for key, mod in self.MODCODS.items():
            if inSNR > mod['THR']:
                tempkey += 1
            else:
                return str(tempkey)
        return str(tempkey)

    def matchModcod(self, modcod):
        for key, mod in self.MODCODS.items():
            if mod["THR"] == modcod["THR"]:
                logging.info(f"Matching modcod found: {key}")
                return key
        logging.warning("No matching modcod found, returning default modcod.")
        return "1"


class ProtocolCLI(cmd.Cmd):
    intro = '''Welcome to the ACM Protocol CLI. Type help or ? to list commands.
    Type exit to exit the CLI.
    Type send <message> to send a message.
    Type setmodcod <modcod_id> to set the modulation and coding scheme.
    Type status to print the current status of the protocol.
    Type generate_data to send packets of random values.
    Type set_received <value> to set the received count.
    Type reinit_sockets to reinitialize the command, transmit, and receive sockets.
    Type run_test to execute the test.py script.
    Type setsnr <value> to set the SNR between 2-14.
    Type kill to stop the test.py script.'''
    prompt = '<<>ACM<>> '

    def __init__(self, loop, protocol):
        super().__init__()
        self.loop = loop
        self.protocol = protocol
        self.test_process = None
        self.data_stream_task = None

    def do_generate_data(self, arg):
        """Generate a stream of data: generate_data <num_packets>"""
        try:
            num_packets = int(arg.strip())
            if num_packets <= 0:
                logging.error("The number of packets must be a positive integer.")
                return
            self.loop.create_task(self.protocol.generate_data_stream(num_packets))
            logging.info(f"Generating {num_packets} packets of data.")
        except ValueError:
            logging.error("Invalid number of packets. Please enter a positive integer.")
    

    def do_send(self, arg):
        'Send a message: SEND <message>'
        if not arg.strip():
            logging.error("Error: The message cannot be empty.")
            return
        self.loop.create_task(self.protocol.loadMSG(arg.encode()))

    def do_setmodcod(self, arg):
        'Set the modulation and coding scheme: SETMODCOD <modcod_id>'
        self.loop.create_task(self.set_modcod(arg))

    async def set_modcod(self, arg):
        try:
            self.protocol.updateModcod(arg)
        except KeyError:
            logging.error(f'Invalid modcod ID: {arg}')

    def do_setsnr(self, arg):
        'Set the SNR: setsnr <value>'
        try:
            value = float(arg)
            self.protocol.ctrl.setVar(instructions.snr, value)
            logging.info(f'Set SNR to {value}')
        except ValueError:
            logging.error('Invalid value for SNR. Please enter a floating-point number.')

    def do_status(self, arg):
        'Print the current status of the protocol'
        logging.info(f'Earth: {self.protocol.earth}')
        logging.info(f'Message: {self.protocol.message}')
        logging.info(f'Received: {self.protocol.received}')
        logging.info(f'Modcod: {self.protocol.modcod}')
        logging.info(f'Txmodcod: {self.protocol.txmodcod}')

    def do_set_received(self, arg):
        'Set the received count: SET_RECEIVED <value>'
        try:
            value = int(arg)
            self.protocol.received = value
            logging.info(f'Set received to {value}')
        except ValueError:
            logging.error('Invalid value for received count. Please enter an integer.')

    def do_reinit_sockets(self, arg):
        'Reinitialize the command, transmit, and receive sockets: REINIT_SOCKETS'
        self.loop.create_task(self.protocol.initialize_sockets())
        logging.info("Sockets have been reinitialized.")

    def do_run_test(self, arg):
        'Run the test.py script: RUN_TEST'
        if not arg.strip():
            arg = "gnuradio_test/test.py"  # Default to "test.py" if no argument is provided
        if not os.path.isfile(arg):
            logging.error(f"Error: The file '{arg}' does not exist.")
            return
        if self.test_process:
            logging.error("Error: test.py is already running.")
            return
        try:
            self.test_process = subprocess.Popen(['python3', arg], start_new_session=True)
            logging.info(f"Script '{arg}' is running.")
        except Exception as e:
            logging.error(f"Failed to run script '{arg}': {e}")

    def do_kill(self, arg):
        'Kill the running test.py script: KILL'
        if self.test_process:
            self.test_process.terminate()
            self.test_process = None
            logging.info("test.py has been terminated.")
        else:
            logging.error("No test.py script is running.")

    def do_exit(self, arg):
        'Exit the CLI'
        if self.test_process:
            self.test_process.terminate()
            self.test_process = None
            logging.info("test.py has been terminated.")
        logging.info('Exiting...')
        return True

    # Tab completion methods
    def complete_send(self, text, line, begidx, endidx):
        if not text:
            completions = ['send ']
        else:
            completions = [f'send {text}']
        return completions

    def complete_setsnr(self, text, line, begidx, endidx):
        if not text:
            completions = ['setsnr ']
        else:
            completions = [f'setsnr {text}']
        return completions

    def complete_setmodcod(self, text, line, begidx, endidx):
        if not text:
            completions = ['setmodcod ']
        else:
            completions = [f'setmodcod {text}']
        return completions

    def complete_status(self, text, line, begidx, endidx):
        if not text:
            completions = ['status ']
        else:
            completions = [f'status {text}']
        return completions

    def complete_set_received(self, text, line, begidx, endidx):
        if not text:
            completions = ['set_received ']
        else:
            completions = [f'set_received {text}']
        return completions

    def complete_reinit_sockets(self, text, line, begidx, endidx):
        if not text:
            completions = ['reinit_sockets ']
        else:
            completions = [f'reinit_sockets {text}']
        return completions

    def complete_run_test(self, text, line, begidx, endidx):
        # Use glob to find matching files
        if not text:
            completions = glob.glob('*.py')  # List all .py files in the current directory
        else:
            completions = glob.glob(text + '*.py')  # List all files matching the current text
        return completions


async def main():
    loop = asyncio.get_event_loop()
    proto = Protocol(Earth=True)
    cli = ProtocolCLI(loop, proto)

    cli_thread = threading.Thread(target=cli.cmdloop)
    cli_thread.start()

    await proto.run_protocol()

    cli_thread.join()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        logging.info("Cleaning up...")
