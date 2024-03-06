import socket
import threading
import pyaudio, time

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

    def start_audio_threads(self):
        # Start separate threads for sending and receiving audio
        recv_thread = threading.Thread(target=self.receive_audio)
        send_thread = threading.Thread(target=self.send_audio)

        recv_thread.start()
        send_thread.start()
        print("ricezione attiva")
        print("invio attivo")

    def send_audio(self):
        while True:
            self.VarMute()
            if self.mute == "0" or self.mute == None :
                data = self.stream_rec.read(self.chunk)
                self.client_socket.sendall(data)
            

    def receive_audio(self):
        while True:
            audio_data = self.client_socket.recv(self.chunk)
            self.stream_play.write(audio_data)

    def close(self):
        # Clean up resources
        self.client_socket.close()
        self.stream_rec.stop_stream()
        self.stream_rec.close()
        self.stream_play.stop_stream()
        self.stream_play.close()
        self.audio.terminate()
    
    def VarMute(self) :
        with open(".mute", "r") as f :
            self.mute = f.read()

def main():
    # Specify the server's address and port
    server_address = '10.10.88.88' # modifier #####################
    server_port = 5555

    # Create an instance of the Client class
    client = Client(server_address, server_port)

    # Start audio threads for sending and receiving audio
    client.start_audio_threads()

    try:
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        # Close the client when KeyboardInterrupt (Ctrl+C) is detected
        client.close()

if __name__ == "__main__":
    main()
