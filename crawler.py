import os
import sys
import re
import mmap
from collections import Counter
import contextlib
from math import log
from porter import PorterStemmer

termSize = 15
xencode = { 0:"00",1:"01",2:"02",3:"03",4:"04",5:"05",6:"06",7:"07",8:"08",9:"09","a":"10","b":"11","c":"12","d":"13","e":"14","f":"15","g":"16","h":"17","i":"18","j":"19","k":"20","l":"21","m":"22","n":"23","o":"24","p":"25","q":"26","r":"27","s":"28","t":"29","u":"30","v":"31","w":"32","x":"33","y":"34","z":"35"}



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
termMapList = []

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
    global termsList,termData,termMapList
    offset = 0
    for term,data in termData.items():
        Sstr=term+" "+str(data[0])+" "+str(data[1])+getStr(data[2])
        termsList.append(Sstr)
        lenSstr = len(Sstr)
        termMapList.append(term+" "+str(offset)+" "+str(offset+lenSstr)+"\n")
        offset = offset+lenSstr

def fillTerms1(docID,lTerms):
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


def mergeTermFiles():
    for root, subFolders, files in os.walk("./indexes/tmp"):
        files.sort()

    linesToAdd = 0
    linesinFile = len(files)
    fullSize  = pow(2,int(log(linesinFile,2))+1)-1
    if (fullSize == linesinFile ):
        linesToAdd = 0
    elif (fullSize < linesinFile):
        fullSize2  = pow(2,int(log(linesinFile,2))+1)-1
        linesToAdd = fullSize2 - linesinFile
    else:
        linesToAdd = fullSize - linesinFile
        
    print(" Line to add : "+str(linesToAdd)+" mapSize"+str(linesinFile))
    while linesToAdd > 0:
        Str = "_"+str(linesToAdd) #+" "+makeFixedLengthStr(0,6)+" "+makeFixedLengthStr(0,6)+"\n"
         #   print("Adding Line")
        linesToAdd = linesToAdd-1
        files.append(Str)
       
    files.sort()



    termFile = "./indexes/termsx.txt"
    termMapFile = "./indexes/termsMapy.txt"
    with open(termFile, "wb") as f:
        f.write(b"*")
    with open(termFile, "r+b") as f:
        # memory-map the file, size 0 means whole file
        map = mmap.mmap(f.fileno(), 0)

    #with open(termMapFile, "wb") as f2:
     #   f2.write(b"*")
    with open(termMapFile, "wb") as f2:
        # memory-map the file, size 0 means whole file
      #  map2 = mmap.mmap(f2.fileno(), 0)
        

            

        byteLen = 0
        for filex in files:

            if (filex[0:1] != "_"):
                fx =  open("./indexes/tmp/"+filex, "r+b")
                # memory-map the file, size 0 means whole file
                map1 = mmap.mmap(fx.fileno(), 0)
                map1.seek(0)
                map.resize(map.size()+map1.size())
                map.write(map1[0:])
                #map.flush()
            
                
                Str = makeFixedLengthSpace(filex,20)+" "+makeFixedLengthStr(byteLen,6)+" "+makeFixedLengthStr(byteLen+map1.size(),6)+"\n"
                f2.write(Str.encode("utf-8"))
                byteLen = byteLen+map1.size()
            else:
                Str = makeFixedLengthSpace(filex,20)+" "+makeFixedLengthStr(0,6)+" "+makeFixedLengthStr(0,6)+"\n"
                f2.write(Str.encode("utf-8"))
               
            
            
            
            
    #map.close()
    #map1.close()
    #map2.flush()
    #map2.close()
            
def fillTerms(docID,lTerms):
    dWordsCnt = Counter(lTerms)
    for term,cnt in dWordsCnt.items():
        term = "./indexes/tmp/"+term
        lTermProp = []
        tf = cnt
        
        sdx = " "+str(docID)+" "+str(tf)
        if os.path.isfile(term): 
            with open(term, "a") as f:
                # memory-map the file, size 0 means whole file
                #map = mmap.mmap(f.fileno(), 0)
                #ctfx = int(map[0:6])
                #dfx = int(map[7:13])
                #sctfx=makeFixedLengthStr(ctfx+ctf,6)
                #sdfx =makeFixedLengthStr(dfx+df,6)
                #sx = sctfx+" "+sdfx+" "
                #map.seek(0)
                #map.write(sx.encode("utf-8"))
                #map.flush()
                
                #fileLen = map.size()
                
                #map.seek(fileLen-1)
                #map.resize(fileLen+len(sdx))
                #map.write(sdx.encode("utf-8"))
                f.write(sdx)
                f.close()
                #map.flush()
                #map.close
        else:
            with open(term, "w") as f:
                f.write( term+" "+sdx)
                f.close()
            #with open(term, "r+b") as f:
                # memory-map the file, size 0 means whole file
             #   map = mmap.mmap(f.fileno(), 0)
                #sctfx=makeFixedLengthStr(ctf,6)
                #sdfx =makeFixedLengthStr(df,6)
              #  sx = str(docID)+" "+str(tf)
              #  map.seek(0)
              #  map.resize(map.size()+len(sx))
              #  sx=sx.encode("utf-8")
              #  map.write(sx)
              #  map.close

        



