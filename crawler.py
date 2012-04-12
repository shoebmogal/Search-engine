import os
import sys
import re
from collections import Counter


#dFileContents = {} # {title:L,contents:L,date:L,author:L,entryDate:L}
dFileData = {} # {docID:dFileContents}
T ="T" #"title"
W = "W" #"contents"
B = "B" #"date"
A = "A" #"author"
N = "N" # "entryDate"
I = "I" # "docID"
X = "X" #ref
termData = {} # term:L[ctf:df:D[docid:tf]]
termsList = []
stopwords_l = []

def populateStopWords():
    with open('stoplist.txt',encoding='utf-8') as stopwords_file:
        for line in stopwords_file:
            stopwords_l.append(line.replace("\n",""))

def remStopWords(query_l):
    words_l = []
    for word_s in query_l:
        if not word_s in stopwords_l:
            words_l.append(word_s)
    return words_l



def getStr(dictP):
    sRet = ""
    for key, value in dictP.items():
        sRet = sRet +" "+ str(key)+ " "+str(value)
    return sRet


def makeTermsList():
    global termsList,termData
    for term,data in termData.items():
        termsList.append(term+" "+str(data[0])+" "+str(data[1])+getStr(data[2])+"\n")

def fillTerms(docID,lTerms):
    global termData
    dWordsCnt = Counter(lTerms)
    for term,cnt in dWordsCnt.items():
       lTermProp = []
       ctf = tf = cnt
       df = 1
       lTermProp = [ctf,df,{docID:tf}]
       if term in termData:
           lTermPropX = termData[term]
           ctfX = lTermPropX[0]
           dfX = lTermPropX[1]
           tfX = lTermPropX[2]
           lTermProp[0] = ctf+ctfX
           lTermProp[1] = df+dfX
           tfX[docID] = tf
           lTermProp[2] = tfX

       termData[term] = lTermProp

def getDocStuff(dDocProps):
    global T,W,B,A,N,I
    lAllLists = []
    if (T in dDocProps):
        lAllLists.append(dDocProps[T])
    if (W in dDocProps):
        lAllLists.append(dDocProps[W])
    if (B in dDocProps):
        lAllLists.append(dDocProps[B])
    if (A in dDocProps):
        lAllLists.append(dDocProps[A])
    if (N in dDocProps):
        lAllLists.append(dDocProps[N])

    lAllLines = []
    for lList in lAllLists:
        lAllLines.extend(lList)
    
    lAllWords = []
    for sLine in lAllLines:
        lWords = sLine.split()
        lAllWords.extend(lWords)


    #print("All words :", lAllWords,"\n")
    lUniqueWords = list(set(lAllWords))
    sRet = str(len(lAllWords))+":"+str(len(lUniqueWords))+":"+dDocProps[B][0]
    return [sRet,lAllWords]

def makeIndexes():
    global T,W,B,A,N,I,dFileData,termData,termsList
    docFile = "docFile.txt"
    docWordsFile = "docWords.txt"
    termsFile = "terms.txt"

    docList = []
    lDocWords = []
    lTerms = []

    for docID,dProps in dFileData.items():
        docList.append(docID+":"+getDocStuff(dProps)[0]+"\n")
        sAllWords = " ".join(getDocStuff(dProps)[1])
        lDocWords.append(docID+":"+sAllWords+"\n")
        fillTerms(docID,getDocStuff(dProps)[1])

    makeTermsList()
    FILE = open(docFile,"w")
    FILE1 = open(docWordsFile,"w")
    FILE2 = open(termsFile,"w")
    # Write all the lines at once:
    FILE.writelines(docList)
    FILE1.writelines(lDocWords)
    FILE2.writelines(termsList)
    

def fetchFromFile(fileName):
    global T,W,B,A,N,I,dFileData
    with open(fileName,encoding='utf-8') as inLinksFile:
        dFileContents = {} # {title:S,contents:S,date:S,author:S,entryDate:S}
        dFile={} # {docID:dFileContents}
        previousProp=""
        for line in inLinksFile:
            #print(line[0:2])
            if(len(line)>2):
                line = line.replace("\n","")
                if(line[0:2] == ".I"):
                    #print("Line has docID")
                    dFileData.update(dFile)
                    dFile={}
                    dFileContents={}
                    dFile[line.split()[1]]=dFileContents
                    #print(dFile)
                    previousProp=I
                elif(line[0:2] == ".T"):
                    #print("Line has title ")
                    previousProp=T
                elif(line[0:2] == ".W"):
                    #print("Line has contents")
                    previousProp=W
                elif(line[0:2] == ".B"):
                    #print("Line has date of pub")
                    previousProp=B
                elif(line[0:2] == ".A"):
                    #print("Line has Author")
                    previousProp=A
                elif(line[0:2] == ".N"):
                    #print("Line has ENtry Date")
                    previousProp=N
                elif(line[0:2] == ".X"):
                    #print("Line has reference")
                    previousProp=X
                else :
                    #print()
                    tempX = []
                    if( previousProp != X):
                        if(previousProp in dFileContents):
                            tempX = dFileContents[previousProp]
                        #print("tempX : ",tempX)
                        line = re.sub('[^a-zA-Z0-9]', ' ', line)
                        tempX.append(line.lower())
                        dFileContents[previousProp]=tempX

        dFileData.update(dFile)
                

    #print(dFileData)
    makeIndexes()






def main(fileName):
    print("Started indexing : "+fileName)
    populateStopWords()
    fetchFromFile(fileName)
#print(d)


#main(sys.argv[1])
