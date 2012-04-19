#Search
#This will search the indexes and give relevant data
#!/usr/bin/python3

import re
import xml.etree.ElementTree as etree
import math
from operator import itemgetter
from http.client import HTTPConnection
from urllib.request import urlopen
import porter
import searchIndexes
import helperFunctions
import searchConstants
import os
import constants
import porter
import copy
import sys

totalResults = 0
lTotalDB = []
user = ""

queryDict = {}
avgQLen = 0.0
queries_oktf_dict = {}
db_no = 0
db_info = {}
term_ctf_df_d = {}
doc_d  = {}
doc_len = {}

vs1_dict = {}
vs2_dict = {}
myx1_d = {}
lm_d = {}
Jelin_d = {}
BM_d = {}
SBM_d = {}
docs_map = {}


vector_space = {}
vector_space_sorted = {}
    
vector_space2 = {}
vector_space_sorted2 = {}
    
laplace_d = {}
laplace_sorted_d = {}
       
JM_d ={}
JM_sorted_d = {}
        
BM25_d = {}
BM25_sorted_d = {}

SBM25_d = {}
SBM25_sorted_d = {}

mx1_d = {}
mx1_sorted_d = {}


collDict = {}

termsDict = {}

def reset():

    global queryDict 
    global avgQLen 
    global queries_oktf_dict 
    global term_ctf_df_d 
    global doc_d  
    global doc_len 
    
    global vs1_dict 
    global vs2_dict 
    global myx1_d 
    global lm_d 
    global Jelin_d 
    global BM_d 
    global SBM_d 
    global docs_map 
    
    
    global vector_space 
    global vector_space_sorted 
    
    global vector_space2 
    global vector_space_sorted2 
    
    global laplace_d 
    global laplace_sorted_d 
    
    global JM_d
    global JM_sorted_d 
    
    global BM25_d 
    global BM25_sorted_d 
    
    global SBM25_d 
    global SBM25_sorted_d 
    
    global mx1_d 
    global mx1_sorted_d 
    

    global termsDict 
    
    queryDict.clear()
    avgQLen = 0.0
    queries_oktf_dict.clear()
    
    term_ctf_df_d.clear()
    doc_d.clear()
    doc_len.clear()
    
    #vs1_dict.clear()
    vs2_dict.clear()
    myx1_d.clear()
    lm_d.clear()
    Jelin_d.clear()
    BM_d.clear()
    SBM_d.clear()
    docs_map.clear()
    

    vector_space.clear()
    vector_space_sorted.clear()
    
    vector_space2.clear()
    vector_space_sorted2.clear()
    
    laplace_d.clear()
    laplace_sorted_d.clear()
       
    JM_d.clear()
    JM_sorted_d.clear()
        
    BM25_d.clear()
    BM25_sorted_d.clear()

    SBM25_d.clear()
    SBM25_sorted_d.clear()

    mx1_d.clear()
    mx1_sorted_d.clear()


#    collDict.clear()

    termsDict.clear()








def readCollections():
    collDir = os.listdir(searchConstants.allCollsDir)
    #print(searchConstants.allCollsDir)
    for indexDir in collDir:
        fName = searchConstants.allCollsDir+"/"+indexDir+searchConstants.collFileP
        #print(fName)
        fl = open(fName,"r")
        linec = fl.read()
        #print(linec)
        fl.close()
        wordList = linec.split()
        Dict = {"num_docs":int(wordList[1]),"num_terms":int(wordList[2]),"num_unique_terms":int(wordList[3]),"ave_doc_len":float(wordList[4])}
        db_info[int(wordList[0])] = Dict



def setQueryDict(qID,dDocProps):
    global queryDict

    lAllLists = []
    if (constants.N in dDocProps):
        lAllLists.append(dDocProps[constants.N])
    if (constants.W in dDocProps):
        lAllLists.append(dDocProps[constants.W])
    if (constants.A in dDocProps):
        lAllLists.append(dDocProps[constants.A])

    lAllLines = []
    for lList in lAllLists:
        lAllLines.extend(lList)
    
    lAllWords = []
    for sLine in lAllLines:
        sLine = re.sub('[^a-zA-Z0-9]', ' ', sLine)
        lWords = sLine.lower().split()
        lAllWords.extend(lWords)

    lAllWords = helperFunctions.remStopWords(lAllWords)

    p = porter.PorterStemmer()
    lAllWordsStemmed = []
    for word in lAllWords:
        word = p.stem(word,0,len(word)-1)
        lAllWordsStemmed.append(word)
        #print("All stemmed : ",lAllWordsStemmed)
    queryDict[qID] = lAllWordsStemmed


