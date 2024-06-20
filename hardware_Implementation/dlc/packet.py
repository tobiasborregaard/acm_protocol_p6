import ctypes

from matplotlib.colors import to_hex
from numpy import byte, ceil, int8, pad, uint8
from sympy import N


class Packet:
    def __init__(self, Modcod=None, Data=b""):
        self.data = (Data)
        if Modcod is not None :
            self.modcod = Modcod
    
    def reedSolo(self, input):
        k = self.modcod['reed']['k']
        n = self.modcod['reed']['n']
        if len(input) % k != 0:
            input += (b'\x00' * (n - len(input)))
        #mchar = len(input) % n
        #if mchar != 0:
        input += (b'\xad' * (k - n))
        return input

    def convoCode(self, input):
        n = self.modcod['conv']['n']
        k = self.modcod['conv']['k']
        padLen = int(len(input) * (n / k) - len(input))
        input += (b'\xad' * padLen)
        return input


    def conc(self):
        out = self.convoCode(self.reedSolo(self.data))
        return out
    
    def postman(self):
        return (self.conc())
    

class Mail:
    def __init__(self, rx=None , modcod=None):
        self.data = rx
        if modcod is None:
            raise ValueError("Modulation and coding scheme must be provided")
        self.modcod = modcod

    def deconvoCode(self, encoded_data):
        n = self.modcod['conv']['n']
        k = self.modcod['conv']['k']
        if n < k:
            raise ValueError("Convolutional 'n' should be greater than 'k'")
        original_length = int(len(encoded_data) * (k / n))
        
        return encoded_data[:original_length]

    def deReedSolo(self, encoded_data):
        # Byt rundt
        k = self.modcod['reed']['n']
        n = self.modcod['reed']['k']
        if n < k:
            raise ValueError("Reed-Solomon 'n' should be greater than 'k'")
        original_length = int(len(encoded_data) - (n - k))
        return encoded_data[:original_length]

    def removePadding(self, encoded_data):
        encoded_data = encoded_data.rstrip(b'\xad')
        return encoded_data.rstrip(b'\x00')

    def deconc(self, encoded_data):
        return self.deReedSolo(self.deconvoCode(encoded_data))
    
    def mailman(self):
        return bytes(self.removePadding(self.deconc(self.data)))


class Framer():
    def __init__(self, data=b"", acm=None):
        if not isinstance(data, bytes):
            raise ValueError("Data must be bytes")
        
        self.data = data            
        self.acm = acm
        
    #selvdokumenterende
    def addACM(self ,input):
        # true = 11001100 = 0xCC
        # false = 00110011 = 0x33
        if self.acm:
            return b'\xCC' + input
        
        else:
            return b'\x33' + input
    #scramble for pakke frame ind
    def scramble(self,):
         
        #start byte 11101001 = 0xE9
        return b'\xAA'*5 +b'\xe9' + self.addACM(self.data)
    
    def descramble(self):
        dat = self.toUTF(self.data)
        if dat is None or len(dat) < 1:
            return None, None
        
        # Check control flags in the data
        try:
            if dat[1] == 0xCC:
                return True, dat[2:]
            elif dat[1] == 0x33:
                return False, dat[2:]
            else:
                return None, None  # Handle case where control byte does not match
        except IndexError as e:
            print(f"Index error when accessing data: {e}")
            return None, None
        

    
   

    def toUTF(self,input):
        rest_of_data = ""
        #convert to hex
        for byte in input:
            rest_of_data += hex(byte)[2:].zfill(2) 
        # print("Hexadecimal data:", rest_of_data)
        try:
            return bytes.fromhex(rest_of_data)
        except UnicodeDecodeError as e:
            print("Error decoding bytes to text:", e)
        except ValueError as e:
            print("Error converting hexadecimal to bytes:", e)





# # Example usage
# modcod = {
#     "reed": {'n': 255, 'k': 223},
#     "convolution": {'n': 2, 'k': 1}
# }
# packet = Packet(Modcod=modcod, Data=b"Harry Potter is dead, ehehehe!")
# # add start byte and end byte

# binary_data = b"deadlolololololkm "

# binary_data = packet.postman()
# frame = framer(data=binary_data, ACM=False)

# framer_data = frame.scramble()

# frame2 = framer(data=framer_data, ACM=False)
# acm, indata = frame2.descramble()
# mail = Mail(rx=indata, modcod=modcod)

# mail_data = mail.mailman()

# print(mail_data)
