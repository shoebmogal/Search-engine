import constants
import sys
import os
import porter


#To get  stop words from the file
def populateStopWords():
    with open(constants.stopWordsFile,encoding=constants.encoding) as stopwords_file:
        for line in stopwords_file:
            constants.stopwords_l.append(line.replace("\n",""))

#To remove stop words from list
#input list
#return list
def remStopWords(query_l):
    words_l = []
    for word_s in query_l:
        if not word_s in constants.stopwords_l:
            words_l.append(word_s)
    return words_l

#Dict to string conversion
#input dict{String:String}
#return String
def getStr(dictP):
    sRet = ""
    for key, value in dictP.items():
        sRet = sRet +" "+ str(key)+ " "+str(value)
    return sRet

#Make a String of fixed length number by adding zeroes before it
#input number,number
#return String
def makeFixedLengthStr(length,n):
    sLen =  str(length)
    zeros=""
    while (n-len(sLen)) > 0:
        zeros=zeros+"0"
        n=n-1
        
    zeros = zeros+sLen
    return zeros

#Make a String of fixed length by adding spaces after it
#input number,number
#return String
def makeFixedLengthSpace(length,n):
    sLen =  str(length)
    zeros=""
    while (n-len(sLen)) > 0:
        zeros=zeros+" "
        n=n-1
        
    zeros = sLen+zeros
    return zeros



def normList(L, normalizeTo=1.0):
    '''normalize values of a list to make its max = normalizeTo'''

    vMax = max(L)
    return [ float(x)/(float(vMax)*1.0)*normalizeTo for x in L]


def normalizeTElement(listT):
    list0 = []
    list1 = []
    listR = []
    dict0 = {}
    for t in listT:
        list0.append(t[0])
        list1.append(t[1])

    list1 = normList(list1)
    i=0
    for l in list0:
        listR.append((l,list1[i]))
        i+=1

    return listR


def normalizeDictEle(dictP):
    dictR = {}
    for k,v in dictP.items():
        dictR[k] = dict(normalizeTElement(v))

    return dictR

#print(normalizeTElement([(1,3),(2,5.0),(3,6.2),(4,6.7),(5,11),(6,33.78),(7,56.22)]))

'''
dictc = {}
dictc[1] = [(1,3),(2,5.0),(3,6.2),(4,6.7)]
dictc[2] = [(5,11),(6,33.78),(7,56.22)]

dictc = normalizeDictEle(dictc)
print(dictc)
'''
