import mmap
import contextlib

with open('./indexes/termsMapy.txt', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        n=3
        n=n-1
        #print ('First 10 bytes via read :', m.read(10))
        print ('First 20 101 bytes via slice:', m[n*35:(n*35+35)])
        #print ('2nd   10 bytes via read :', m.read(10))



with open("hello.txt", "wb") as f:
    f.write(b"Hello Python!\n")

with open("t", "r+b") as f:
    # memory-map the file, size 0 means whole file
    map = mmap.mmap(f.fileno(), 0)
    # read content via standard file methods
    print(map.readline())  # prints b"Hello Python!\n"
    # read content via slice notation
    #print(map[:5])  # prints b"Hello"
    # update content using slice notation;
    # note that new content must have same size
    #map[6:] = b" world!\n"
    # ... and read again using standard file methods
    #map.resize(1000000000)
    #map.seek  (1000000)
    #map.write(b"abc")o
    #print(map.readline())  # prints b"Hello  world!\n"

    # close the map
    map.close()
