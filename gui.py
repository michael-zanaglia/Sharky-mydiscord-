import cv2,numpy,random
from pygame import *
from PIL import *
from PIL import Image

LIST_MAJ=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
LIST_MIN=['a','à','â','ä','b','c','ç','d','e','é','è','ë','ê','f','g','h','i','ï','î','j','k','l','m','n','o','œ','ô','ö','p','q','r','s','t','u','ü','û','ù','v','w','x','y','z']
LIST_DIG=['0','1','2','3','4','5','6','7','8','9']
LIST_SPE=['!','?','.',',','/',':',';',"'",'"','-','_','(',')','☺','>','<','@','=','*','&','%','\\','’','シ','🐟','^','°']
LIST_SPE_INDEX=['!','inter','p',',','slash','dp',';',"'","db'",'-','_','(',')','☺','cr','cl','@','=','*','&','%','dash',"'",'シ','🐟','^','°']
LIST_BAS=['p','q','g',',','y','.','ç']
LIST_BAS_INDEX=[1,1,1,1,1,1,2]
list_char=[LIST_MAJ,LIST_MIN,LIST_DIG,LIST_SPE]

def CHECK_EMOJI(message):
    message=str(message).replace(':sourire:','☺')
    # message=str(message).replace(':requin:','🦈')
    message=str(message).replace(':lenny:','シ')
    message=str(message).replace(':poisson:','🐟')
    return message

def CALC_WORD(message):
    LIST_MOTS=[]
    MOT=''
    a=0
    for e in message:
        a+=1
        if e !=' ':
            MOT+=e
        else:
            LIST_MOTS.append(MOT)
            MOT=''
        if a==len(message):
            LIST_MOTS.append(MOT)
            MOT=''
    return LIST_MOTS

def CHECK_RETURNS(message):
    res=0
    for e in message:
        if e == '█':
            res+=1
    return res

def CHECK_LENGHT(cur_len,mot):

    CHECK_LEN=0.5
    for e in mot:
        if e in LIST_DIG:
            TYP='DIG'
        elif e in LIST_MIN:
            TYP='MIN'
        elif e in LIST_MAJ:
            TYP='MAJ'
        elif e in LIST_SPE:
            TYP='SPE'
            LET=True
            b=0
            for o in LIST_SPE:
                if o == e:
                    break
                b+=1
            e=LIST_SPE_INDEX[b]
        else:
            TYP='SPE'
            e='NONE'
        PATH='GRAPHICS/FONTS/'+TYP+'/'+e+'.png'
        LET_IMG=Image.open(PATH)
        LET_IMG = numpy.array(LET_IMG)
        h,w,c=LET_IMG.shape
        CHECK_LEN+=float(w/6)

    if cur_len+CHECK_LEN>=34.0:
        return True
    else:
        return False
    
def CALC_SIZE(message):
    LINE_LEN=0.0
    COL=1
    for i in range(len(message)):
        if message[i]==' ' or  i==0:
            a=1
            if i == 0:
                a=0
            CUR_WORD=''
            if i+1 == len(message):
                pass
            else:
                while message[i+a]!=' ':
                    CUR_WORD+=message[i+a]
                    a+=1
                    if i+a == len(message):
                        break

        if LINE_LEN>34.0 or message[i]=='█':
            LINE_LEN=0.0
            COL+=1

        letter=message[i]
        if message[i] in LIST_DIG:
            TYP='DIG'
            LET=True
        elif message[i] in LIST_MIN:
            TYP='MIN'
            LET=True
        elif message[i] in LIST_MAJ:
            TYP='MAJ'
            LET=True
        elif message[i] in LIST_SPE:
            TYP='SPE'
            LET=True
            b=0
            for e in LIST_SPE:
                if e == message[i]:
                    break
                b+=1
            letter=LIST_SPE_INDEX[b]
        elif message[i] == ' ':
            if not CHECK_LENGHT(LINE_LEN,CUR_WORD):
                LINE_LEN+=0.5
                TYP=''
                LET=False
        else:
            letter='NONE'
            TYP='SPE'
            LET=True
        b=0
        if LET and message[i]!='█':
            try:
                PATH='GRAPHICS/FONTS/'+TYP+'/'+letter+'.png'
                LET_IMG=Image.open(PATH)
                LET_IMG = numpy.array(LET_IMG)
                h,w,c=LET_IMG.shape
                LINE_LEN+=float(w/6)
            except:
                if letter!=' ':
                    PATH='GRAPHICS/FONTS/NONE.png'
                    LET_IMG=cv2.imread(PATH)
                    h,w,c=LET_IMG.shape
                    LINE_LEN+=float(w/6)

        if message[i] == ' ' and CHECK_LENGHT(LINE_LEN,CUR_WORD):
            LINE_LEN=0.0
            COL+=1
    return COL

