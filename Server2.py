import socket, threading, os, time, datetime, logging
from Service import notification

class Server:
    def __init__(self):
        self.host = "10.10.103.23"
        self.port = 5555
        self.clients = []  # Lista dei client connessi
        

        # Inizializzazione del server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        print(f"{self.host}")
        self.server_socket.listen()

        logging.basicConfig(filename='server_log.txt', level=logging.ERROR)

        

    def start_server(self):
        """Avvia il server."""
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection accepted from {client_address}")
                self.clients.append((client_socket, client_address))
                self.send_notification_to_all("online", "")
                # Avvia un thread separato per gestire il client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except Exception as e:
            logging.error(f"Error in server: {e}")
        finally:
            self.server_socket.close()


            
    def handle_client(self, client_socket):
        """Gestisce la connessione di un client."""

        try:
            # Invia notifica di connessione al client
            self.send_notification_to_all("online", client_socket.getpeername())
            while True:
                audio_data = client_socket.recv(1024)  # Riceve dati audio dal client
                if not audio_data:
                    print("End of reception")
                    break
                # Gestisci i dati audio ricevuti
                # Per ora, stampiamo solo la dimensione dei dati ricevuti
                print(f"Received audio data size: {len(audio_data)} bytes")

                # Invia l'audio ricevuto a tutti i client tranne al mittente originale
                for other_client_socket, _ in self.clients:
                    if other_client_socket != client_socket:
                        try:
                            other_client_socket.sendall(audio_data)
                        except Exception as e:
                            logging.error(f"Error sending audio data to other client: {e}")
                            # Gestione dell'errore: Chiudi la connessione del client
                            # Chiudi la connessione del client e invia notifica di indisponibilità
                            self.send_notification_to_all("indisponible", other_client_socket.getpeername())

                            other_client_socket.close()
                            self.clients.remove((other_client_socket, _))
                            continue  # Passa al prossimo client
        except ConnectionResetError:
            print("Connessione resettata dal client.")
        except Exception as e:
            logging.error(f"Error handling client: {e}")
        finally:
            # Invia notifica di disconnessione al client
            self.send_notification_to_all("offline", client_socket.getpeername())
            # Rimuovi il client dalla lista dei client connessi
            self.clients.remove((client_socket, _))
            # Chiudi la connessione del client
            client_socket.close()
            print("Connection closed.")

    def send_notification_to_all(self, status, user):
        """Invia una notifica a tutti i client connessi."""
        for client_socket, _ in self.clients:
            client_socket.sendall(f"Notification {status}".encode())
            notif = notification.Notification(status=status, user=user)
            notif.show_notification(duration=3, text=f"{user} é {status}!")
            # Invia il messaggio al client

    def broadcast_message(self, message, sender_socket):
        """Invia il messaggio a tutti i client tranne al mittente originale."""
        for client_socket, _ in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode())
                except Exception as e:
                    logging.error(f"Error sending message to client: {e}")
                    
                    # Gestione dell'errore: Chiudi la connessione del client
                    # Chiudi la connessione del client e invia notifica di indisponibilità
                    self.send_notification_to_all("indisponible", client_socket.getpeername())
                    client_socket.close()
                    self.remove_client(client_socket)
                    continue  # Passa al prossimo client

    def close(self):
        """Chiude il server e pulisce le risorse."""
        # Invia notifica di disconnessione a tutti i client
        self.send_notification_to_all("offline", "Server")
        # Chiude le connessioni dei client
        for client_socket, _ in self.clients:
            try:
                client_socket.close()
            except Exception as e:
                print(f"Error closing client connection: {e}")
        # Chiude il server socket
        try:
            self.server_socket.close()
        except Exception as e:
            print(f"Error closing server socket: {e}")

def main():
    server = Server()
    server.start_server()
    notif = notification.Notification(status="online", user="Server")
    notifd = notification.Notification(status="offline", user="Server")
    notif.show_notification(7, "Server starting...")
    try:
        # Mantieni il thread principale in esecuzione
        while True:
            pass
    except KeyboardInterrupt:
        # Chiudi il server quando viene rilevato KeyboardInterrupt (Ctrl+C)
        notifd.show_notification(7,"Server closing...")
        server.close()
if __name__ == "__main__":
    main()
