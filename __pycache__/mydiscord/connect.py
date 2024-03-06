import socket
import mysql.connector
import pygame
import re
import sys
import subprocess
import json


#HOST =  socket.gethostbyname(socket.gethostname())
#PORT = 9531
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect((HOST, PORT))
#client.send("HELLO NIGHTCITY!!!!".encode('utf-8'))
#data = client.recv(1024).decode("utf8")
#print(data)


class Connexion() :
    
    
    def __init__(self) :
        self.conn = mysql.connector.connect(
            user = "root",
            passwd = "Pokemine20-",
            host = "localhost",
            database = "mydiscord"
        )
        self.cursor = self.conn.cursor()
        self.l_name = []
        self.l_mdp = []
        self.l_mail = [] 
        
    def TakeDataFromAccesTable(self) :
        self.name_acces = self.cursor.execute("select name from acces")
        self.name_acces = self.cursor.fetchall()
        for x in range(len(self.name_acces)) :
            self.l_name.append(self.name_acces[x][0])
        self.passwd_acces = self.cursor.execute("select password from acces")
        self.passwd_acces = self.cursor.fetchall()
        for x in range(len(self.passwd_acces)) :
            self.l_mdp.append(self.passwd_acces[x][0])
        self.mail_acces = self.cursor.execute("select mail from acces")
        self.mail_acces = self.cursor.fetchall()
        for x in range(len(self.mail_acces)) :
            self.l_mail.append(self.mail_acces[x][0])
    
    def NewSubscriber(self, name, password, mail) :
        if mail in self.l_mail :
            p.LabelError("Erreur le mail existe deja.", True)
        elif p.spe == [] or len(password) < 8 :
            pygame.draw.rect(p.screen, (100, 100, 255), pygame.Rect(100, 590, 400, p.label_co.get_height()))
            p.LabelError("Votre mot de passe doit contenir au moins 8 caracteres dont au moins 1 spécial.", False)
        else :   
            try :
                pygame.draw.rect(p.screen, (100, 100, 255), pygame.Rect(100, 560, 600, 50))
                pygame.draw.rect(p.screen, (100, 50, 255), pygame.Rect(700, 560, 20, 50))
                self.cursor.execute("insert into acces (name, password, mail) values ('{}', '{}', '{}')".format(name, password, mail))
                self.conn.commit()
                p.LabelConnected("Bienvenue chez Sharky ! Vous pouvez vous connecter.", False)
                base64 = self.VarBse()
                self.cursor.execute("insert into img (pseudo, base64) values ('{}', '{}')".format(name, base64))
                self.conn.commit()
                p.spe = []
                pygame.time.delay(500)
            except :
                p.LabelError("Entrer un mail valide.", True)
            self.TakeDataFromAccesTable()
    
    def VarBse(self) :
        with open(".defaultimg", "r") as f :
            return f.read()
                
        
class Formulaire() :
    
    
    def __init__(self, nom, mdp, mail) :
        self.nom = nom
        self.mdp = mdp
        self.mail = mail
        
    def CheckAccount(self, conn) :
        print(conn)
        check = False
        if conn :
            if self.mail in connect.l_mail :
                index = connect.l_mail.index(self.mail)
                if self.mdp == connect.l_mdp[index] and  self.nom == connect.l_name[index] :
                    check = True
                else :
                    p.LabelConnected("Connexion échouée.", True)
            else :
                p.LabelConnected("Connexion échouée.", True)
            if check :
                p.LabelConnected("Connexion réussie !", True)
                pygame.display.update()
                pygame.time.delay(1000)
                self.RegisterOnJson(self.nom)
                subprocess.Popen(["python", "main.py"])
                subprocess.Popen(["python", "server.py"])
                connect.cursor.execute("insert into run (pseudo, mail) values ('{}', '{}')".format(self.nom, self.mdp))
                connect.conn.commit()
                #subprocess.Popen(["python", "vocal.py"])
                pygame.quit()
                sys.exit()
                
                
        else :
            if self.nom == "" or self.mdp == "" or self.mail == "" :
                p.LabelConnected("Remplissez tout les champs obligatoires.", False)
            else :
                connect.NewSubscriber(self.nom, self.mdp, self.mail)
    
    def RegisterOnJson(self, nom) :
        put_in = []
        put_in.append(nom)
        with open("pseudo.json", "w") as p :
            json.dump(put_in, p, indent=4) 
        
        