def MSG_FORM(message,sender,hour,style,response):

    hr,min,begin='','',False
    for k in hour:
        if k==':':
            break
        else:
            hr+=k
    for k in hour:
        if begin:
            min+=k
        if k==':':
            begin=True
    if int(hr)<10:
        hr='0'+hr
    if int(min)<10:
        min= min
    message=CHECK_EMOJI(message)
    H_SIZE=CALC_SIZE(message)
    BUB_TOP=Image.open(f'GRAPHICS/DEF_BUB/{style}/BAR_TOP.png')
    BUB_MID=Image.open(f'GRAPHICS/DEF_BUB/{style}/BAR_MID.png')
    BUB_SPA=Image.open(f'GRAPHICS/DEF_BUB/{style}/BAR_SPA.png')
    BUB_BOT=Image.open(f'GRAPHICS/DEF_BUB/{style}/BAR_BOT.png')
    BUB=Image.new('RGBA',(234,14+(H_SIZE*12)+((H_SIZE-1)*4)))
    BUB.paste(BUB_TOP,(0,0))
    BUB.paste(BUB_MID,(0,7))
    for i in range(H_SIZE):
        if i+1 != H_SIZE:
            BUB.paste(BUB_SPA,(0,19+16*i))
            BUB.paste(BUB_MID,(0,23+16*i))
    BUB.paste(BUB_BOT,(0,3+H_SIZE*16))

    stop=False

    if response!="None":
        num=5
    else:
        num=3
    for j in range(num):
        breakable=True
        if j == 0:
            val=message
            x=13
            row=7
            LINE_LEN=0.0
        elif j == 1:
            val=sender
            x=4
            row=4
            LINE_LEN=0.0
            BUB=BUB.crop((0,-20,234,14+(H_SIZE*12)+((H_SIZE-1)*4)))
        elif j == 2:
            val=f"{hr}:{min}"
            x=200
            row=4
            LINE_LEN=-0.0
        elif j == 3:
            breakable=False
            BUB=BUB.crop((0,0,234,14+(H_SIZE*12)+((H_SIZE-1)*4)+50))
            res=response[0]
            x=4
            row=(H_SIZE*12)+((H_SIZE-1)*4)+36
            LINE_LEN=0.0
            res=f'Réponse à {response[1]} :'
            val=res
        elif j==4:
            rep_text=''

            breakable=False
            m20=False
            res=response[0]
            x=12
            row=(H_SIZE*12)+((H_SIZE-1)*4)+50
            LINE_LEN=0.0
            res=f'"{res}"'
            val=res
        for i in range(len(val)):
            if val[i]==' ' or  i==0:
                a=1
                if i == 0:
                    a=0
                CUR_WORD=''
                if i+1 == len(val):
                    pass
                else:
                    while val[i+a]!=' ':
                        CUR_WORD+=val[i+a]
                        a+=1
                        if i+a == len(val):
                            break

            if LINE_LEN>34.0 or val[i]=='█':
                if not breakable:
                    x+=3
                else:
                    row+=16
                    x=13
                    LINE_LEN=0.0

            if j==4:
                rep_text+=val[i]
                if LINE_LEN > 30:
                    val=rep_text+'.."'
                    stop = True
                    stop_count=1

            letter=val[i]
            if val[i] in LIST_DIG:
                TYP='DIG'
                LET=True
            elif val[i] in LIST_MIN:
                TYP='MIN'
                LET=True
            elif val[i] in LIST_MAJ:
                TYP='MAJ'
                LET=True
            elif val[i] in LIST_SPE:
                TYP='SPE'
                LET=True
                b=0
                for e in LIST_SPE:
                    if e == val[i]:
                        break
                    b+=1
                letter=LIST_SPE_INDEX[b]
            elif val[i] == ' ':
                if not CHECK_LENGHT(LINE_LEN,CUR_WORD):
                    LINE_LEN+=0.5
                    x+=3
                    TYP=''
                    LET=False
            else:
                letter='NONE'
                TYP='SPE'
                LET=True
            b=0
            if val[i] in LIST_BAS:
                for j in LIST_BAS:
                    if j==val[i]:
                        break
                    b+=1
                y=row+LIST_BAS_INDEX[b]
            else:
                y=row
            if i!=len(val)-1:
                if letter == '_':
                    if val[i+1]=='_':
                        letter='_'
                    else:
                        letter='__'
            if LET and val[i]!='█':
                try:
                    PATH='GRAPHICS/FONTS/'+TYP+'/'+letter+'.png'
                    LET_IMG=Image.open(PATH)
                    LET_IMG = numpy.array(LET_IMG)
                    h,w,c=LET_IMG.shape
                    LINE_LEN+=float(w/6)
                    BUB.paste(Image.open(PATH),(x,y),Image.open(PATH))
                    x+=w
                except:
                    if letter!=' ':
                        PATH='GRAPHICS/FONTS/NONE.png'
                        LET_IMG=cv2.imread(PATH)
                        h,w,c=LET_IMG.shape
                        LINE_LEN+=float(w/6)
                        BUB.paste(Image.open(PATH),(x,y),Image.open(PATH))
                        x+=w

            if val[i] == ' ' and CHECK_LENGHT(LINE_LEN,CUR_WORD):
                if not breakable:
                    x+=3
                else:
                    row+=16
                    x=13
                    LINE_LEN=0.0
            
            if stop:
                stop_count+=1
                if stop_count==5:
                    break
    return BUB

