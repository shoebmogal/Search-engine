import os
import sys
import mmap
import contextlib

# Now I will have to take the termMapy and convert it into a binary tree file
with open('./indexes/termsMapy.txt', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        n=3
        n=n-1
   #     print ('size :', m.size()/35)
  #      print ('First 20 101 bytes via slice:', m[n*35:(n*35+35)])
        
        with open("./indexes/termMapFileSorted1.txt", "wb") as f2:
            def bst(iStart,iEnd,m):
  #              print("istart: "+str(iStart)+" iENd :"+str(iEnd))
                lenList = int(iEnd-iStart)
                if(lenList != 0):
                    middle = (lenList-1)/2
                    middle=int(round(middle, 0))
                    middle = middle+iStart
                    #print("middle: "+str(middle))
                    f2.write(m[middle*35:(middle*35+35)])
                    bst(iStart,middle,m)
                    bst(middle+1,iEnd,m)
                else:
                    f2.write(b"                                  \n")
#                    print("leafnode")
                    
            bst(0,int(m.size()/35),m)




with open('./indexes/termMapFileSorted1.txt', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m1:

        def search(query,index,noOfNodes,m1):
            sData = m1[index*35:(index*35+35)]
            sData = sData.decode("utf-8")

            #print(" Data : "+str(sData)+" At index : "+str(index)+" NoofNodes : "+str(noOfNodes))
            lData = sData.split()
            if(lData != []):
                middle = (noOfNodes+1)//2
                middle=int(round(middle, 0))
                
                if(lData[0] == query):
                    return lData[1:]
                elif (query < lData[0]):
                    print (query+ " < "+lData[0])
                    return search(query,index+1,middle,m1)
                elif (query > lData[0]):
                    print (query+ " > "+lData[0]+" so go to index : "+str(index+middle))
                    return search(query,index+middle,middle,m1)
                
                
                else:
                    return []


        print(" size : "+str(int(m1.size()/35)))
        lBytes = search(sys.argv[1],0,int(m1.size()/35),m1)
        print("lBytes : ",lBytes)

        termFile = "./indexes/termsx.txt"
        with open(termFile, "r+b") as f:
            # memory-map the file, size 0 means whole file
            map = mmap.mmap(f.fileno(), 0)
            print("Term stuff :  ",map[int(lBytes[0]):int(lBytes[1])])