class Py() :
    def __init__(self, L, l) :
        self.L = L
        self.l = l
        self.screen = pygame.display.set_mode((self.L, self.l))
        self.text = ""
        self.text2 = ""
        self.text3 = ""
        self.state = None
        self.sharky = pygame.image.load(r"img/sharky.png")
        
    def ShowScreenColor(self) :
        color_screen = pygame.Color((100,50,255))     
        self.screen.fill(color_screen)   
        
    def OverlayForForm(self) :
        L_overlay = 600
        l_overlay = 600
        self.L_overlay =  self.L//2-L_overlay//2
        self.l_overlay = self.l//2-l_overlay//2
        self.windows_for_input = pygame.Rect(self.L_overlay, self.l_overlay , L_overlay, l_overlay)
        color_windows = (100, 100, 255, 50)
        pygame.draw.rect(self.screen, color_windows, self.windows_for_input)
        self.screen.blit(self.sharky, (150,150))
    
    def LabelError(self, txt, bool) :
        pygame.draw.rect(self.screen, (100, 100, 255), pygame.Rect(100, 560, 600, 50))
        if bool :
            font = pygame.font.SysFont(None, 30)
            self.label_error = font.render(txt, True, (255,0,0))
            pygame.draw.rect(self.screen, (100, 100, 255), pygame.Rect(300, 590, 400, self.label_co.get_height()))
            self.screen.blit(self.label_error, (400, 560))
        else :
            font = pygame.font.SysFont(None, 24)
            self.label_error = font.render(txt, True, (255,0,0))
            self.screen.blit(self.label_error, (100, 560))
    
    def LabelConnected(self, txt, bool) :
        font = pygame.font.SysFont(None, 30)
        self.label_co = font.render(txt, True, (255,255,255))
        pygame.draw.rect(self.screen, (100, 100, 255), pygame.Rect(100, 560, 600, 50))
        pygame.draw.rect(self.screen, (100, 100, 255), pygame.Rect(300, 590, 400, self.label_co.get_height()))
        if bool :
            self.screen.blit(self.label_co, (300, 590))
        else :
            self.screen.blit(self.label_co, (105, 590))
    
    def LabelTitle(self, bool) :
        font = pygame.font.SysFont(None, 70)
        if bool :
            label_title = font.render("Connecte toi !", True, (255,255,255))
        else : 
            label_title = font.render("Rejoins nous !", True, (255,255,255))
        self.screen.blit(label_title, (self.name_box.x, 140))
       
    def BoxForInput(self) :
        font = pygame.font.SysFont(None, 30)
        label_nom = font.render("Pseudo*", True, (255,255,255))
        label_mdp = font.render("Mot de Passe*", True, (255,255,255))
        label_mail = font.render("Adresse-mail*", True, (255,255,255))
        self.screen.blit(label_nom, (200, 320))
        self.screen.blit(label_mdp, (200, 420))
        self.screen.blit(label_mail, (200, 520))
        self.name_box = pygame.Rect(self.L_overlay+250, self.l_overlay+200, 310, 50)
        self.mdp_box = pygame.Rect(self.L_overlay+250, self.l_overlay+300, 310, 50) 
        self.mail_box = pygame.Rect(self.L_overlay+250, self.l_overlay+400, 310, 50)
        pygame.draw.rect(self.screen, (35,35,35), self.name_box)
        pygame.draw.rect(self.screen, (35,35,35), self.mdp_box)
        pygame.draw.rect(self.screen, (35,35,35), self.mail_box) 
        pygame.draw.rect(self.screen, (255,1,1), self.name_box, 2)
        pygame.draw.rect(self.screen, (255,1,1), self.mdp_box, 2)
        pygame.draw.rect(self.screen, (255,1,1), self.mail_box, 2) 
    
    def BoxSignUp(self, conn) :
        self.sub_box = pygame.Rect(650, 25, 120, 50)
        pygame.draw.rect(self.screen, (0,200,60), self.sub_box)
        font = pygame.font.SysFont(None, 25)
        if conn :
            if self.state == 1 :
                pygame.draw.rect(p.screen, (255,255,255), p.sub_box, 2)
            self.state = 0
            label_sub = font.render("S'inscrire", True, (255,255,255))
            self.screen.blit(label_sub, (self.sub_box.x+20, self.sub_box.y+15))
        else : 
            self.state = 1
            pygame.draw.rect(p.screen, (255,255,255), p.sub_box, 2)
            label_sub = font.render("Se connecter", True, (255,255,255))
            self.screen.blit(label_sub, (self.sub_box.x+10, self.sub_box.y+15))
        
    
    def BoxConnexion(self, conn) : 
        self.connx_box = pygame.Rect(self.L_overlay+200, self.l_overlay+525, 210, 50)
        font = pygame.font.SysFont(None, 30)
        if conn : 
            f = font.render("Connexion", True, (255,255,255))
        else :
            f = font.render("S'inscrire", True, (255,255,255))
        pygame.draw.rect(self.screen, (255,0,0), self.connx_box)
        self.screen.blit(f, (self.connx_box.x + self.L_overlay // 2, self.connx_box.y + 15))
    
    def TextInput(self, box, active, event) :
        if box not in [self.name_box, self.mdp_box] :
            self.font = pygame.font.SysFont(None, 27)
        else :
            self.font = pygame.font.SysFont(None, 40)
        self.text_color = (255,255,255)
        if active :
            if event.key == pygame.K_BACKSPACE :
                if box == self.name_box :
                    self.text = self.text[:-1]
                elif box == self.mdp_box :
                    self.text2 = self.text2[:-1]
                elif box == self.mail_box :
                    self.text3 = self.text3[:-1]      
            #elif event.key == pygame.K_TAB :
            #    boxes = [self.name_box, self.mdp_box, self.mail_box] 
            #    if box in boxes :
            #        index = boxes.index(box)
            #        next_index = (index+1) % len(boxes)
            #        box = boxes[next_index] 
            else :
                if box == self.name_box and self.font.size(self.text)[0] < box.w - 40 :
                    self.text += event.unicode 
                elif box == self.mdp_box and self.font.size(self.text2)[0] < box.w - 40 :
                    self.text2 += event.unicode 
                elif box == self.mail_box and self.font.size(self.text3)[0] < box.w - 40 :
                    self.text3 += event.unicode 
                    
        exp = r"[^a-zA-Z0-9]"
        self.spe = re.findall(exp, self.text2)
        if box == self.name_box :
            self.PrintText(self.text, box)
        elif box == self.mdp_box :
            self.PrintText(self.text2, box)
        elif box == self.mail_box :
            self.PrintText(self.text3, box)
    
    
    def PrintText(self, txt, box) :
        inp_text = self.font.render(txt, True, self.text_color)
        pygame.draw.rect(self.screen, (35,35,35), box)
        pygame.draw.rect(self.screen, (1,255,1), box, 2)
        self.screen.blit(inp_text, (box.x + 10, box.y + 10))
        
        
        
        
        
pygame.init()   
pygame.display.set_caption("Sharky")
last_selected = None
active = False
page_conn = True    
connect = Connexion()
connect.TakeDataFromAccesTable()
p = Py(800, 800)
running = True
p.ShowScreenColor()
p.OverlayForForm()
p.BoxForInput()
p.BoxConnexion(page_conn)
p.BoxSignUp(page_conn)
p.LabelTitle(page_conn)


while running :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN :
            posx, posy = pygame.mouse.get_pos()
            for x in [p.name_box, p.mdp_box, p.mail_box] :
                if page_conn :
                    if x.collidepoint(posx, posy) :
                        if last_selected in [p.name_box, p.mdp_box, p.mail_box] : 
                            pygame.draw.rect(p.screen, (255,1,1), last_selected, 2)
                        pygame.draw.rect(p.screen, (1,255,1), x, 2)
                        active = True
                        last_selected = x
                if not page_conn :
                    if x.collidepoint(posx, posy) :
                            if last_selected in [p.name_box, p.mdp_box, p.mail_box] : 
                                pygame.draw.rect(p.screen, (255,1,1), last_selected, 2)
                            pygame.draw.rect(p.screen, (1,255,1), x, 2)
                            active = True
                            last_selected = x
            
            if p.connx_box.collidepoint(posx, posy) :
                pygame.draw.rect(p.screen, (255,255,255), p.connx_box, 2)
                form = Formulaire(p.text, p.text2, p.text3)
                form.CheckAccount(page_conn)
                
            if p.sub_box.collidepoint(posx, posy) :
                p.text, p.text2, p.text3 = "", "", ""
                if page_conn :
                    page_conn = False
                else :
                    page_conn = True
                p.ShowScreenColor()
                p.OverlayForForm()
                p.BoxSignUp(page_conn)
                p.BoxForInput()
                p.BoxConnexion(page_conn)
                p.LabelTitle(page_conn)
        if page_conn :
            if event.type == pygame.KEYDOWN :
                p.TextInput(last_selected, active, event)
        if not page_conn :
            if event.type == pygame.KEYDOWN :
                p.TextInput(last_selected, active, event)
        
        if event.type == pygame.MOUSEBUTTONUP :
            pygame.draw.rect(p.screen, (255,0,0), p.connx_box, 2)
            pygame.draw.rect(p.screen, (0,200,60), p.sub_box, 2)
            
                
    
    pygame.display.flip()
    
pygame.quit()
sys.exit()