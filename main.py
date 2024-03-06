import pygame, subprocess, sys, mysql.connector, json
from PIL import Image
from io import BytesIO
import base64
import easygui, pathlib, cv2, numpy, gui
import time
import datetime
import traceback

class Py() :
    def __init__(self, l, L) :
        self.l = l
        self.L = L
        self.screen = pygame.display.set_mode((self.L, self.l))
        self.width_surface = 1400
        self.x = 0
        surface_for_connected  = pygame.Surface((658, 100))
        self.sfc = surface_for_connected
        self.sfc.set_clip((0,0,658,100))
        self.sfc_img  = pygame.Surface((self.width_surface,100))
        self.txt_chat = ""
        self.txt_chat2 = ""
        self.txt_chat3 = ""
        self.txt_chat = ""
        self.current = self.txt_chat
        self.style = "DEF"
        self.pseudo, self.mail = self.WritePseudo()
        self.scrollspace = pygame.Rect(253, 102, 647, 12)
        self.bar = pygame.Rect(self.scrollspace.x, self.scrollspace.y, 50, self.scrollspace.h)
        self.stop_bar = False
        self.msg_zone = pygame.Surface((648,686)) #252 114
        self.msg_zone.set_clip((0,0,648,686))
        self.shown_messages=pygame.Surface((648,100000))
        self.message_height=0
        self.screen.blit(self.msg_zone,(252,114))
        self.msgy=0
        self.txt_chat = ""
        self.pseudo, self.mail = self.WritePseudo()
        self.clock=pygame.time.Clock()
        self.tick_g=0
        self.last_load = ""
        self.shown_messages.fill('#4b0082')
        self.loaded_msgs=0
        self.font = pygame.font.Font('GRAPHICS/FONTS/pokemon-rs.ttf', 70)
        self.text = self.font.render('Chargement des messages', True, (255,255,255), (0,0,0))
        self.lm_txt = self.font.render((str(self.loaded_msgs)+'%'), True, (255,255,255), (0,0,0))
        self.screen.blit(self.text,(180,450))
        self.screen.blit(self.lm_txt,(180,520))
        pygame.display.update()
        
    def ShowMessages(self, msg):
        self.shown_messages.fill('#4b0082')
        a=0
        y=0
        m =  co.TakePseudoOfUsers(msg[1])
        self.message_height=0
        for x in msg:
            bubble_img=gui.MSG_FORM(str(msg[0]), self.pseudo if msg[1] == self.mail else m, msg[2], msg[3], msg[4])
            bubble=numpy.array(bubble_img)
            h,w,c=bubble.shape
            bubble_img=bubble_img.resize((w*2,h*2),Image.NEAREST)
            image_data = bubble_img.tobytes()
            bubble_surface = pygame.image.fromstring(image_data, (w*2,h*2), "RGBA")
            if p.pseudo==msg[1]:
                x=180
            else:
                x=0
            self.shown_messages.blit(bubble_surface,(x,y))
            if x!=msg[-1]:
                if msg[4]!="None":
                    offset=10
                else:
                    offset=0
            y+=h*2+offset
            self.message_height+=h*2+offset
            a+=1
        self.message_height+=10
    
    def LoadMessage(self,msg):
        new_load = msg[0][0]
        m = co.TakePseudoOfUsers(msg[0][2])
        if self.last_load != new_load :
            #print(new_load, self.last_load)
            y=self.message_height
            bubble_img=gui.MSG_FORM(str(msg[0][1]),self.pseudo if self.mail == msg[0][2] else m,msg[0][3],msg[0][4],msg[0][5])
            print(msg[0][2], m)
            bubble=numpy.array(bubble_img)
            h,w,c=bubble.shape
            bubble_img=bubble_img.resize((w*2,h*2),Image.NEAREST)
            image_data = bubble_img.tobytes()
            bubble_surface = pygame.image.fromstring(image_data, (w*2,h*2), "RGBA")
            if self.mail==msg[0][2]:
                x=180
            else:
                x=0
        
            self.shown_messages.blit(bubble_surface,(x,y))
            if msg[0][5]!="None":
                offset=10
            else:
                offset=0
            y+=h*2+offset
            pass
            self.message_height+=h*2+offset
            if -abs(self.message_height) == self.msgy-686-h*2:
                
                if self.message_height<686:

                    self.msgy=abs(self.message_height-686)
                else:
                    self.msgy=-abs(self.message_height-686)
        self.last_load = new_load
        #print("fin de la fonct,", self.last_load)

    def LoadMessageStart(self,msg):
        new_load = msg[0]
        m = co.TakePseudoOfUsers(msg[1])[0]
        if self.last_load != new_load :
            #print(new_load, self.last_load)
            y=self.message_height
            bubble_img=gui.MSG_FORM(str(msg[0]),m if self.mail == msg[1] else m,msg[2],msg[3],msg[4])
            bubble=numpy.array(bubble_img)
            h,w,c=bubble.shape
            bubble_img=bubble_img.resize((w*2,h*2),Image.NEAREST)
            image_data = bubble_img.tobytes()
            bubble_surface = pygame.image.fromstring(image_data, (w*2,h*2), "RGBA")
            if self.mail==msg[1]:
                x=180
            else:
                x=0
        
            self.shown_messages.blit(bubble_surface,(x,y))
            if msg[4]!="None":
                offset=10
            else:
                offset=0
            y+=h*2+offset
            pass
            self.message_height+=h*2+offset
        self.last_load = new_load
        #print("fin de la fonct,", self.last_load)
    
    def Text(self) :
        font = pygame.font.SysFont(None, 30)
        if len(self.pseudo) > 12 :
            font_p = pygame.font.SysFont(None, 25)
        else :
            font_p = font

        now=datetime.datetime.now()
        sec=now.strftime("%S")
        if int(pygame.time.get_ticks())%1000<=500:
            sep=':'
        else:
            sep=' '
        current_hour = now.strftime("%H"+sep)
        current_min = now.strftime("%M")


        pseudo_txt = font_p.render(self.pseudo, True, (250,250,250))
        hour_txt = font_p.render(current_hour, True, (250,250,250))
        min_txt = font_p.render(current_min, True, (250,250,250))
        voc_txt = font.render("# Channels Vocaux", True, (250,250,250))
        chat_txt = font.render("# Channels Textuels", True, (250,250,250))
        
        self.screen.blit(pseudo_txt, (150,75))
        self.screen.blit(hour_txt, (150,30))
        self.screen.blit(min_txt, (180,30))
        self.screen.blit(voc_txt, (25,115))
        self.screen.blit(chat_txt, (25,380))

    def RightClick(self,x,y):
        x-=252
        y-=114
        tup=(x,y,x+200,y+200)
        print(tup)
        pygame.draw.rect(self.screen,(35,35,35),tup)
    
    def ShowScreen(self) :
        pygame.display.set_caption("Sharky")
        screen_color = pygame.Color((75,0,130))
        self.screen.fill(screen_color)
    
    def ShowScroll(self) :
        pygame.draw.rect(self.screen, (250,250,250), self.scrollspace)
        pygame.draw.rect(self.screen, (60,60,60), self.bar)
            
    def MooveBar(self) :
        posx, _ = pygame.mouse.get_pos()
        
        self.bar.x = posx
        indice = 900 / p.width_surface 
        self.x = -abs(self.bar.left*indice)
        print(f"indice : {indice}")
        #print(self.bar.left, "&")
        #print(self.bar.right)
        
        if self.bar.right >= 900 :
            self.x = p.width_surface
            self.bar.right = self.scrollspace.right
        elif self.bar.x < self.scrollspace.left :
            self.x = 0
            self.bar.x = self.scrollspace.left
            
        self.ShowScroll()
        
        
    def DrawLine(self) :
        pygame.draw.line(self.screen, (255,255,255), (250,0), (250, 900), 2)
        pygame.draw.line(self.screen, (60,0,104), (253,100), (900, 100), 3)
        pygame.draw.line(self.screen, (255,255,255), (0,145), (250, 145), 2)
        pygame.draw.line(self.screen, (255,255,255), (0,410), (250, 410), 2)
        
        profil_case = pygame.Rect(0, 0, 249, 102)
        pygame.draw.rect(self.screen, (60,0,104), profil_case)
        self.surface_cercle = pygame.Surface((80,80), pygame.SRCALPHA)
        pygame.draw.circle(self.surface_cercle, (255,255,0), (40,40), 40, 2)
        self.mask = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(self.mask, (255, 255, 255), (40, 40), 38)
        
    
    def Text(self) :
        font = pygame.font.SysFont(None, 30)
        if len(self.pseudo) > 12 :
            font_p = pygame.font.SysFont(None, 25)
        else :
            font_p = font
        pseudo_txt = font_p.render(self.pseudo, True, (250,250,250))
        voc_txt = font.render("# Channels Vocaux", True, (250,250,250))
        chat_txt = font.render("# Channels Textuels", True, (250,250,250))
        
        self.screen.blit(pseudo_txt, (150,75))
        self.screen.blit(voc_txt, (25,115))
        self.screen.blit(chat_txt, (25,380))
    
    def WritePseudo(self) :
        with open("files/pseudo.json", "r") as p :
            pseudo_mail = json.load(p)
        return pseudo_mail
    
    def TextSaloon(self, hoover) : 
        chat_img = pygame.image.load(r"img/chat.png")
        voc_img = pygame.image.load(r"img/v.png")
        font_channel = pygame.font.SysFont(None, 25)
        self.colo = [(250,250,250), (250,250,250), (250,250,250), (250,250,250)]
        if hoover != None :
            self.colo[hoover] = (255,255,0)
        else :
            self.RectSaloon()
            
        channel_voc_priv = font_channel.render("Vocal Privé", True, self.colo[0])
        channel_voc_pub = font_channel.render("Vocal Public", True, self.colo[1])
        channel_chat_priv = font_channel.render("VIP", True, self.colo[2])
        channel_chat_pub = font_channel.render("Saloon", True, self.colo[3])
        self.screen.blit(channel_voc_priv,(15,170))
        self.screen.blit(channel_voc_pub,(15,235))
        self.screen.blit(channel_chat_priv,(15,440))
        self.screen.blit(channel_chat_pub,(15,500))
        self.screen.blit(voc_img, (200, 165))
        self.screen.blit(voc_img, (200, 225))
        self.screen.blit(chat_img, (200, 435))
        self.screen.blit(chat_img, (200, 495))
    
    def RectSaloon(self) :
        self.private_voc = pygame.Rect(0, 160, 249, 50)
        self.public_voc = pygame.Rect(0, 220, 249, 50)
        
        self.private_chat = pygame.Rect(0, 425, 249, 50)
        self.public_chat = pygame.Rect(0, 485, 249, 50)
        
        
        
        pygame.draw.rect(self.screen, (60,0,104), self.private_voc)
        pygame.draw.rect(self.screen, (60,0,104), self.public_voc)
        
        pygame.draw.rect(self.screen, (60,0,104), self.private_chat)
        pygame.draw.rect(self.screen, (60,0,104), self.public_chat)
        #(85,26,139)
        
    def LoadImg(self) :
        afk = pygame.image.load(r"img/disconnect.png")
        self.screen.blit(afk, (132,860))
        self.afk_rect = afk.get_rect(topleft=(132,860))
        img_profile = self.Profile(co.RecupererBase64())
        img_profile = pygame.transform.scale(img_profile, (80,80)).convert_alpha()
        img_profile.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.surface_cercle.blit(img_profile, (0,0))
        self.screen.blit(self.surface_cercle, (15, 15))
        
    
    def Profile(self, data) :
        im=Image.open(BytesIO(base64.b64decode(data)))
        return pygame.image.frombytes(im.tobytes(), im.size,im.mode).convert()
        
        
    def Logo(self, bool, called) :
        settings = pygame.image.load(r"img/settings.png")
        if bool :
            mic = pygame.image.load(r"img/mic.png")
            
        else :
            mic = pygame.image.load(r"img/mute.png")
        
        if called :
            phone = pygame.image.load(r"img/close.png")
            self.phone = phone.get_rect(topleft=(100,860)) 
            self.screen.blit(phone,(100, 860))
            
            
        self.mic_rect = mic.get_rect(topleft=(170,860))   
        self.settings_rect = settings.get_rect(topleft=(208,860)) 
        self.screen.blit(mic,(170, 860))
        self.screen.blit(settings,(208, 860))
        
        
    def Regroup(self, bool, called) :
        self.ShowScreen()
        self.DrawLine()
        self.LoadImg()
        self.Logo(bool, called)
        self.Text()
        self.RectSaloon()
        self.TextSaloon(None)
        #self.ChatBox()
        
    def ExitWindow(self, focusy, focusn) :
        overlay_bord = pygame.Rect(0, 540, 250, 300)
        self.overlay = pygame.Surface((250, 300))
        self.overlay.fill((50,50,50))
        font = pygame.font.SysFont(None, 30)
        f = font.render("Souhaitez-vous", True, (250, 250, 250))
        f2 = font.render("vous déconnecter ?", True, (250, 250, 250))
        y_txt = font.render("Yes", True, (250, 250, 250))
        n_txt = font.render("No", True, (250, 250, 250))
        
        self.overlay.blit(f, (45,10))
        self.overlay.blit(f2, (33,35))
        self.yes = pygame.Rect(75, 100, 100, 50)
        pygame.draw.rect(self.overlay, (250,0,0), self.yes)
        if focusy :
            pygame.draw.rect(self.overlay, (250,250,250), self.yes, 2)
        self.no = pygame.Rect(75, 200, 100, 50)
        pygame.draw.rect(self.overlay, (0,0,250), self.no)
        if focusn :
            pygame.draw.rect(self.overlay, (250,250,250), self.no, 2)
        self.overlay.blit(y_txt, (105,115))
        self.overlay.blit(n_txt, (110,215))
        self.screen.blit(self.overlay, (0,540))
        pygame.draw.rect(self.screen, (250,250,250), overlay_bord, 2)
    
    def ChangeImage(self, num) :
        overlay_bord = pygame.Rect(0, 540, 250, 300)
        self.overlay = pygame.Surface((250,300))
        self.overlay.fill((50,50,50))
        cross = pygame.image.load("img/cross.png")
        if num == 1 or number == 0:
            self.check1 = pygame.image.load("img/check.png")
            self.check2 = pygame.image.load("img/void.png")
            self.check3 = pygame.image.load("img/void.png")
            self.check4 = pygame.image.load("img/void.png") 
        elif num == 2 :
            self.check1 = pygame.image.load("img/void.png")
            self.check2 = pygame.image.load("img/check.png")
            self.check3 = pygame.image.load("img/void.png")
            self.check4 = pygame.image.load("img/void.png") 
        elif num == 3 :
            self.check1 = pygame.image.load("img/void.png")
            self.check2 = pygame.image.load("img/void.png")
            self.check3 = pygame.image.load("img/check.png")
            self.check4 = pygame.image.load("img/void.png") 
        elif num == 4 :
            self.check1 = pygame.image.load("img/void.png")
            self.check2 = pygame.image.load("img/void.png")
            self.check3 = pygame.image.load("img/void.png")
            self.check4 = pygame.image.load("img/check.png") 
        
        self.check_rect1 = self.check1.get_rect(topleft=(10,100))
        self.check_rect2 = self.check2.get_rect(topleft=(10,130))
        self.check_rect3 = self.check3.get_rect(topleft=(10,160))
        self.check_rect4 = self.check4.get_rect(topleft=(10,190))
        self.cross_rect = cross.get_rect(topleft=(205,0))
        
        self.overlay.blit(self.check1, (10,100))
        self.overlay.blit(self.check2, (10,130))
        self.overlay.blit(self.check3, (10,160))
        self.overlay.blit(self.check4, (10,190))
        self.overlay.blit(cross, (205,0))
        font = pygame.font.SysFont(None, 25)
        self.change_box = pygame.Rect(10,50, 230, 35)
        pygame.draw.rect(self.overlay, (100,100,100), self.change_box)
        f = font.render("Changer l'image de profile", True, (250, 250, 250))
        default = font.render("Style par défaut", True, (250, 250, 250))
        fire = font.render("Feu", True, (250, 250, 250))
        bubble = font.render("Bulles", True, (250, 250, 250))
        rock = font.render("Roche", True, (250, 250, 250))
        self.overlay.blit(f, (15,55))
        self.overlay.blit(default, (40,105))
        self.overlay.blit(fire, (40,135))
        self.overlay.blit(bubble, (40,165))
        self.overlay.blit(rock, (40,195))
        self.screen.blit(self.overlay, (0, 540))
        pygame.draw.rect(self.screen, (250,250,250), overlay_bord, 2)
    
    
    def CheckingStyle(self, num) :
        if num == 1 :
            self.style = "DEF" 
        elif num == 2 :
            self.style = "FIR" 
        elif num == 3 :
            self.style = "BUB" 
        elif num == 4 :
            self.style = "ROC" 
        return num
            
    def ChatBox(self, bool, chatting) :
        self.chatbox = pygame.Rect(252,800,648,100)
        if chatting :
            pygame.draw.rect(self.screen, (35,35,35), self.chatbox)
            if bool :
                pygame.draw.rect(self.screen, (35,255,35), self.chatbox, 2)
            else :
                pygame.draw.rect(self.screen, (255,35,35), self.chatbox, 2)
        else :
            pygame.draw.rect(self.screen, (150,150,150), self.chatbox)
            pygame.draw.rect(self.screen, (0,0,0), self.chatbox, 2)

    
    def TextInput(self, event, bool) :
        font = pygame.font.SysFont(None, 26)
        y = self.chatbox.y+10
        pygame.key.set_repeat(500,45)
        if bool :
            if event.key == pygame.K_BACKSPACE :
                self.current = self.current[:-1]
            elif event.key == pygame.K_RETURN:
                msg = self.current
                heure = datetime.datetime.now().strftime("%H:%M")
                reponse = "None"
                co.SendMsg(msg, heure, reponse)
                self.current = ""
            else :
                if self.chatbox.w - 30 > font.size(self.current)[0] :
                    self.current += event.unicode 
                else :
                    pass
                    
                 #   self.chatbox.x = 0
            
            txt = font.render(f"{self.current}"+"|", True, (250,250,250))
            pygame.draw.rect(self.screen, (35,35,35), self.chatbox)
            pygame.draw.rect(self.screen, (35,255,35), self.chatbox, 2)
            #if self.chatbox.w - 30 > font.size(self.txt_chat)[0]  :
            self.screen.blit(txt, (self.chatbox.x+10, y))   
          
            
            #else :
                #txt = font.render(f"{self.txt_chat}"+"|", True, (250,250,250))
                #txt = font.render(self.txt_chat[-1], True, (250,250,250))
                #y += 15
                #self.screen.blit(txt, (self.chatbox.x+10, y))   
                
    def VarMute(self, number) :
        with open("files/.mute", "w") as m :
            m.write(number)
    
    def ConnectedUser(self, img) :
        #global bool, called
        #### POUR CHAQUE IMG BLIT + 100
        img = self.Profile(img)
        img = pygame.transform.scale(img, (85,85))
        return img
        #pygame.display.update()
        
            


