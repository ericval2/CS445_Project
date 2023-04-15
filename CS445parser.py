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


#parse first line in contentToParse, find the word sudo and save the rest of line
def parseFile(contentToParse):
    #split the contentToParse into lines
    lines = contentToParse.splitlines()
    #get the first line
    firstLine = lines[0]
    #find the word sudo
    sudo = re.search('sudo', firstLine)
    #get the index of the word sudo
    sudoIndex = sudo.start()
    #get the rest of the line
    comment = firstLine[sudoIndex + 5:]
    #remove the last 4 characters from the comment
    comment = comment[:-4]
    #return the comment 
    return comment



def main():
    content = locReadFile()
    newContent = parseFile(content)
    print(newContent)

if __name__ == "__main__":
    main()