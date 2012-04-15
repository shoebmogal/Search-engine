Name = "Shoeb Ahmed Mogal"

#space
space = " "
newLine = "\n"
underscore = "_"

#Index stuff
rootDir = "."
indexDir = rootDir+"/indexes"
termsDir = indexDir+"/tmp"
filetoIndex = ""

#Index files
docFile = indexDir+"/d3.txt"
docWordsFile = indexDir+"/docWords.txt"
termsFile = indexDir+"/terms.txt"
termsListFile = indexDir+"/termsList.txt"
fSortedTermIndex = indexDir+"/termsMapy.txt"
termBTreeFile = indexDir+"/termBTree.txt"


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
stopwords_l = []


#encoding
encoding="utf-8"


