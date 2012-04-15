import constants
import sys
import os
import indexesInit
import crawler
import indexer

constants.filetoIndex = sys.argv[1]

def main():
    indexesInit.main()
    #crawler.main(constants.filetoIndex)
    indexer.main()
    indexesInit.cleanup()
main()    