def setUserQueryDict(Query):
    global queryDict
    lAllWords = []
    sLine = re.sub('[^a-zA-Z0-9]', ' ', Query)
    lWords = sLine.lower().split()
    lAllWords.extend(lWords)

    lAllWords = helperFunctions.remStopWords(lAllWords)

    p = porter.PorterStemmer()
    lAllWordsStemmed = []
    for word in lAllWords:
        word = p.stem(word,0,len(word)-1)
        lAllWordsStemmed.append(word)
        #print("All stemmed : ",lAllWordsStemmed)
    queryDict[0] = lAllWordsStemmed

    

def setAvgQLen():
    global queryDict,avgQLen
    n = len(queryDict)
    #print(queryDict)
    dLen =0
    for k,v in queryDict.items():
        dLen = dLen+len(v)
        
    avgQLen = (dLen/n)





def readQueries():
        filex =  open(searchConstants.qFile,encoding=constants.encoding) 
        dFileContents = {} # {title:S,contents:S,date:S,author:S,entryDate:S}
        dFile={} # {docID:dFileContents}
        previousProp=""
        for line in filex:
            if(len(line)>2):
                line = line.replace("\n","")
                if(line[0:2] == ".I"): #("Line has docID
                   
                    if(len(dFileContents) !=0):
                        setQueryDict(docID,dFileContents)
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

            setQueryDict(docID,dFileContents)


def get_oktf_queries():
    global queries_oktf_dict
    global queryDict
    global avgQLen
    global avg_query_len_i
    for q_key,q_value_l in queryDict.items():
        query_oktf_d = {}
        for term in q_value_l:
            tf = q_value_l.count(term)
            oktf = tf/(tf + 0.5 + 1.5*len(q_value_l)/avgQLen)
            query_oktf_d[term] = oktf
        queries_oktf_dict[q_key] = query_oktf_d



def get_ctf_df(term):

    print("Askingfor term ",term," in db ",db_no)
    if term in termsDict:
        termListc = termsDict[term]
    else:
        termListc = searchIndexes.getTermStats(str(term),db_no)
        termsDict[term] = termListc
    print("got result : ", termListc[2:])
    termListx = termListc[2:]
    ctf = termListc[0]
    df = termListc[1]   
    g = 0
    termListd = []
    
    for a in termListx:
        if(g%3 == 0):
            #print("a is ",(termListx[g],termListx[g+1],termListx[g+2]))
            c = str(termListx[g])
            c = int(c[2:len(c)-1])
            d = str(termListx[g+1])
            d = int(d[2:len(d)])
            e = str(termListx[g+2])
            e = int(e[2:len(e)-1])
            #print("c,d,e",(c,d,e))
            termListd.append((c,d,e))
            #xxx[0]
        g+=1
        
    #print("term-- :",term," ctf : ",ctf+1," df :",df+1)
    #print("converted result : ", termListd)
    global term_ctf_df_d
    term_ctf_df_d[term] = {'ctf':ctf,'df':df}
    #print ("ctf= %(ctf)f df= %(df)f" % {'ctf': ctf, 'df':df})
    #print(type(inverted_list))
    all_docs_len = 0

    for (docid,doclen,tf) in termListd:
        all_docs_len = all_docs_len + int(doclen)
        #print (docid," ",doclen)
        
    if df == 0:
        df =1

    global db_info
   
    #print(db_info)
    #print(db_no)
    avg_doc_len = db_info[db_no]["ave_doc_len"]
    #avg_doc_len = all_docs_len/df
    global doc_d 
    global doc_len

    for (docid,doclen,tf) in termListd:
        #print("len********** ",doclen)
        tf = float(tf)
        doclen = float(doclen)
        avg_doc_len = float(avg_doc_len)
        oktf = tf/(tf + 0.5+1.5*doclen/avg_doc_len)
        x={}
        x[term] = [tf,oktf,doclen]
        if docid in doc_d:
            x.update( doc_d[docid])

        doc_d[docid] = x
        doc_len[docid] =doclen    
        


def getQRes(qID,QLst):
    for term in QLst:
        get_ctf_df(term)


