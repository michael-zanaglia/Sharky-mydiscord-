import socket
import threading
import os
import time
import datetime

class Server:
    def __init__(self):
        self.host = "192.168.1.12" #modifier ######################
        self.port = 5555
        self.clients = []  # Lista dei client connessi

        # Inizializzazione del server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def start_server(self):
        """Avvia il server."""
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection accepted from {client_address}")
                self.clients.append((client_socket, client_address))

                # Avvia un thread separato per gestire il client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except Exception as e:
            print(f"Error in server: {e}")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        """Gestisce la connessione di un client."""
        try:
            while True:
                audio_data = client_socket.recv(8096)  # Riceve dati audio dal client
                if not audio_data:
                    print("End of reception")
                    break
                # Gestisci i dati audio ricevuti
                # Per ora, stampiamo solo la dimensione dei dati ricevuti
                print(f"Received audio data size: {len(audio_data)} bytes")

                # Invia l'audio ricevuto a tutti i client tranne al mittente originale
                for other_client_socket, _ in self.clients:
                    if other_client_socket != client_socket:
                        other_client_socket.sendall(audio_data)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            # Chiudi la connessione del client
            client_socket.close()
            print("Connection closed.")

def main():
    server = Server()
    server.start_server()

if __name__ == "__main__":
    main()
