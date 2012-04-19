import constants
import sys
import os
import indexesInit
import indexer



def main(fileToIndex):
    constants.filetoIndex = fileToIndex
    indexesInit.main()
    #crawler.main(constants.filetoIndex)
    indexer.main()
    indexesInit.cleanup()

main(sys.argv[1])    
