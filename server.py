#Server
import socket
from crawler import main

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50017              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

termIndex= {} #termID: startByte,stopByte

def loadIndexMapFiles():
    termsMapFile = "termsMap.txt"
     with open(termsMapFile,encoding='utf-8') as stopwords_file:
        for line in stopwords_file:
            line = line.replace("\n","")
            lWords = line.split()
            termIndex[lWords[0]] = [lWords[1],lWords[2]] 
    


loadIndexMapFiles()

while True:
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)

    print ("true")
    data = conn.recv(1024)
    print("waiting")
    if not data: break
    conn.sendall(data)

    sData = data.decode("utf-8")
    print("Received : "+sData)
    lCmd = sData.split()
    if(lCmd[0] == "crawl"):
        main(lCmd[1])

conn.close()


