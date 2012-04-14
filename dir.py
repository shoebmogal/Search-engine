import os
import sys
rootdir = sys.argv[1]

y=[]
def bst(list1):
    if (list1 != []):
        middle = (len(list1)-1)/2
        middle=int(round(middle, 0))
        print("m:  ---------------------------->"+list1[middle])
        print("middle: "+str(middle))
        y.append(list1[middle])
        print("istart: "+str(0)+" iENd :"+str(middle)+" lenList : "+str(len(list1)))
        bst(list1[:middle])
        print("istart: "+str(middle+1)+" iENd :"+str(len(list1))+" lenList : "+str(len(list1)))
        bst(list1[middle+1:])
    #print("l:" +str(len(list1)))
    #print("list:" +str(list1))
    #if(middle-1 >= 0):
        #print("list-1:" +str(list1[:middle-1]))
    #    return [list1[middle],bst(list1[:middle]),  bst(list1[middle:])]
      
    #else:
     #   return []
    

    #if(middle+1 <= len(list1)):
      #  print("list+1:" +str(list1[middle:]))
    else:
        print("m:  ----------------------------> []"+str(list1))
        y.append(" ")
    


def bst1(iStart,iEnd,list1):

    lenList = int((iEnd-iStart))
    print("istart: "+str(iStart)+" iENd :"+str(iEnd)+" lenList : "+str(lenList))
    if (lenList != 0):
        middle = (lenList-1)/2
        middle=int(round(middle, 0))
        middle = middle+iStart
        print(" middle : "+str(middle))
        print("element ----------------------------> "+str(list1[middle]))
        #print("element++ ----------------------------> "+str(list1[middle+1]))
        y.append(list1[middle])
        bst1(iStart,middle,list1)
        bst1(middle+1,iEnd,list1)
  
    else:
        print("element ----------------------------> []")
        y.append(" ")
    


def search(query,index,noOfNodes):
    if(y[index] != []):
         if(y[index] == query):
             return index
         elif (query < y[index]):
             return search(query,index+1,(1+noOfNodes)//2)
         elif (query > y[index]):
             return search(query,index+((1+noOfNodes)//2)+1,(1+noOfNodes)//2)

             
    else:
        return -1

x = [] 

for root, subFolders, files in os.walk(rootdir):
    files.sort()
    x = files
    files = ['a','b','c','d','e','f','g','h','i']
    #print(files)
    #print("Rec----------------------------------------------------")
    bst(files)
    #print("Proc----------------------------------------------------")
    #bst1(0,len(files),files)


print(y)

print(y[search("g",0,len(files))])