def getDocStuff(dDocProps):
    global T,W,B,A,N,I
    lAllLists = []
    if (T in dDocProps):
        lAllLists.append(dDocProps[T])
    if (W in dDocProps):
        lAllLists.append(dDocProps[W])
    #if (B in dDocProps):
    #    lAllLists.append(dDocProps[B])
    if (A in dDocProps):
        lAllLists.append(dDocProps[A])
    #if (N in dDocProps):
    #    lAllLists.append(dDocProps[N])

    lAllLines = []
    for lList in lAllLists:
        lAllLines.extend(lList)
    
    lAllWords = []
    for sLine in lAllLines:
        lWords = sLine.split()
        lAllWords.extend(lWords)

    lAllWords = remStopWords(lAllWords)

    p = PorterStemmer()
    lAllWordsStemmed = []
    for word in lAllWords:
        word = p.stem(word,0,len(word)-1)
        lAllWordsStemmed.append(word)
    #print("All words :", lAllWordsStemmed,"\n")
    lUniqueWords = list(set(lAllWordsStemmed))
    lenAllWords = len(lAllWordsStemmed)
    lenAllWords
    sRet = makeFixedLengthStr(len(lAllWordsStemmed),6)+" "+makeFixedLengthStr(len(lUniqueWords),6) #+":"+dDocProps[B][0]
    return [sRet,lAllWordsStemmed]

def makeFixedLengthStr(length,n):
    sLen =  str(length)
    zeros=""
    #print(n-len(sLen))
    while (n-len(sLen)) > 0:
        zeros=zeros+"0"
        #print(zeros)
        n=n-1
        
    zeros = zeros+sLen
    #print(zeros)
    return zeros

def makeFixedLengthSpace(length,n):
    sLen =  str(length)
    zeros=""
    #print(n-len(sLen))
    while (n-len(sLen)) > 0:
        zeros=zeros+" "
        #print(zeros)
        n=n-1
        
    zeros = sLen+zeros
    #print(zeros)
    return zeros



def makeIndexes():
    global T,W,B,A,N,I,dFileData,termData,termsList,termMapList
    docFile = "./indexes/d3.txt"
    docWordsFile = "./indexes/docWords.txt"
    termsFile = "./indexes/terms.txt"
    termsMapFile = "./indexes/termsMap.txt"
    docList = []
    lDocWords = []
    lTerms = []
    
    with open(docFile, "wb") as f:
     f.write(b"Hello Python!\n")

    with open(docFile, "r+b") as f:
        
        # memory-map the file, size 0 means whole file
        map = mmap.mmap(f.fileno(), 0)
        map.resize(5000*14)
        for docID,dProps in dFileData.items():
            docList.append(makeFixedLengthStr(int(docID),6)+" "+getDocStuff(dProps)[0]+"\n")
            map.seek(int(docID)*14)
            str1 = getDocStuff(dProps)[0]+"\n"
            map.write(str1.encode("utf-8"))
            sAllWords = " ".join(getDocStuff(dProps)[1])
            lDocWords.append(docID+":"+sAllWords+"\n")
            fillTerms(docID,getDocStuff(dProps)[1])
        

       
        map.close()
    
    mergeTermFiles()    
    makeTermsList()
    #FILE = open(docFile,"w")
    FILE1 = open(docWordsFile,"w")
    FILE2 = open(termsFile,"w")
    FILE3 = open(termsMapFile,"w")
    # Write all the lines at once:
    #FILE.writelines(docList)
    FILE1.writelines(lDocWords)
    FILE2.writelines(termsList)
    FILE3.writelines(termMapList)    

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


main(sys.argv[1])

