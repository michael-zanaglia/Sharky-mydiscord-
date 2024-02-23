import pygame, subprocess, sys, mysql.connector, json
from PIL import Image
from io import BytesIO
import base64
import easygui, pathlib, cv2, numpy as np



#class Data():
    #def __init__(self) :
    #    self.conn = mysql.connector.connect(
    #        host = "localhost",
    #        user = "root",
    #        password = "",
   #         database = "mydiscord"
    #    )
    #    self.cursor = self.conn.cursor()

class Py() :
    def __init__(self, l, L) :
        self.l = l
        self.L = L
        self.screen = pygame.display.set_mode((self.L, self.l))
        self.txt_chat = ""

        
        
    def ShowScreen(self) :
        pygame.display.set_caption("Sharky")
        screen_color = pygame.Color((75,0,130))
        self.screen.fill(screen_color)
    
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
        pseudo = self.WritePseudo()
        font = pygame.font.SysFont(None, 30)
        if len(pseudo) > 12 :
            font_p = pygame.font.SysFont(None, 25)
        else :
            font_p = font
        pseudo_txt = font_p.render(pseudo, True, (250,250,250))
        voc_txt = font.render("# Channels Vocaux", True, (250,250,250))
        chat_txt = font.render("# Channels Textuels", True, (250,250,250))
        
        self.screen.blit(pseudo_txt, (150,75))
        self.screen.blit(voc_txt, (25,115))
        self.screen.blit(chat_txt, (25,380))
    
    def WritePseudo(self) :
        with open("pseudo.json", "r") as p :
            pseudo = json.load(p)
        for x in pseudo :
            return x
    
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
        return pygame.image.fromstring(im.tobytes(), im.size,im.mode).convert()
        
        
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
        overlay_bord = pygame.Rect((self.L-500)//2, (self.l-125)//2, 500, 125)
        self.overlay = pygame.Surface((500,125))
        self.overlay.fill((50,50,50))
        font = pygame.font.SysFont(None, 30)
        f = font.render("Souhaitez-vous vous déconnecter ?", True, (250, 250, 250))
        y_txt = font.render("Yes", True, (250, 250, 250))
        n_txt = font.render("No", True, (250, 250, 250))
        
        self.overlay.blit(f, (70,10))
        self.yes = pygame.Rect(50, 50, 100, 50)
        pygame.draw.rect(self.overlay, (250,0,0), self.yes)
        if focusy :
            pygame.draw.rect(self.overlay, (250,250,250), self.yes, 2)
        self.no = pygame.Rect(350, 50, 100, 50)
        pygame.draw.rect(self.overlay, (0,0,250), self.no)
        if focusn :
            pygame.draw.rect(self.overlay, (250,250,250), self.no, 2)
        self.overlay.blit(y_txt, (80,65))
        self.overlay.blit(n_txt, (388,65))
        self.screen.blit(self.overlay, ((self.L-500)//2, (self.l-125)//2))
        pygame.draw.rect(self.screen, (250,250,250), overlay_bord, 2)
    
    def ChangeImage(self) :
        overlay_bord = pygame.Rect((self.L-500)//2, (self.l-125)//2, 500, 125)
        self.overlay = pygame.Surface((500,125))
        self.overlay.fill((50,50,50))
        cross = pygame.image.load("img/cross.png")
        self.cross_rect = cross.get_rect(topleft=(450,0))
        self.overlay.blit(cross, (450,0))
        font = pygame.font.SysFont(None, 25)
        self.change_box = pygame.Rect(40,50, 230, 35)
        pygame.draw.rect(self.overlay, (100,100,100), self.change_box)
        f = font.render("Changer l'image de profile", True, (250, 250, 250))
        self.overlay.blit(f, (45,55))
        self.screen.blit(self.overlay, ((self.L-500)//2, (self.l-125)//2))
        pygame.draw.rect(self.screen, (250,250,250), overlay_bord, 2)
        
    def ChatBox(self, bool, chatting) :
        self.chatbox = pygame.Rect(252,800,600,100)
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
                self.txt_chat = self.txt_chat[:-2]
            elif event.key == pygame.K_RETURN:
                #### ENVOYER LE TXT DANS LE SQL PUIS OUVRIR LE CLIENT POUR POUVOIR ENVOYER LE MESSAGE SI LE 
                # MESSAGE EST RECU ME L'AFFICHE DANS TOUT LES MAINS DES USERS
                self.txt_chat = ""
            else :
                if self.chatbox.w - 30 > font.size(self.txt_chat)[0] :
                    self.txt_chat += event.unicode 
            
            txt = font.render(f"{self.txt_chat}"+"|", True, (250,250,250))
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
        with open(".mute", "w") as m :
            m.write(number)
            


class Connexion() :
    def __init__(self) :
        self.conn = mysql.connector.connect(
            user = "root",
            passwd = "votremdp",
            host = "localhost",
            database = "mydiscord"
        )
        self.cursor = self.conn.cursor()
        
    def RecupererBase64(self) :
        self.cursor.execute("select base64 from img where pseudo = '{}'".format(p.WritePseudo()))
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
                print('vertical')
            image=image.resize((128,128))
            image.save(buffered, format=ext)
            img_str = base64.b64encode(buffered.getvalue())
            img_str=str(img_str).replace("b'",'').replace("'",'')
            print(img_str)
            self.cursor.execute("update img set base64 = '{}' where pseudo = '{}'".format(img_str, p.WritePseudo()))
            self.conn.commit()
        except :
            pass
        
    
setting = False
running = True
active = False
focus = False
bool = True
bool_for_box = False
chatting = False
called = False
pygame.init()
pygame.mixer.init()
co = Connexion()
p = Py(900,900)
p.Regroup(bool, called)
p.ChatBox(bool_for_box, chatting)
#took = take
#try :#
   # print(take)
#except :
#    pass



while running :
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN :
            posx, posy = pygame.mouse.get_pos()
            if p.afk_rect.collidepoint(posx, posy) and not setting:
                active = True
                p.ExitWindow(focus, False)
            if p.settings_rect.collidepoint(posx, posy) and not active :
                setting = True
                p.ChangeImage()
            if setting :
                if p.cross_rect.collidepoint(posx -((p.L-500)//2), posy - ((p.l-125)//2)) :
                    setting = False 
                if p.change_box.collidepoint(posx -((p.L-500)//2), posy - ((p.l-125)//2)) :
                    co.ChangeImg()
            if active :
                if p.yes.collidepoint(posx -((p.L-500)//2), posy - ((p.l-125)//2)) :
                    focus = True
                    p.ExitWindow(focus, False)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    subprocess.Popen(["python", "connect.py"])
                    pygame.quit()
                    sys.exit()
                    #revenir sur l'ecran de connexion
                if p.no.collidepoint(posx -((p.L-500)//2), posy - ((p.l-125)//2)) :
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
            if p.public_voc.collidepoint(posx, posy) :
                sound = pygame.mixer.Sound("connect.mp3")
                sound.play()
                client = subprocess.Popen(["python", "Client2.py"])
                called = True
                p.Logo(bool, called)
            try :
                if p.phone.collidepoint(posx, posy) :
                    sound = pygame.mixer.Sound("bye.mp3")
                    sound.play()
                    called = False
                    p.Logo(bool, called)
                    client.terminate()
            except : 
                pass
        if event.type == pygame.MOUSEBUTTONUP :
            if active and not setting:
                focus = False
                p.ExitWindow(focus, False)
            else : 
                focus = False
                p.Regroup(bool, called)
                p.ChatBox(bool_for_box, chatting)
            if setting :
                p.ChangeImage()
        
        if event.type == pygame.MOUSEMOTION :
            case = [p.private_voc, p.public_voc, p.private_chat, p.public_chat]
            posx, posy = pygame.mouse.get_pos()
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
    pygame.display.flip()
    
# 10.10.85.129
print("bye")
subprocess.Popen(["python", "Server2.py"]).terminate()
pygame.quit()
sys.exit()
