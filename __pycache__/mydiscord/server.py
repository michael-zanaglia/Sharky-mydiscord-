#import socket

#HOST =  socket.gethostbyname(socket.gethostname())
#PORT = 9531

#server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server.bind((HOST, PORT))

#print("Connexion au server done...")
#while True :
#    server.listen(5)
#    conn, addr = server.accept()
#    print(f"Connecte avec {conn} & {addr}")
#    data = conn.recv(1024).decode('utf-8')
#    print(f"Message recu : {data}")
#    response = f"Merci pour ton message {addr} ;). à bientot !"
#    conn.send(response.encode('utf-8'))
#    conn.close()
#    print("Fini")

 # cd Desktop/Laplateforme/code/sql/mydiscord

import pyaudio
import threading
import socket
import random


class VocalServer():
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.clients = []
        self.lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        print(f"Nouveau client connecté : {client_address}")

        recv_audio = self.audio.open(
            format=pyaudio.paInt16,
            output=True,
            channels=2,
            rate=48000,
            frames_per_buffer=1024*4
        )
        recv_audio.start_stream()
        #print("Son recu")
        self.clients.append(client_address)
        print(len(self.clients))
        while True:
           # client_socket.settimeout(1)
            try:
                data, _ = client_socket.recvfrom(8192*8*len(self.clients))
                #print("a",self.clients)
                #print('data recu')
                #recv_audio.write(data)
            except : #socket.timeout:
                print(f"Client déconnecté : {client_address}")
                self.clients.remove(client_address)
                print("bye")
                print("b",self.clients)
            with self.lock :
                for x in self.clients :
                    
                    client_socket.sendto(data, x)
    
                         

        
            


    def start_server(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        print(f"Serveur en écoute sur {host}:{port}")
        while True :
            data, address = s.recvfrom(8192*4)
            with self.lock :
                if address not in self.clients:
                    #print("Bienvenue a l'addresse :", address)
                    client_thread = threading.Thread(target=self.handle_client, args=(s, address))
                    client_thread.start()

if __name__ == '__main__':
    server = VocalServer()
    server.start_server('10.10.85.129', 9531)
   