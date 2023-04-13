import os
import time
import shutil

incomingFile = "textfile.txt"
copiedFile = "newFile.txt"

#copy listening file into a different file
def copy_file():
	shutil.copyfile(incomingFile, copiedFile)

#Loop listen for as long as program is needed
while(True):	
	print("Listening")
	#Open port 1234 for listening, write to txt
	os.system("nc -l -p 1234 > " + incomingFile)
	print("Beginning Wait")
	time.sleep(5)
	copy_file()
	time.sleep(5)
	print("Starting again")
