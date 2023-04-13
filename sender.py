import os
import time
import sys
import hashlib

receiverIP = "192.168.56.102"
fileToSend = "textfile.txt"
bufferSize = 1024 
previousSha = None
	
#Create SHA1 hash of a file
def file_hasher(filename):
	sha1 = hashlib.sha1()
   
	with open(filename,'rb') as file:
		inputBlock = 0
		while inputBlock != b'':
			inputBlock = file.read(1024)
			sha1.update(inputBlock)
           
	return sha1.hexdigest()
	
#Loop sending for as long as program is needed
while(True):
	finalHash = file_hasher(fileToSend)
	#Check if hash is different, send if it is
	if(previousSha != finalHash):
		print("Sending")	
		os.system("nc -w 3 " + receiverIP + " 1234 < " + fileToSend)
		previousSha = finalHash
		
	print("Beginning sleep")	
	time.sleep(10)
	print("Starting again")
		
