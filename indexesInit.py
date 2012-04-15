import constants
import sys
import os
import shutil
import helperFunctions

def main():
    shutil.rmtree(constants.indexDir)
    createIndexStructure()
    createFile(constants.docFile)
    createFile(constants.docWordsFile)
    createFile(constants.termsFile)
    createFile(constants.fSortedTermIndex)
def createIndexStructure():
    createDir(constants.indexDir)
    createDir(constants.termsDir)

def createDir(sDir):
    sNewpath = sDir
    if not os.path.exists(sNewpath): 
        os.makedirs(sNewpath)

def createFile(fileName):
    with open(fileName, "w") as f:
        f.write(helperFunctions.makeFixedLengthSpace("\n",constants.docSize))
    f.close()

#To delete all the unnecessary files
def cleanup():
    shutil.rmtree(constants.termsDir)
    os.remove(constants.fSortedTermIndex)
