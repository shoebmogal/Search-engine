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

from math import log
from porter import PorterStemmer
from collections import Counter


def main():
    helperFunctions.populateStopWords()
    print("Started.")
    crawlFile()
    print("Done with crawling.")
    mapCreator.mergeTermFiles()
    print("Done with merging")
    mapCreator.makeTermBTree()

def writeDocIndex(docID,strToWrite):
    with open(constants.docFile, "r+b") as f:
        map = mmap.mmap(f.fileno(), 0)
        docFileSize = map.size()
        seekTo = int(docID)*constants.docSize
        if(seekTo >= (docFileSize)):
            map.resize(docFileSize+(2*constants.docSize))
        map.seek(seekTo)
        map.write(strToWrite.encode(constants.encoding))
        map.close




def getDocStuff(dDocProps):
    lAllLists = []
    if (constants.T in dDocProps):
        lAllLists.append(dDocProps[constants.T])
    if (constants.W in dDocProps):
        lAllLists.append(dDocProps[constants.W])
    if (constants.A in dDocProps):
        lAllLists.append(dDocProps[constants.A])

    lAllLines = []
    for lList in lAllLists:
        lAllLines.extend(lList)
    
    lAllWords = []
    for sLine in lAllLines:
        lWords = sLine.split()
        lAllWords.extend(lWords)

    lAllWords = helperFunctions.remStopWords(lAllWords)

    p = PorterStemmer()
    lAllWordsStemmed = []
    for word in lAllWords:
        word = p.stem(word,0,len(word)-1)
        lAllWordsStemmed.append(word)

    lUniqueWords = list(set(lAllWordsStemmed))
    lenAllWords = len(lAllWordsStemmed)

    sRet = helperFunctions.makeFixedLengthStr(len(lAllWordsStemmed),constants.docWordCntLen)+constants.space+helperFunctions.makeFixedLengthStr(len(lUniqueWords),constants.docWordCntLen)+constants.newLine

    return [sRet,lAllWordsStemmed]
                
def makeTermFiles(docID,lTerms):
    dWordsCnt = Counter(lTerms)
    for term,cnt in dWordsCnt.items():
        term = constants.termsDir+"/"+term
        lTermProp = []
        tf = cnt
        sdx = " "+str(docID)+" "+str(tf)
        if os.path.isfile(term): 
            f= open(term, "a")
            f.write(sdx)
            f.close()
        else:
            f=  open(term, "w")
            f.write( term+" "+sdx)
            f.close()




def writeToIndexFiles(docID,dData):    
    lDocData = getDocStuff(dData)
    writeDocIndex(docID,lDocData[0])
    makeTermFiles(docID,lDocData[1])
    
   
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

        
                

