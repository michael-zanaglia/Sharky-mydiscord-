import socket, threading, pyaudio, time, datetime, keyboard, wave, os, zlib
from Service.notification import Notification

import logging


class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

        # Audio settings
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 8096

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

        # Initialize audio streams for recording and playback
        self.stream_rec = self.audio.open(format=self.format,
                                          channels=self.channels,
                                          rate=self.rate,
                                          input=True,
                                          frames_per_buffer=self.chunk)
        self.stream_play = self.audio.open(format=self.format,
                                           channels=self.channels,
                                           rate=self.rate,
                                           output=True)
    
        # Initialize socket for communication with the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))

        # Inizialize File audio
        self.frames = []
    
        # Configura il logger
        logging.basicConfig(filename='client.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # def compress_audio_data(self, data):
    #     # Comprimi i dati audio utilizzando zlib
    #     compressed_data = zlib.compress(data)
    #     return compressed_data
    

    def start_notif(self):
        try:
            # Invia notifica di connessione al server
            notif = threading.Thread(target=self.receive_message_to_server)
            online = threading.Thread(target=self.send_message_to_server("online"))
            notif.start()
            online.start()
        except Exception as e:
            logging.error(f"Errore in start_notif: {e}")

#### Call ####
    def start_audio_threads(self):
        # Avvia thread audio per invio e ricezione
        recv_thread = threading.Thread(target=self.receive_audio)
        send_thread = threading.Thread(target=self.send_audio)

        recv_thread.start()
        send_thread.start()
        

    def send_audio(self):
        try:
            while True:
                data = self.stream_rec.read(self.chunk)
                self.client_socket.sendall(data)
                # compress_data = self.compress_audio_data(data)
                # self.client_socket.sendall(compress_data)
                print(f"Envoye {len(data)} bytes")
        except Exception as e:
            logging.error(f"Errore in send_audio: {e}")    
    

    def receive_audio(self):
        while True:
            audio_data = self.client_socket.recv(self.chunk)
            self.stream_play.write(audio_data)

    def receive_message_to_server(self):
        while True:
            data = self.client_socket.recv(1024).decode()
            user = self.client_socket.getpeername()
            stat = ["online", "offline", "indisponible"]
            for status in stat:
                if status in data:
                    notif = Notification(status, user)
                    notif.show_notification(10, text=f"{user} é ora {status}!")
                else:
                    continue

    def send_message_to_server(self, message):
        while True:
            # Invia il messaggio al server
            self.client_socket.sendall(message.encode())
            break
#### Vocal message ####
    def start_recording(self):
        print("Press Enter to start recording...")
        keyboard.wait("enter")
        print("Recording...")
        
        # Prepara il salvataggio dell'audio
        program_folder = os.getcwd()
        current_time = datetime.datetime.now()
        folder_name = current_time.strftime("%Y-%m-%d")
        folder_path = os.path.join(program_folder, folder_name)
        try:
            os.makedirs(folder_path)
        except FileExistsError:
            pass
        filename_mp3 = os.path.join(folder_path, f"audio_{current_time.strftime('%H-%M-%S')}.mp3")
        
        # Avvia la registrazione e la conversione in tempo reale
        # audio_segment = AudioSegment.empty()
        while True:
            data = self.stream_rec.read(self.chunk)
            # audio_segment += AudioSegment(data)
            self.frames.append(data)
            if keyboard.is_pressed("UP"):
                print("Recording completed!")
                break
            ############################## Audio compresso ################################
        # # Compressione audio
        # compressed_audio_data = self.compress_audio_data(audio_segment.raw_data)
    
        # Salva l'audio compresso in formato MP3
        with open(filename_mp3, "wb") as audio_file:
            audio_file.write(audio_file)
        print(f"Compressed audio recorded and saved to '{filename_mp3}'.")
            ############################# Audio non compresso #############################
        # Salva l'audio in formato MP3
        # audio_segment.export(filename_mp3, format="mp3")
        # print(f"Audio recorded and saved to '{filename_mp3}'.")

        # Pulisce le risorse audio
        self.stream_rec.stop_stream()
        self.stream_rec.close()

        scelta = self.get_input()

        if scelta == True:
            # Invia l'audio al server
            self.send_audio_to_server(filename_mp3)
        else:
            pass

    def get_input(self):
        print("Vuoi inviare questa registrazione?(y/n)")
        while True:
            try:
                key_press = keyboard.read_event(suppress=True).name.lower()
                if key_press == "y":
                    return True
                elif key_press == "n":
                    return False
                else:
                    print("Opzione non valida. Premi 'y' per sì o 'n' per no.")
            except Exception as e:
                print(f"Errore durante la lettura dell'input: {e}")

    def send_audio_to_server(self, filename):
        print("Sending audio to server...")
        with open(filename, "rb") as audio_file:
            while True:
                data = audio_file.read(self.chunk)
                if not data:
                    break
                self.client_socket.sendall(data)
        print("Audio sent to server.")

    # def listen_audio(self, audio_data):
        # print("Playing audio...")
        # audio_segment = AudioSegment(audio_data)
        # audio_segment.export("received_audio.mp3", format="mp3")
        # os.system("start received_audio.mp3")  # Apre il file audio utilizzando il programma predefinito

    def close(self):
        try:
            if self.client_socket:
                # Invia un segnale di "fine trasmissione" al server prima di chiudere la connessione
                self.client_socket.sendall(b'')  # Invia una stringa vuota come segnale di chiusura
                time.sleep(3)  # Opzionale: attendi un po' per consentire al server di gestire il segnale di chiusura
                # Chiudi la connessione del client
                self.client_socket.close()
        except Exception as e:
            print(f"Errore durante la chiusura del socket: {e}")

        try:
            if self.stream_rec.is_active():
                self.stream_rec.stop_stream()
                self.stream_rec.close()
        except Exception as e:
            print(f"Errore durante la chiusura dello stream di registrazione: {e}")

        try:
            if self.stream_play.is_active():
                self.stream_play.stop_stream()
                self.stream_play.close()
        except Exception as e:
            print(f"Errore durante la chiusura dello stream di riproduzione: {e}")

        try:
            if self.audio.is_active():
                self.audio.terminate()
        except Exception as e:
            print(f"Errore durante la terminazione di PyAudio: {e}")

    def VarMute(self) :
        with open(".mute", "r") as f :
            self.mute = f.read()

def main():
    # Specify the server's address and port
    server_address = '10.10.104.232'
    server_port = 5555

    # Create an instance of the Client class
    client = Client(server_address, server_port)

    # Start audio threads for sending and receiving audio
    client.start_notif()
    client.start_audio_threads()
    
    try:
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        # Close the client when KeyboardInterrupt (Ctrl+C) is detected
        print("Exiting...")
        time.sleep(2)
        client.send_message_to_server("offline")
        time.sleep(1)
        client.close()
    except Exception as e:
        logging.error(f"Errore non gestito in main: {e}")

if __name__ == "__main__":
    main()

