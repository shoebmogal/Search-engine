import constants
import sys
import os
import porter
import helperFunctions
import os
import sys
import re
import mmap
import contextlib
import mapCreator
#import compression
import copy

from math import log
from porter import PorterStemmer
from collections import Counter

byteLenD = 0

def main():
    helperFunctions.populateStopWords()
    print("Started.")
    crawlFile()
    print("Done with crawling.")
    mapCreator.mergeTermFiles()
    print("Done with merging")
    mapCreator.makeTermBTree()
    makeCollFile()
   

def writeDocIndex(docID,strToWrite):
    constants.numDocs = constants.numDocs+1
    with open(constants.docFile, "r+b") as f:
        map = mmap.mmap(f.fileno(), 0)
        docFileSize = map.size()
        seekTo = int(docID)*constants.docSize
        if(seekTo >= (docFileSize)):
            map.resize(docFileSize+(2*constants.docSize))
        map.seek(seekTo)
        map.write(strToWrite.encode(constants.encoding))
        map.close

def stemList(list1):
    p = PorterStemmer()
    lAllWordsStemmed = []
    for word in list1:
        word = p.stem(word,0,len(word)-1)
        lAllWordsStemmed.append(word)
    return lAllWordsStemmed

dPlace = {}
def putinDPLace(place,list1):
    global dPlace
 #   print(list1)
    x = ""
    for l2 in list1:
        l3 = stemList(helperFunctions.remStopWords(l2.split()))
        for w in l3:
#            print(w)
            if w in dPlace:
                x = dPlace[w]
            dPlace[w] = x+place

def getDocStuff(dDocProps):
    lAllLists = []

    if (constants.T in dDocProps):
        lAllLists.append(dDocProps[constants.T])
        putinDPLace("1",dDocProps[constants.T])
    if (constants.W in dDocProps):
        lAllLists.append(dDocProps[constants.W])
        putinDPLace("2",dDocProps[constants.W])
    if (constants.A in dDocProps):
        lAllLists.append(dDocProps[constants.A])
        putinDPLace("3",dDocProps[constants.A])

    lAllLines = []
    for lList in lAllLists:
        lAllLines.extend(lList)
    
    lAllWords = []
    for sLine in lAllLines:
        sLine = re.sub('[^a-zA-Z0-9]', ' ', sLine)
        lWords = sLine.lower().split()
        lAllWords.extend(lWords)
    lw = copy.deepcopy(lAllWords)
    lAllWords = helperFunctions.remStopWords(lAllWords)

    p = PorterStemmer()
    lAllWordsStemmed = []
    for word in lAllWords:
        word = p.stem(word,0,len(word)-1)
        lAllWordsStemmed.append(word)

    lUniqueWords = list(set(lAllWordsStemmed))
    lenAllWords = len(lAllWordsStemmed)
    constants.allDocsLen = constants.allDocsLen+lenAllWords
    sRet = helperFunctions.makeFixedLengthStr(len(lAllWordsStemmed),constants.docWordCntLen)+constants.space+helperFunctions.makeFixedLengthStr(len(lUniqueWords),constants.docWordCntLen)+constants.newLine

    return [sRet,lAllWordsStemmed," ".join(lw)]
                


def makeTermFiles(docID,lTerms):
    global dPlace
    print(dPlace)
    dWordsCnt = Counter(lTerms)
    for term,cnt in dWordsCnt.items():
        term = constants.termsDir+"/"+term
        lTermProp = []
        tf = cnt
        sdx = str(docID)+" "+str(tf) #+" "+dPlace[term.split("/")[-1]]
        #sdx=helperFunctions.makeFixedLengthStr(docID,4)+helperFunctions.makeFixedLengthStr(tf,3)
        #sdx = compression.encode(sdx)
        if os.path.isfile(term): 
            constants.numTerms=constants.numTerms+1
            f= open(term, "a")
            f.write(sdx)
            f.close()
        else:
            constants.numTerms=constants.numTerms+1
            constants.numUniqueTerms=constants.numUniqueTerms+1
            f=  open(term, "w")
            f.write(sdx)
            f.close()
    dPlace.clear()


def makeCollFile():
    f = open(constants.collFile,"w")
    Str = str(constants.IndexName)+constants.space
    Str = Str + str(constants.numDocs)+constants.space+str(constants.numTerms)
    Str = Str + constants.space+str(constants.numUniqueTerms)
    Str = Str + constants.space+str(constants.allDocsLen/constants.numDocs)
    f.write(Str)
    f.close()


def makeDocCacheBTree():
    f = open(constants.SortedCacheIndex, 'r')
    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    f2 = open(constants.docCacheBTreeFile, "wb")
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





def makeTermStr(byteStart,byteEnd):
    Str = helperFunctions.makeFixedLengthStr(byteStart,8)
    Str = Str+constants.space
    Str = Str+helperFunctions.makeFixedLengthStr(byteEnd,8)+constants.newLine
    return Str


def makeDocCache(docID,AllWords):
    global byteLenD
    fx = open(constants.docCacheFile, "a")
    fx.write(AllWords)
    fx.close
    f2 =  open(constants.SortedCacheIndex, "ab")
    Str = makeTermStr(byteLenD,byteLenD+len(AllWords))
    byteLenD = byteLenD+len(AllWords)
    f2.write(Str.encode(constants.encoding))
    f2.close()    
    

def writeToIndexFiles(docID,dData):    
    lDocData = getDocStuff(dData)
    writeDocIndex(docID,lDocData[0])
    makeTermFiles(docID,lDocData[1])
    makeDocCache(docID,lDocData[2])
    
def crawlFile():
        filex =  open(constants.filetoIndex,encoding=constants.encoding) 
        dFileContents = {} # {title:S,contents:S,date:S,author:S,entryDate:S}
        dFile={} # {docID:dFileContents}
        previousProp=""
        for line in filex:
            if(len(line)>2):
                line = line.replace("\n","")
                if(line[0:2] == ".I"): #("Line has docID
                   
                    if(len(dFileContents) !=0):
                        writeToIndexFiles(docID,dFileContents)
                        dFileContents={}
                        
                    docID = line.split()[1]
                    previousProp=constants.I
                elif(line[0:2] == ".T"): #("Line has title ")
                    previousProp=constants.T
                elif(line[0:2] == ".W"): #("Line has contents")
                    previousProp=constants.W
                elif(line[0:2] == ".B"): #("Line has date of pub")
                    previousProp=constants.B
                elif(line[0:2] == ".A"): #("Line has Author")
                    previousProp=constants.A
                elif(line[0:2] == ".N"): #("Line has ENtry Date")
                    previousProp=constants.N
                elif(line[0:2] == ".X"): #("Line has reference")
                    previousProp=constants.X
                else :
                    tempX = []
                    if( previousProp == constants.T or previousProp == constants.W or previousProp == constants.A):
                        if(previousProp in dFileContents):
                            tempX = dFileContents[previousProp]
                        line = re.sub('[^a-zA-Z0-9]', ' ', line)
                        tempX.append(line.lower())
                        dFileContents[previousProp]=tempX

        
                

