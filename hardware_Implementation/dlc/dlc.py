
import zmq
import pmt
import numpy
import json

import threading
import time

context = zmq.Context()
send = context.socket(zmq.PUB)
recv = context.socket(zmq.SUB)
recv.setsockopt_string(zmq.SUBSCRIBE,"")
send.bind("tcp://*:5555")
recv.connect("tcp://localhost:5556")

# def timeout(time) {

# }

my_variables = {"freq":1000}
while True:
    #message = input()
    # try:
    #     message = json.loads(message)
    #     print("loaded json")
    # except:
    #     continue
    dst, act, var, val = input().split()
    message = [dst, act, {var:json.loads(val)}]
    send.send(pmt.serialize_str(pmt.to_pmt(message)))
    m = recv.recv()
    print(m)
    m = pmt.deserialize_str(m)
    m = pmt.to_python(m)
    print(m)
    if m[0] == "set":
        for keys in m[1]:
            my_variables[keys] = m[1][keys]
    #print("done")