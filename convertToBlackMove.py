from os import listdir
from os.path import isfile, join
import codecs
import re

def openText(filename):
    try:
        text = " ".join([ line for line in codecs.open(filename,"r","utf-8")])
    except :
        return False
    return text

#===============================================================================
# #Lines to be changed - START
#===============================================================================

path="D:\\\go\\sgf\\problems\\"# CHANGE THIS LINE  your main directory
listOfDirectories=["dir1","dir2","dir3"]# CHANGE THIS LINE your subdirectories

#===============================================================================
# #Lines to be changed - END
#===============================================================================
for d in listOfDirectories:
    path2=path+d
    onlyfiles = [ f for f in listdir(path2) if isfile(join(path2,f)) ]
    print(path2)
    print(onlyfiles)
    for f in onlyfiles:
        if(f.find(".sgf")!=-1):
            filepath=path2+"/"+f
            sgfstring=openText(filepath)
            if(sgfstring!=False):
                indexB=sgfstring.find(";B[")
                indexW=sgfstring.find(";W[")
                if (((indexB)>(indexW))|((indexB==-1)&(indexW!=-1))):
                    print(filepath)
                    sgfstring=sgfstring.replace("B[","xxx[")
                    sgfstring=sgfstring.replace("W[","B[")
                    sgfstring=sgfstring.replace("xxx[","W[")

                    insensitive_white1 = re.compile(re.escape('white'), re.IGNORECASE) # replace the comments and ignore case
                    sgfstring=insensitive_white1.sub('temptemp', sgfstring)

                    insensitive_black = re.compile(re.escape('black'), re.IGNORECASE)
                    sgfstring=insensitive_black.sub('White', sgfstring)

                    insensitive_white2 = re.compile(re.escape('temptemp'), re.IGNORECASE)
                    sgfstring=insensitive_white2.sub('Black', sgfstring)
                    try:
                        open(filepath,"r+").write(sgfstring)
                    except:
                        print("fail to write "+filepath)