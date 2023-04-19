#Script to continuously scan well known ports.
#Chooses between a variety of stealth scans, and full connect scanning.
import os
import sys
import random
import time

targetIP = "192.168.56.102"

def portScan(scanType, portNumber):
	scan = "nmap -s" + scanType + " -p " + portNumber + " " + targetIP
	print(scan)
	#Have terminal conduct scan
	os.system(scan)
	#sleep to allow Ctrl+C to end script and not just start next scan
	time.sleep(1)
	
#Randomly Generate the Scan Type
def chooseScanType():
	randomNum = random.randint(0,4)
	if randomNum == 0:
		return "A"
	elif randomNum == 1:
		return "N"
	elif randomNum == 2:
		return "X"
	elif randomNum == 3:
		return "F"
	else:
		return "T"

#Randomly Generate Port Number Between Well-Known Ports
def choosePortNum():
	return random.randint(0, 1023)

#Present main menu to user
def menuInput():
	print("What kind of scan would you like to do?")
	print("1. Randomized scans on well known ports")
	print("2. Scan of first 1000 ports")
	print("3. Exit")
	return input()
	
#Present scan options to user
def scanInput():
	print("What type of scan would you like to run?")
	print("1. Full Connect Scan")
	print("2. Fin Scan")
	print("3. Null Scan")
	print("4. XMAS Scan")
	print("5. Ack Scan")
	print("6. Exit")
	return input()

#Determine the type of scan being conducted
def userScan(userType):
	if userType == "1":
		os.system("nmap -sT " + targetIP)
	elif userType == "2":
		os.system("nmap -sF " + targetIP)
	elif userType == "3":
		os.system("nmap -sN " + targetIP)
	elif userType == "4":
		os.system("nmap -sX " + targetIP)
	elif userType == "5":
		os.system("nmap -sA " + targetIP)
	elif userType == "6":
		return
	else:
		print("Please enter a valid number")
		
def main():
	while(True):
		version = menuInput()
		if version == "1":
			while(True):
				scanType = chooseScanType()
				portNumber = str(choosePortNum())
				portScan(scanType, portNumber)
		elif version == "2":
			userType = scanInput()
			userScan(userType)
			
		elif version == "3":
			print("Exiting")
			break
		else:
			print("Please enter a valid number")

if __name__ == "__main__":
	main()
