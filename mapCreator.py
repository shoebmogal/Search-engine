import os
import sys
import re
import mmap
from collections import Counter
import contextlib
from math import log
from porter import PorterStemmer
import helperFunctions
import constants


def getLinesToAdd(linesinFile):
    fullSize  = pow(2,int(log(linesinFile,2))+1)-1
    if (fullSize == linesinFile ):
        linesToAdd = 0
    elif (fullSize < linesinFile):
        fullSize2  = pow(2,int(log(linesinFile,2))+1)-1
        linesToAdd = fullSize2 - linesinFile
    else:
        linesToAdd = fullSize - linesinFile
    return linesToAdd

def addDummyTerms(files,linesToAdd):
    while linesToAdd > 0:
        Str = constants.underscore+str(linesToAdd)
        linesToAdd = linesToAdd-1
        files.append(Str)
    return files

def makeTermStr(term,byteStart,byteEnd):
    Str = helperFunctions.makeFixedLengthSpace(term,constants.termSize)
    Str = Str+constants.space
    Str = Str+helperFunctions.makeFixedLengthStr(byteStart,constants.byteLen)
    Str = Str+constants.space
    Str = Str+helperFunctions.makeFixedLengthStr(byteEnd,constants.byteLen)+constants.newLine
    return Str

def mergeTermFiles():
    files = os.listdir(constants.termsDir)
    linesinFile = len(files)
    linesToAdd = getLinesToAdd(linesinFile)
    files = addDummyTerms(files,linesToAdd)
    files.sort()

    f = open(constants.termsFile, "r+b")
    map = mmap.mmap(f.fileno(), 0)
        
    fr =  open(constants.termsListFile,"w")
    
    f2 =  open(constants.fSortedTermIndex, "wb")

    byteLen = 0
    for filex in files:
        if (filex[0:1] != constants.underscore):
            fr.write(filex+constants.space)
            fx =  open(constants.termsDir+"/"+filex, "r+b")
            map1 = mmap.mmap(fx.fileno(), 0)
            map1.seek(0)
            map.resize(map.size()+map1.size())
            map.write(map1[0:])
            Str = makeTermStr(filex,byteLen,byteLen+map1.size())
            byteLen = byteLen+map1.size()
        else:
            Str = makeTermStr(filex,0,0)

        f2.write(Str.encode(constants.encoding))
               
    fr.close()   
    f2.close()
    map.close()
    f.close()



def makeTermBTree():
    f = open(constants.fSortedTermIndex, 'r')
    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    f2 = open(constants.termBTreeFile, "wb")
    termSize = constants.termLineSize
    print("termSize ",termSize)
    def bst(iStart,iEnd,m):
        lenList = int(iEnd-iStart)
        if(lenList != 0):
            middle = (lenList-1)/2
            middle=int(round(middle, 0))
            middle = middle+iStart
            f2.write(m[middle*termSize:(middle*termSize+termSize)])
            bst(iStart,middle,m)
            bst(middle+1,iEnd,m)
        else:
            blankStr = helperFunctions.makeFixedLengthSpace("\n",termSize)
            f2.write(blankStr.encode(constants.encoding))
            
    bst(0,int(m.size()/termSize),m)


