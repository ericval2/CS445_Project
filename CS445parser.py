import os
import re

#create function that will locate the log folder from the partent directory and the alert file from the log folder
def locReadFile():
    #locate the log folder from the parent directory
    parentDir = os.getcwd()
    logDir = 'log'
    logFolder = os.path.join(parentDir, logDir)
    #locate the alert file from the log folder
    alertFile = os.path.join(logFolder, 'newFile.txt') 
    #open the alert file for reading
    f = open(alertFile, 'r+')
    fileContent = f.read()
    f.truncate(0)
    f.close()
    #print(fileContent)
    #erase contents of file


    return fileContent


#function that parses comments
def parseComments(contentToParse):
    split = contentToParse.splitlines()
    lineInt = len(split)
    #create a list that will hold the comments
    commentLines = []
    #parse comment lines which are every 6th line
    for i in range(0, lineInt):
        if i % 6 == 0:
            commentLines.append(split[i])

    return commentLines


#function that parses ip addresses
def parseIPAddrs(contentToParse):
    split = contentToParse.splitlines()
    lineInt = len(split)
    #create a list that will hold the ips
    ipLines = []
    #loop through the lines and parse the ip addresses
    for i in range(0, lineInt):
        if i % 6 == 3:
            ipLines.append(split[i])

    altIPLines = []

    #loop through iplines and get the first ip address of every line
    for i in range(0, len(ipLines)):
        #find the ip address
        search = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ipLines[i])
        #get the index of the ip address
        searchIndex = search.start()
        #get the ip address
        ip = ipLines[i][searchIndex:]
        #remove the port number from the ip address and everything after it
        ip = ip.split(':')[0]
        #append the ip address to the altIPLines list
        altIPLines.append(ip)

    return altIPLines


#parse the comment for the words XMAS, FIN, or NULL
def ifStatement(comment, ip):
    # define sudo iptables -A INPUT string
    sudoIptables = 'sudo iptables -A INPUT -s'
    # define snort rule string for FIn scan
    snortRuleFin = ' -p tcp --tcp-flags ALL FIN'
    # define snort rule string for NULL scan
    snortRuleNull = ' -p tcp --tcp-flags ALL NONE'
    # define snort rule string for XMAS scanc
    snortRuleXmas = ' -p tcp --tcp-flags ALL FIN,PSH,URG'
    # define snort rule string for ACK scan
    snortRuleAck = ' -p tcp --tcp-flags ALL ACK'
    # define reject string
    reject = '-j REJECT --reject-with tcp-reset'

    ipAddr = ip

    #if statements for if the comment contains the words XMAS, FIN, or NULL
    if 'XMAS' in comment:
        xmasDefend = sudoIptables + ' ' + ipAddr + snortRuleXmas + ' ' + reject
        return xmasDefend
    elif 'FIN' in comment:
        finDefend = sudoIptables + ' ' + ipAddr + snortRuleFin + ' ' + reject
        return finDefend
    elif 'NULL' in comment:
        nullDefend = sudoIptables + ' ' + ipAddr + snortRuleNull + ' ' + reject
        return nullDefend
    elif 'ACK' in comment:
        ackDefend = sudoIptables + ' ' + ipAddr + snortRuleAck + ' ' + reject
        return ackDefend
    else:
        return 'No known scan detected'


def main():

    while os.stat('log/newFile.txt').st_size != 0:
        file = locReadFile()
        comments = parseComments(file)
        ips = parseIPAddrs(file)
        #loop through both comments and ips and input into ifStatement function
        for i in range(0, len(comments)):
            os.system(ifStatement(comments[i], ips[i]))
        print("Parsed")
    

if __name__ == "__main__":
	while(True):
		main()
