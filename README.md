# Data exfiltration POC (server, client)

This is a POC of deta exfiltration on port 80, using python , taking some measurs to obfuscate.

Common fiulds for client and server are in single configuration file.

## Client side

* Having massage on file (can be set of files).
* Creating a 32 bytes key.
* Saving key on file.
* Creating a 16 bytes IV.
* Encrypting with AES EAX the message using the key and IV.
* Encoding IV to base64.
* Getting hash of base64 message sum (sha256)
* Splitting message to random length of strings and adding numerator for each string.
* Encoding each munbered pached to base64.
* Sending b64 IV with random phrase header to server.
* Sending each packet with random phrase header to server.
* Sleeping for random time (from 1 to 3 sec)
* Sending b64 check hash with closing phrase header to server.


## Server side

* Listening on port 80 and whaiting for start signal.
* Start recording data when found a phrase from random fuild prases in packet hedear.
* Recording all data until close phrase in packet header.
* Sending 200 response when getting packets
* puting packets in dict, spliting numerators and sorting by keys.
* Extracting IV and checksum from dict and decoding from base64.
* Combining dict to string.
* Getting hash of base64 message sum (sha256) and comparing to one from client.
* If OK, decoding message from base64.
* Reading key from file
* Decrypting message using key and IV.
* DONE !

## Usage:
1. Modify server IP address on client sctipt.
2. Modify sending message file (or create a script for all .docx files).
3. Run server script on C2 computer.
4. Generated key from client need to be shared with server.
5. Run client script on dedicated computer.

## TODO
1. Client side - send packets on computer HTTP requests to obfuscate trafic.
2.  C2 server to generate random key, client will ask for key to encrypt data.
3.  Use HTTPS communication.