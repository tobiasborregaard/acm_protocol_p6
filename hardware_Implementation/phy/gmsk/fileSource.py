import zmq
import numpy as np
import time

context = zmq.Context()
socket: zmq.Socket = context.socket(zmq.REP)

socket.bind("tcp://*:5555")


integers = [np.random.randint(0, 100) for _ in range(10000)]

# Write integers to a text file
filename1 = r"C:\Users\chri0\Documents\GitHub\SDR_Ground_Station\hardwareImplementation\phy\gmsk\integers.txt"
with open(filename1, 'w') as file:
    for integer in integers:
        file.write(str(integer) + '\n')

vals = []
with open(filename1, 'r') as f:
    for line in f:
        int_vals = np.byte(line.strip())
        vals.append(int_vals)


time.sleep(1)
for i in vals:
    socket.recv()
    print(f"got here {i}")
    socket.send(i)

time.sleep(10)
rec = np.fromfile(r"C:\Users\chri0\Documents\GitHub\SDR_Ground_Station\hardwareImplementation\phy\gmsk\integers_received.txt", dtype=np.byte)
# print(rec[0:32])
# print(vals[0:32])
vals = np.array(vals)
print(np.array_equal(vals, rec))
rec[31] = 0
print(np.array_equal(vals, rec))

print(1)