def processDocs(q_key,QLst,term_oktf_l):
    global doc_d,doc_len
    #print("All docs :" , doc_d)   

    for doc,doc_val_d in doc_d.items():
        vector = 0
        vector2 = 0
        d1 = 0
        d2 = 0
        tf = 0
        doclen = 0
        Pd_mle = None
        Pt_Md = None
        Pt_Mc = None
        Pt_d = None
        lamb = 0.2
        JM = 0
        bmx = 0
        sbmx= 0
        flag = 0
        mx1 =0
        #print("Q;ts" ,QLst)   
        for term in QLst:
             qt = 0
             at = 0
             tf = 0
                
             if term in term_oktf_l:
                 qt = term_oktf_l[term]
             if term in doc_val_d:
                 at = doc_val_d[term][1]
                 tf = doc_val_d[term][0]
                        
             doclen =doc_len[doc]

             #print(term)
             vector = vector + (qt * at)
             zt = term_ctf_df_d[term]['df']
             if (zt > 0):
                 vector2 = vector2 +(qt * at*(math.log(db_info[db_no]['num_docs']/zt)))
                
         
             if Pd_mle is None :
                 Pd_mle = ((tf+1)/(doclen + (db_info[db_no]['num_unique_terms'])))
             else:
                 Pd_mle = Pd_mle * ((tf+1)/(doclen + db_info[db_no]['num_unique_terms']))
                
             if tf != 0:
                 flag = 1;

             if Pt_Md is None:
                 Pt_Md = lamb*((tf)/doclen)
             else:
                 Pt_Md = lamb* ((tf)/doclen)

             if Pt_Mc is None:
                 Pt_Mc = (1-lamb)*(term_ctf_df_d[term]['ctf']/db_info[db_no]['num_terms'])
             else:
                 Pt_Mc = (1-lamb)*(term_ctf_df_d[term]['ctf']/db_info[db_no]['num_terms'])

             if Pt_Mc is None:
                 Pt_Mc = 0
                    
             #print("Pt  ",Pt_Md,Pt_Mc)
             zt2 = Pt_Md + Pt_Mc
             if(zt2 > 0):
                 JM = JM + math.log(zt2)

             x = ((1) / (1)) / ((term_ctf_df_d[term]['ctf'] + 0.5) /(db_info[db_no]['num_docs']-term_ctf_df_d[term]['ctf'] + 0.5))
                
             if x < 0:
                 x =1
             k1 = 2
             k2 = 10
             b = 1.5 
             K = (k1*((1-b)+ (b*(doclen/db_info[db_no]['ave_doc_len']))))
                
             if (K!=0):
                 y = ((k1+1)*(tf+1)) / (K+tf+1)
             z = ((k2+1)*qt) / (k2+qt)
                #print ("x : ",x," y :",y," z ",z)
             t = x*y*z
                #print(t)
              
             bmx = bmx + math.log(t)
            
             sbmx = sbmx + (tf/(tf + 0.5 + 1.5*(doclen/db_info[db_no]['ave_doc_len'])))
               
             mx1 = mx1 + tf
                
                #print("Pd_mle :" , Pd_mle, "Pt_Md : ",Pt_Md,"Pt_Mc : ",Pt_Mc)
                #print("Term : ",term," Doc_id : ",doc,"ctf :  ",term_ctf_df_d[term]['ctf'])
               
        #print("Doc : ",doc, " Vector ",vector)
        #print("vaecor space ",vector_space)
        vector_space[doc] = vector
        #print("vaecor space ",vector_space)
        vector_space2[doc] = vector2
        laplace_d[doc] = Pd_mle
        JM_d[doc] = JM
        BM25_d[doc] = bmx
        SBM25_d[doc] = sbmx
            
        mx1_d[doc] = mx1
    
    vector_space_sorted = sorted(vector_space.items(), key = itemgetter(1), reverse=True)
        #print(doc_d)
    global vs1_dict
    #print("XXXXXXXXX vector space : ",vector_space)
    v1d = copy.deepcopy(vector_space)
    
    vs1_dict[q_key] = v1d
    #print("Dict_______________________ ",vs1_dict,"---------------------")
    vector_space.clear()    
   # print("vs1 dict000000000000000000000000000 ",vs1_dict)
    vector_space_sorted2 = sorted(vector_space2.items(), key = itemgetter(1), reverse=True)
        #print(doc_d)
    global vs2_dict
    vs2_dict[q_key] = copy.deepcopy(vector_space2)
    vector_space2.clear()
        
    laplace_sorted_d = sorted(laplace_d.items(), key = itemgetter(1), reverse=True)
        #print(doc_d)
    global lm_d
    lm_d[q_key] = copy.deepcopy(laplace_d)
    laplace_d.clear()
                                 
    JM_sorted_d = sorted(JM_d.items(), key = itemgetter(1), reverse=True)
        #print(doc_d)
    global Jelin_d
    Jelin_d[q_key] = copy.deepcopy(JM_d)
    JM_d.clear()
        
    BM25_sorted_d = sorted(BM25_d.items(), key = itemgetter(1), reverse=True)
        #print(doc_d)
    global BM_d
    BM_d[q_key] = copy.deepcopy(BM25_d)
    BM25_d.clear()
    
    SBM25_sorted_d = sorted(SBM25_d.items(), key = itemgetter(1), reverse=True)
        #print(doc_d)
    global SBM_d
    SBM_d[q_key] = copy.deepcopy(SBM25_d)
    SBM25_d.clear()    

    mx1_sorted_d = sorted(mx1_d.items(), key = itemgetter(1), reverse=True)
        #print(doc_d)
    global myx1_d
    myx1_d[q_key] = copy.deepcopy(mx1_d)
    mx1_d.clear()
                                 
    

                                 
    doc_d.clear()
    #print(" doc d ",doc_d)


    global docs_map
    


