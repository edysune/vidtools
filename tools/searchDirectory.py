from genericpath import isdir
import json 
import os
from os import listdir
from os.path import isfile, join

#todo:
# 1) write single file to json
#   Contents include:
#       <Directory Path (absolute), File>
#           Directory Path = string?
#           File = <string, file type, file size>

# Note: May need a way to group together similiar directories instead of just using absolute paths?

# 2) Compare 2 directories against each other - may need to look into GUI options? GUI options implies that we need a config file saved for this with reading/writing capabilities.

# 3) See about writing these types of things to a database

# 4) Create a GUI for this

# 5) Once in a database, should write some type of logic to merge into existing database

# 6) Should create logic around databases pulling information from database resource sites
# - Title Recommendations, Seasons, Episodes that do/don't exist, incomplete libraries, shows that are not found, bad structures of stuff

# 7) Possible additions to functionality like mass renaming of episodes and structures, update libraries logs, scan libraries for new data 

# 8) Possible subtitle downloading and merging? Not sure how useful this would be.

directoryToSearch1 = "../test_dir/a1";
directoryToSearch2 = "../test_dir/a2";

class fileStructure:
    def __init__(self):
        self.files = dict()
    
    def addFile(self, file):
        if self.files.get(file.getPath()) == None:
            self.files[file.getPath()] = [ file ]
        else:
            self.files[file.getPath()].append(file)

    def printFiles(self):
        for key in self.files.keys():
            tabChr = '\t'
            print(f'\n{tabChr * self.files[key][0].tab}{key}')
            for f in self.files[key]:
                f.printFile(True)

class file:
    def __init__(self, path, fileName, tab):
        self.path = path
        self.fileName = fileName
        self.size = os.path.getsize(join(path, fileName))
        self.tab = tab
    
    def getSize(self, conversion = "KB"):
        conversionRate = 1
        conversion = conversion.upper()

        if conversion == "B":
            return f'{self.size} {conversion}'

        #todo: refactor this, this is done horribly but shouldn't have much problems with simple data
        if conversion == "KB":
            conversionRate = 1000
        elif conversion == "MB":
            conversionRate = 1000000
        elif conversion == "GB":
            conversionRate = 1000000000

        return f'{self.size / conversionRate} {conversion}'

    def getFileName(self):
        return self.fileName

    def getPath(self):
        return self.path

    def getFile(self):
        return {
            "path": self.path,
            "fileName": self.fileName,
            "size": self.getSize()
        }


    def printFile(self, toConsole = False):
        tabChr = '\t'
        printedFile = f'{tabChr * self.tab}{self.fileName} ({self.getSize()})'
        if (toConsole):
            print(printedFile)
        return printedFile



def main():
    directory1 = fileStructure()
    searchDirectory(directoryToSearch1, directory1, 0)
    directory1.printFiles()

def searchDirectory(currentDir, fStruct, tab):
    for fname in listdir(currentDir):
        #print(nextFile)
        nextFile = join(currentDir, fname)
        if isdir(nextFile):
            searchDirectory(nextFile, fStruct, tab + 1)
        elif isfile(nextFile):
            fStruct.addFile(file(currentDir, fname, tab))




main()