class Connexion() :
    def __init__(self) :
        self.conn = mysql.connector.connect(
            user = "michael_zanaglia",
            passwd = "PhDxDGc6",
            host = "cannes-mysql.local",
            database = "michael_zanaglia"
        )
        self.cursor = self.conn.cursor()
        self.x = 10
        self.loaded_msgs=0
        

    def SupprimerLigneRun(self):
        self.cursor.execute("delete from run where pseudo = '{}'".format(p.mail))
        self.conn.commit()
    
    def RecupererBase64(self) :
        self.cursor.execute("select base64 from img where pseudo = '{}'".format(p.mail))
        self.base = self.cursor.fetchall()
        return self.base[0][0]
    
    def ChangeImg(self) :
        try :
            path = easygui.fileopenbox(title="Choisir une image en .PNG", filetypes=["*.png", "*.jpg"])
            buffered = BytesIO()
            ext=pathlib.Path(path).suffix
            ext=ext.replace('.','').upper()
            if ext=='JPG':
                ext='JPEG'
            image=Image.open(path)
            img_cv2=cv2.imread(path)
            h,w,c=img_cv2.shape
            if w >= h:
                image=image.crop(((w-h)/2,0,(w-h)/2+h,h))
            else:
                image=image.crop((0,(h-w)/2,w,(h-w)/2+w))
            try :
                image=image.resize((80,80))
            except :
                pass
            image.save(buffered, format=ext)
            img_str = base64.b64encode(buffered.getvalue())
            img_str=str(img_str).replace("b'",'').replace("'",'')
            self.cursor.execute("update img set base64 = '{}' where pseudo = '{}'".format(img_str, p.mail))
            self.conn.commit()
        except :
            pass
        
    def SendMsg(self, msg, hr, res) :
        self.cursor.execute("insert into msg (msg, mail, heure, style, reponse) values (%s,%s,%s, %s, %s)",(msg, p.mail, hr, p.style, res))
        self.conn.commit()
    
    def WhosConnected(self) :
        self.cursor.execute("select pseudo from run")
        self.liste_mail = self.cursor.fetchall()
        self.conn.commit()
        p.sfc_img.fill("#4b0082")
        if len(self.liste_mail) > 1 :
            for x in self.liste_mail :
                index = self.liste_mail.index(x)
                user = self.liste_mail[index][0]
                if user != p.mail :
                    self.cursor.execute("select base64 from img where pseudo = '{}'".format(user))
                    self.img = self.cursor.fetchall()
                    self.img = self.img[0][0]
                    img = p.ConnectedUser(self.img)
                    rect_img = img.get_rect(topleft=(self.x,8))
                    p.sfc_img.blit(img, (self.x,8))
                    self.x += 100
                    if self.x > (p.width_surface - 80) :
                        p.width_surface += 255
                        p.sfc_img  = pygame.Surface((p.width_surface,100))
                    pygame.draw.rect(p.sfc_img, (0,255,0), rect_img, 2)
        else :
            p.sfc.blit(p.sfc_img, (p.x,0))

        #print(self.x, "&")
        #print(p.width_surface)
        self.x = 10
    
    def TakeData(self) :
        request = "select * from msg"
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        for x in data :
            datas = (x[1],x[2],x[3],x[4], x[5])
            self.loaded_msgs+=1
            self.percent=self.loaded_msgs/len(data)*100
            print(int(self.percent))
            p.LoadMessageStart(datas)
            p.screen.fill((0,0,0))
            p.text = p.font.render('Chargement des messages', True, (255,255,255), (0,0,0))
            p.lm_txt = p.font.render((str(int(self.percent))+'%'), True, (255,255,255), (0,0,0))
            p.screen.blit(p.text,(180,450))
            p.screen.blit(p.lm_txt,(180,520))
            p.last_load = x[0]
            pygame.display.update()

    def TakeLastLine(self) :
        request = "select * from msg where ID = (select max(ID) from msg)"
        self.cursor.execute(request)
        last = self.cursor.fetchall()
        self.conn.commit()
        p.LoadMessage(last)
        return last
    
    def TakePseudoOfUsers(self,mail) :
        request = "select name from acces where mail = '{}'".format(mail)
        self.cursor.execute(request)
        m = self.cursor.fetchall()
        return m[0][0]
    
        
    
                
        
                
                
       
