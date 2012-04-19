import constants
import sys
import os
import shutil
import helperFunctions

def main():
    #if os.path.exists(constants.allCollsDir): 
     #   shutil.rmtree(constants.allCollsDir)
    createIndexStructure()
    createFile(constants.docFile)
    createFile(constants.docCacheFile)
    createFile(constants.termsFile)
    createFile(constants.fSortedTermIndex)
    createFile(constants.collFile)
    createFile1(constants.SortedCacheIndex)
def createIndexStructure():
    createDir(constants.allCollsDir)
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

def createFile1(fileName):
    with open(fileName, "w") as f:
        f.write(helperFunctions.makeFixedLengthSpace("\n",18))
    f.close()

#To delete all the unnecessary files
def cleanup():
    shutil.rmtree(constants.termsDir)
    #os.remove(constants.fSortedTermIndex)
