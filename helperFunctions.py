import constants

#To get  stop words from the file
def populateStopWords():
    with open('stoplist.txt',encoding='utf-8') as stopwords_file:
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