mooving = False   
setting = False
running = True
active = False
focus = False
bool = True
bool_for_box = False
chatting = False
called = False
scrolling = False
number = 0
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
co = Connexion()
p = Py(900,900)
p.Regroup(bool, called)
p.ChatBox(bool_for_box, chatting)
co.TakeData()
#print(co.TakeLastLine()[0][1])

try : 
    while running :
    
        p.tick_g+=1
        if p.tick_g==61:
            p.tick_g=1
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
                
            if event.type == pygame.MOUSEWHEEL:
                p.msgy+=event.y*45
                if p.msgy>0:
                    p.msgy=0
                if p.msgy < 686-p.message_height:
                    p.msgy=686-p.message_height
            if event.type == pygame.MOUSEBUTTONDOWN :
                posx, posy = pygame.mouse.get_pos()
                if p.bar.collidepoint(posx, posy) and not active and not setting and scrolling :
                    mooving = True
                if p.afk_rect.collidepoint(posx, posy) and not setting:
                    active = True
                    p.ExitWindow(focus, False)
                if p.settings_rect.collidepoint(posx, posy) and not active :
                    setting = True
                    p.ChangeImage(number)
                if setting :
                    if p.cross_rect.collidepoint(posx -0, posy - 540) :
                        setting = False 
                    if p.change_box.collidepoint(posx -0, posy - 540) :
                        co.ChangeImg()
                    if p.check_rect1.collidepoint(posx -0, posy - 540) :
                        number = p.CheckingStyle(1)
                    if p.check_rect2.collidepoint(posx -0, posy - 540) :
                        number = p.CheckingStyle(2)
                    if p.check_rect3.collidepoint(posx -0, posy - 540) :
                        number = p.CheckingStyle(3)
                    if p.check_rect4.collidepoint(posx -0, posy - 540) :
                        number = p.CheckingStyle(4)
                if active :
                    if p.yes.collidepoint(posx - 0, posy - 540) :
                        focus = True
                        p.ExitWindow(focus, False)
                        pygame.display.update()
                        pygame.time.delay(500)
                        subprocess.Popen(["python", "connect.py"])
                        co.SupprimerLigneRun()
                        pygame.quit()
                        sys.exit()
                        #revenir sur l'ecran de connexion
                    if p.no.collidepoint(posx - 0, posy - 540) :
                        active = False
                        focus = True
                        p.ExitWindow(False, focus)
                if p.mic_rect.collidepoint(posx, posy) :
                    if active == False and setting == False :
                        if bool :
                            bool = False
                            p.Logo(bool, called)
                            p.VarMute("1")
                        else :
                            bool = True
                            p.Logo(bool, called)
                            p.VarMute("0")
                if p.chatbox.collidepoint(posx, posy) and chatting :
                    bool_for_box = True
                    p.ChatBox(bool_for_box, chatting)
                else :
                    bool_for_box = False
                    p.ChatBox(bool_for_box, chatting)
                if p.public_chat.collidepoint(posx, posy) :
                    chatting = True
                if not called :
                    if p.public_voc.collidepoint(posx, posy) :
                        sound = pygame.mixer.Sound("sound/connect.mp3")
                        sound.play()
                        client = subprocess.Popen(["python", "Client2.py"])
                        called = True
                        p.Logo(bool, called)
                if called :
                    try :
                        if p.phone.collidepoint(posx, posy) :
                            sound = pygame.mixer.Sound("sound/bye.mp3")
                            client.terminate()
                            sound.play()
                            called = False
                            p.Logo(bool, called)
                    except : 
                        pass
            if event.type == pygame.MOUSEBUTTONUP :
                mooving = False
                if active and not setting:
                    focus = False
                    p.ExitWindow(focus, False)
                else : 
                    focus = False
                    p.Regroup(bool, called)
                    p.ChatBox(bool_for_box, chatting)
                if setting :
                    p.ChangeImage(number)
            
            if event.type == pygame.MOUSEMOTION :
                case = [p.private_voc, p.public_voc, p.private_chat, p.public_chat]
                posx, posy = pygame.mouse.get_pos()
                if mooving and not active and not setting :
                    p.MooveBar()
                if not active and not setting:
                    ind = None
                    for x in case :
                        if x.collidepoint(posx,posy):
                            ind = case.index(x)
                            pygame.draw.rect(p.screen, (85,26,139), x)
                            p.TextSaloon(ind)
                    
                        else :
                            pygame.draw.rect(p.screen, (60,0,104), x)
                    
                    p.TextSaloon(ind)
                    
            if event.type == pygame.KEYDOWN and not active and not setting :
                p.TextInput(event, bool_for_box)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_DOWN:
                    p.msgy=-abs(p.message_height-686)
        ###### VERIFIER LA TABLE run ET SI JE VOIS UN MAIL QUI N'EST PAS LE MIEN JE PRINT L'IMAGE DU MAIL EN QUESTION
        p.screen.blit(p.sfc,(252,0)) 
        p.sfc.blit(p.sfc_img, (p.x,0))
        co.WhosConnected()
        if len(co.liste_mail) >= 7 :
            scrolling = True
        else :
            scrolling = False
        if scrolling :
            p.ShowScroll()
        
        
        co.TakeLastLine()
                
        p.msg_zone.blit(p.shown_messages,(0,p.msgy))
        p.screen.blit(p.msg_zone,(252,114))

        pygame.display.flip()
        clock.tick(240)
        
    # 10.10.85.129
    print("bye")
    try :
        subprocess.Popen(["python", "Server2.py"]).terminate()
    except :
        pass
    co.SupprimerLigneRun()
    pygame.quit()
    sys.exit()
except Exception as e:
    print(e)
    print(traceback.format_exc())
    subprocess.Popen(["python", "Server2.py"]).terminate()
    co.SupprimerLigneRun()
    pygame.quit()
    sys.exit()