def writetoFile(filename,d):
    FILE = open(filename,"w")
    for query_num,result in d.items():
        i = 1
        #print("For query no : ",query_num)
        for rs in result:
            FILE.write(str(query_num)+" Q0 "+helperFunctions.makeFixedLengthStr(rs[0],4)+" "+str(i)+" "+str(rs[1])
                       +" Exp\n")
            i+=1
            
    FILE.close()



def printResults(d):
    global totalResults
    for query_num,result in d.items():
        i = 1
        for rs in result:
            if(i <= totalResults):
                print(str(i)+" Document No :"+ str(rs[0])+"\n    Rank : "+str(rs[1])+"\n   Cache : "+str(searchIndexes.getDocContents(rs[0],0))+"\n\n")                      
            i+=1
            



def getResults():
    global queries_oktf_dict,queryDict
    global collDict,vs1_dict
    #print("queryDict",queryDict)
    #print("vs1 qqqqdict",vs1_dict)
    for key,value in queryDict.items():
        print("For query ",key," : ",value)
        getQRes(key,value)
        #print("vs1 dict",vs1_dict)
        term_oktf_l = queries_oktf_dict[key]
        #print("vs1 dict",vs1_dict)
        processDocs(key,value,term_oktf_l)
        #print("vs1 dict",vs1_dict)
   # writetoFile("1zzz.txt",vs1_dict)

    collDict[db_no] = [vs1_dict,vs2_dict,lm_d,Jelin_d,BM_d,SBM_d,myx1_d]
    



def merge7(d1,d2):
    d3 = {}
    for docID,score in d1.items():
        if docID in d2:
            d3[docID] = score+d2[docID]
        else :
            d3[docID] = score


    for docID,score in d2.items():
        if docID not in d3:
            d3[docID] = score
    return d3


def merge9(dict1, dict2):
    dict3 = {}
    #print("dict2 ",dict2)
    for q_num,ig in dict2.items():
        dict3[q_num] = merge7(dict1[q_num],dict2[q_num])
    #print("dict 3",dict3)
    return dict3
                             
def sort(dict1):
    dict2 = {}
    for qID, val in dict1.items():
        val1 = sorted(val.items(), key = itemgetter(1), reverse=True)
        dict2[qID] = val1

    return dict2


def mergeAll(listP):
    dictR = {}
    for d in listP:
        d=helperFunctions.normalizeDictEle(d)
        if(len(dictR)==0):
            dictR = d
        else:
            dictR = merge9(dictR,d)

    return dictR

def mergeResults():

    global collDict
    vs1 = {}
    vs2  = {}
    m3 = {}
    m4 = {}
    m5 = {}
    m6 = {}
    m7 = {}
    m8 = {}
