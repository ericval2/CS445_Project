import os
import re

#create function that will locate the log folder from the partent directory and the alert file from the log folder
def locReadFile():
    #locate the log folder from the parent directory
    parentDir = os.getcwd()
    logDir = 'log'
    logFolder = os.path.join(parentDir, logDir)
    #locate the alert file from the log folder
    alertFile = os.path.join(logFolder, 'alert.txt')
    #open the alert file for reading
    f = open(alertFile, 'r')
    fileContent = f.read()
    f.close()

    return fileContent


#parse first line in contentToParse, find the word alert and save the rest of line
def parseFirstComment(contentToParse):
    #split the contentToParse into lines
    lines = contentToParse.splitlines()
    #get the first line
    firstLine = lines[0]
    #find the word alert
    search = re.search('alert', firstLine)
    #get the index of the word alert
    searchIndex = search.start()
    #get the rest of the line
    comment = firstLine[searchIndex + 5:]
    #remove the last 4 characters from the comment
    comment = comment[:-4]
    #return the comment 
    return comment

#parse the third line in contentToParse, find the ip first address and save it
def parseIP(contentToParse):
    #split the contentToParse into lines
    lines = contentToParse.splitlines()
    #get the third line
    thirdLine = lines[3]
    #find the ip address
    search = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', thirdLine)
    #get the index of the ip address
    searchIndex = search.start()
    #get the ip address
    ip = thirdLine[searchIndex:]
    #remove the port number from the ip address and everything after it
    ip = ip.split(':')[0]
    #return the ip address
    return ip

#parse the comment for the words XMAS, FIN, or NULL
def ifStatement(comment, ip):
    # define sudo iptables -A INPUT string
    sudoIptables = 'sudo iptables -A INPUT'
    # define snort rule string for FIn scan
    snortRuleFin = ' -p tcp --tcp-flags ALL FIN'
    # define snort rule string for NULL scan
    snortRuleNull = ' -p tcp --tcp-flags ALL NULL'
    # define snort rule string for XMAS scanc
    snortRuleXmas = ' -p tcp --tcp-flags ALL FIN,PSH,URG'
    # define snort rule string for ACK scan
    snortRuleAck = ' -p tcp --tcp-flags ALL ACK'
    #define snort rule string for Full Connect scan
    snortRuleFullCon = ' -p tcp --syn'
    # define reject string
    reject = '-j REJECT --reject-with tcp-reject'

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
    elif 'Full Connect' in comment:
        fullConDefend = sudoIptables + ' ' + ipAddr + snortRuleFullCon + ' ' + reject
        return fullConDefend
    else:
        return 'No known scan detected'


def main():
    content = locReadFile()     #locate and read the alert file
    comment = parseFirstComment(content)     #parse the first line of the alert file
    ipAddr = parseIP(content)        #parse ip address call in 3rd line of alert file
    defend = ifStatement(comment, ipAddr)        #if statement call for if the comment contains the words XMAS, FIN, or NULL
    print(defend)
    #os.system(defend)       #run the defend command in the terminal

if __name__ == "__main__":
    main()