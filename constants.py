IndexName = 0
#space
space = " "
newLine = "\n"
underscore = "_"

#Index stuff
rootDir = "."
allCollsDir = rootDir+"/allCollections"
indexDir = allCollsDir+"/indexes_"+str(IndexName)
termsDir = indexDir+"/terms"
filetoIndex = ""

#Index files
docFile = indexDir+"/d3.txt"
docCacheFile = indexDir+"/docCache.txt"
docCacheIndexFile = indexDir+"/docIndexCache.txt"
termsFile = indexDir+"/terms.txt"
termsListFile = indexDir+"/termsList.txt"
fSortedTermIndex = indexDir+"/termsMapy.txt"
termBTreeFile = indexDir+"/termBTree.txt"
collFile = indexDir+"/collInfo.txt"
SortedCacheIndex = indexDir+"/sortedDocsIndex.txt"
docCacheBTreeFile= indexDir+"/bTreeDocsIndex.txt"

#Terms and DocIDs size
docWordCntLen = 6
byteLen = 6
termSize = 20
docSize = docWordCntLen+len(space)+docWordCntLen+len(newLine)
termLineSize = termSize+len(space)+byteLen+len(space)+byteLen+len(newLine)
#cacm.all 
T ="T" #"title"
W = "W" #"contents"
B = "B" #"date"
A = "A" #"author"
N = "N" # "entryDate"
I = "I" # "docID"
X = "X" #ref

#stopwords list
stopWordsFile=rootDir+"/stoplist.txt"
stopwords_l = []


#encoding
encoding="utf-8"


#collection details
numDocs=0
numTerms = 0
numUniqueTerms = 0
allDocsLen = 0
