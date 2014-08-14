import re
import chardet
import codecs

tenuki="tt"

Filedirectory="./"
basicDicNormal={'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':0,'k':1,'l':2,'m':3,'n':4}
basicDicReverted={'s':1,'r':2,'q':3,'p':4,'o':5,'n':6,'m':7,'l':8,'k':9,'j':0,'i':1,'h':2,'g':3,'f':4}

dicComment={}

def convert(filename,mode):
'''
Does not work with variations (at least untested)
'''
    filename2=Filedirectory+filename
    text=openText(filename2)
    tab=findMoves(text)
    corner=findCorner(tab)
    if(mode=="joseki"):
        dic=buildReplacementdic(corner)
        conventionRespected=findIfConventionRespected(tab,dic)
        text=parseTab(tab,dic,conventionRespected)
        print(text)
    open(Filedirectory+"JosekiBase.csv","a+b").write("\r\n"+filename+text)

def findIfConventionRespected(tab,dic,firstPlayer=0):
'''
Regroup symmetric josekis with the same numbers association
'''
    for occurence in tab:
        if occurence[firstPlayer]!="":
            value=findInDic(dic,occurence[firstPlayer])
            if(value!="tenuki"):
                chiffre1=value[0]
                chiffre2=value[1]
                if(chiffre1!=chiffre2):
                    if(int(chiffre1)>int(chiffre2)):
                        return True
                    else:
                        return False
        firstPlayer=1-firstPlayer


def findCorner(tab):
    for occurence in tab:
        if (occurence[0]!=""):
            move=occurence[0]
            letter1=move[0]
            letter2=move[1]
            if(letter1 in basicDicNormal.keys()):
                cornerletter1="a"
            else:
                cornerletter1="s"
            if(letter2 in basicDicNormal.keys()):
                cornerletter2="a"
            else:
                cornerletter2="s"
            return(cornerletter1+cornerletter2)


def buildReplacementdic(corner):
    firstLetterDic=basicDicNormal
    secondLetterDic=basicDicNormal
    newdic={}
    newdic["tt"]="tenuki"
    if(corner[0]=="s"):
        firstLetterDic=basicDicReverted
    if(corner[1]=="s"):
        secondLetterDic=basicDicReverted
    for letter1,value1 in firstLetterDic.iteritems():
        for letter2,value2 in secondLetterDic.iteritems():
            newkey=letter1+letter2
            value=str(value1)+str(value2)
            newdic[newkey]=value
    return newdic



def openText(filename):
    text = " ".join([ line for line in codecs.open(filename,"r","utf-8")])
    return text

def findMoves(text):
    p = re.compile('(?:B\[(.*?)\])'+ # Black moves
                   '|'+
                   '(?:W\[(.*?)\])'+ # White Moves
                   '|'
                   '(?:C\[(.*?)\])' # Commentaries
                   )
    tab=p.findall(text)
    return tab

def parseTab(tab,dic,convention,allowComments=False,firstPlayer=0):
    text=""
    for occurence in tab:
        if occurence[firstPlayer]=="":
            if occurence[2]=="":
                raise Exception("error in sgf file")
            else :
                if(allowComments):
                    text+=";"+occurence[2] 
        else:
            text+=";"+findInDic(dic,occurence[firstPlayer],convention)
            firstPlayer=1-firstPlayer
    return(text)


def findInDic(dic,key,convention=True):
    if key in dic.keys():
        if(not convention):
            return(dic[key][1]+dic[key][0])
        return dic[key]
    else:
        return key

filename=raw_input("give the name of the sgf file in this directory you want to map : ")
convert(filename,mode="joseki")
