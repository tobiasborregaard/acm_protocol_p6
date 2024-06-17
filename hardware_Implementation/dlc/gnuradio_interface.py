from queue import Queue
from typing import Any
import zmq
import enum
from dataclasses import dataclass
import pmt

@dataclass
class instructions_dataclass:
    addr: str
    name: str
    type: Any
class instructions(enum.Enum):
    # modcodrecv =    {"addr":"mux", "name":"modcod", "type":str}
    # modCodTx =      {"addr":"demux", "name":"modcod", "type":str}
    # snr =           {"addr":"awgn", "name":"snr", "type":float}
    # testSnr =       {"addr":"snr_meas", "name":"snr", "type":float}
    modCodRecv  = [instructions_dataclass("demux", "modcod", str), instructions_dataclass("demux_1", "modcod", str)]
    modCodTx    = [instructions_dataclass("mux", "modcod", str), instructions_dataclass("mux_1", "modcod", str)]
    testSnr     = instructions_dataclass("awgn", "snr", float)
    snr         = instructions_dataclass("snr_meas", "snrAvg", float) 





class sockets():
    context = zmq.Context()

    def __init__(self):
        pass



class recvSock(sockets):
    def __init__(self, ip = "localhost", port = 5557):
        super().__init__()
        self.socket = super().context.socket(zmq.REQ)
        self.socket.connect("tcp://" + ip + ":" + str(port))
        self.dataqueue = Queue()
        return

    def recv(self):
        while True:
            self.socket.send_string("")
            r = self.socket.recv()
            #r = np.frombuffer(r, dtype=np.uint8)
            r = bytearray(r)
            # Ask if gnuradio is ready
            # Get one byte
            for val in r:
                self.dataqueue.put(val)
            # byte
            

    def run(self):
        self.recv()
        pass

    # def sync(self):
    #     # 0xe9
    #     # ringbuff = 8bytes
    #     # recvSockObject.dataqueue.get() -> Returns byte
    #     # Data = []
    #     # Syncword fundet? : Bool
    #         # Yes:
    #             # Smid i data (Forskudt)
    #         # Nej:
    #             # Kør rundt i ringbuffer
    #         # Frame done:
    #             # Synword fundet: False
    #     return




class transmitSock(sockets):
    def __init__(self, ip = "*", port = 5558):
        super().__init__()
        self.socket = super().context.socket(zmq.REP)
        self.socket.bind("tcp://" + ip + ":" + str(port))
        return
     
    #Wrappes i Async
    def send(self, bytes: bytearray): 
        for byte in bytes:
            self.socket.recv()
            self.socket.send((byte.to_bytes()))
        return

class cmdSock(sockets):
    def __init__(self, serverIp = "*", serverPort = 5555, gnuRadioIp="localhost", gnuRadioPort = 5556):
        super().__init__()
        self.cmdTx = super().context.socket(zmq.PUB)
        self.cmdTx.bind("tcp://"+ serverIp + ":" + str(serverPort))
        self.cmdRx = super().context.socket(zmq.SUB)
        self.cmdRx.setsockopt_string(zmq.SUBSCRIBE, "")
        self.cmdRx.connect("tcp://" + gnuRadioIp + ":" + str(gnuRadioPort))
        return

    def protocol(self, get: bool, var: instructions_dataclass, val = None):
        req = []
        req.append(var.addr)
        if get:
            req.append("get")
        else:
            req.append("set")
        req.append({var.name:val})
        return pmt.to_pmt(req)     
    
    #Return any
    def getVar(self, var: instructions):
        instruction = []
        if type(var.value) == list:
             instruction = var.value
        else:
            instruction.append(var.value)
        tmp = []
        for index in instruction:
            req = self.protocol(True, index)
            self.cmdTx.send(pmt.serialize_str(req))
            r = self.cmdRx.recv()
            r = pmt.to_python(pmt.deserialize_str(r))

            if type(r) == str:
                if r.lower().startswith("err"):
                    raise Exception(r)
            elif type(r) == list:
                if len(instruction) == 1:
                    return r[1][index.name]
                else:
                    tmp.append(r[1][index.name])
        
        #raise Exception("You are not supposed to get here")
        
        return tmp

    def setVar(self, var: instructions, val):
        instruction = []
        if type(var.value) == list:
             instruction = var.value
        else:
            instruction.append(var.value) 
        for index in instruction:
            if index.type != type(val):
                raise Exception(f"Wrong type {index.name} uses {index.type} you gave {type(val)}")
            req = self.protocol(False, index, val)
            self.cmdTx.send(pmt.serialize_str(req))
            r = self.cmdRx.recv()
            r = pmt.to_python(pmt.deserialize_str(r))

            if type(r) == str:
                if r.lower().startswith("err"):
                    raise Exception(r)
            elif type(r) == list:
                if r[1][index.name].lower() != "ok":
                    raise Exception(r[1])
            
        return "ok"
        #raise Exception("You are not supposed to get here")


if __name__ == "__main__":
    from threading import Thread
    import numpy as np
    import time
    cmd = cmdSock()
    send = transmitSock()
    rx = recvSock()
    
    def input_handler():
        while True:
            inp = input()
            inp = inp.split()
            if int(inp[0]) == 0:
                print(cmd.getVar(instructions.testSnr))
            elif int(inp[0]) == 2:
                print(cmd.getVar(instructions.modCodTx))
            elif int(inp[0]) == 1:
                cmd.setVar(instructions.testSnr, float(inp[1]))
            elif int(inp[0]) == 3:
                cmd.setVar(instructions.modCodTx, str(inp[1]))
    def test():
        t_in = Thread(target=input_handler)
        t_in.start()
        t_recv = Thread(target=rx.recv)
        t_recv.start()


        # data = np.random.randint(255, size=int(1e4), dtype=np.uint8)
        # data_bytearr = bytearray(data.tobytes())
        # t_send = Thread(target=send.send, args=(data_bytearr,))
        # t_send.start()
        
        # recv = np.zeros(len(data), dtype=np.uint8)
        # counter = 0
        # while len(recv) > counter:
        #     recv[counter] = np.uint8(rx.dataqueue.get())
        #     print(counter)
        #     counter += 1
        
        # print(np.array_equal(recv, data))
        # time.sleep(5)
        while True:
            
            # for i in range(1, 14):
            #     cmd.setVar(instructions.modCodTx, str(i))
            #     time.sleep(0.1)
            pass
        return

    test()

    print("Done")