#vs2 = lm_d,Jelin_d,BM_d,SBM_d,myx1_d
    #print("length of coll : ",collDict)
    for db,resultList in collDict.items():
        #print("vs 1 ",collDict[db][0])
        if(len(vs1) ==0):
            vs1 = collDict[db][0]
        else:
            vs1 = merge9(vs1,collDict[db][0])

        if(len(vs2) ==0):
            vs2 = collDict[db][1]
        else:
            vs2 = merge9(vs2,collDict[db][1])

        if(len(m3) ==0):
            m3 = collDict[db][2]
        else:
            m3 = merge9(m3,collDict[db][2])

        if(len(m4) ==0):
            m4 = collDict[db][3]
        else:
            m4 = merge9(m4,collDict[db][3])


        if(len(m5) ==0):
            m5 = collDict[db][4]
        else:
            m5 = merge9(m5,collDict[db][4])

        if(len(m6) ==0):
            m6 = collDict[db][5]
        else:
            m6 = merge9(m6,collDict[db][5])

        if(len(m7) ==0):
            m7 = collDict[db][6]
        else:
            m7 = merge9(m7,collDict[db][6])



    #print("vs1:",vs1)
    vs1 = sort(vs1)
    vs2 = sort(vs2)
    m3 = sort(m3)
    m4 = sort(m4)
    m5 = sort(m5)
    m6 = sort(m6)
    m7 = sort(m7)
    m8 = mergeAll([vs1,vs2,m3,m4,m6])
    m8 = sort(m8)
              
    #vs1_sorted = sorted(vs1.items(), key = itemgetter(1), reverse=True)
                  
    if(user == "test"):              
        writetoFile("./results/vs1z.txt",vs1)
        writetoFile("./results/vs2x.txt",vs2)
        writetoFile("./results/lmx.txt",m3)
        writetoFile("./results/elinx.txt",m4)                              
        writetoFile("./results/BMx.txt",m5)
        writetoFile("./results/SBMx.txt",m6)
        writetoFile("./results/myXx.txt",m7)              
        writetoFile("./results/meta.txt",m8)              
    else:
        print("For Vector space 1  ")
        printResults(vs1)
        print("For Vector space 2 ")
        printResults(vs2)
        print("For LM  ")
        printResults(m3)
        print("For Jelinik Mercer  ")
        printResults(m4)
        print("For BM25  ")
        printResults(m5)
        print("For SBM 25  ")
        printResults(m6)
        print("For My Experiment  ")
        printResults(m7)
        print("For Meta search ")
        printResults(m8)


def startTest():
    global db_no,queryDict,collDict,lTotalDB
    for db in lTotalDB:
        db = int(db)
        #reset()
        db_no=db
        helperFunctions.populateStopWords()
        readQueries()
        #print("qd",queryDict)
        setAvgQLen()
        get_oktf_queries()
        getResults()
        
    #print("length of coll : ",len(collDict))
    mergeResults()

def startUserSearch(query):
    global db_no,queryDict,collDict
    for db in lTotalDB:
        db  = int(db)
        #reset()
        db_no=db
        helperFunctions.populateStopWords()
        setUserQueryDict(query)
        #print("qd",queryDict)
        setAvgQLen()
        get_oktf_queries()
        getResults()
        
    #print("length of coll : ",len(collDict))
    mergeResults()



def usage():
    print("Usage :")
    print("python3 search.py [\"test\"] num num1 num2 num3... ")
    print("    For test mode ")
    print("    num is total results to display, test ignores this")
    print("    Then all the databases we want to query")

    print("python3 search.py [\"user\"] num \"Query\" num1 num2 num3... ")
    print("    For user mode ")
    print("    num is total results to display, test ignores this")
    print("    The query to search.")
    print("    Then all the databases we want to query")


    print("python3 search.py listdb ")
    print("   This will list all the collections with their details")


def main():
    global totalResults,lTotalDB,user
    readCollections()
    if(len(sys.argv) ==1):
        usage()
    elif(sys.argv[1]=="listdb"):
            print(db_info)

    elif(sys.argv[1]=="test"):
        user = sys.argv[1]
        totalResults = int(sys.argv[2])
        lTotalDB = sys.argv[3:]
        for db in lTotalDB:
            if int(db) not in db_info:
                print("Database :",db," not found, exiting.")
                sys.exit()
        startTest()

    elif(sys.argv[1]=="user"):
        user = sys.argv[1]
        totalResults = int(sys.argv[2])
        query = sys.argv[3]
        lTotalDB = sys.argv[4:]
        for db in lTotalDB:
            if int(db) not in db_info:
                print("Database :",db," not found, exiting.")
                sys.exit()
        startUserSearch(query)
    else:
        usage()

    
main()
