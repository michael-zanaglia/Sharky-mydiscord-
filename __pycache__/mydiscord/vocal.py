import pyaudio
import threading
import socket

class Vocal() :
    
    def __init__(self) :
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connect = ('10.10.85.129', 9531)
        self.audio = pyaudio.PyAudio()
        self.chunck = 1024*4
        
    def receive_audio(self) :
        recv_audio = self.audio.open(
            format=pyaudio.paInt16,
            output=True,
            channels=2,
            rate=48000,
            frames_per_buffer=self.chunck
        )
        recv_audio.start_stream()
        while True :
            try :
                data, addr = self.s.recvfrom(8192*4)
                recv_audio.write(data)
            except OSError as e:
                print(f"error : {e}")

    
    
    def send_audio(self) :
        ip = socket.gethostbyname(socket.gethostname())
        send_audio = self.audio.open(
            format=pyaudio.paInt16,
            input=True,
            channels=2,
            rate=48000,
            frames_per_buffer=self.chunck
        )
        send_audio.start_stream()
        while True :
            data = send_audio.read(self.chunck)
            self.s.sendto(data, self.connect)

if __name__ == '__main__' :
    ip = socket.gethostbyname(socket.gethostname())
    lock = threading.Lock()
    #s.bind(("192.168.245.1", 9531))
    voc = Vocal()
    with lock :
        send_thread = threading.Thread(target=voc.send_audio)
        recv_thread = threading.Thread(target=voc.receive_audio)
        
        send_thread.start()
        recv_thread.start() 
        
    