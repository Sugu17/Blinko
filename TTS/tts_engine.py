from fileinput import filename
import requests
import sounddevice,soundfile
import sys,os

class TTSEngine:
    def __init__(self,text) -> None:
        self.filename="temp.wav"
        self.url=f"http://[::1]:5002/api/tts?text={text}"
        self.request()


    def request(self):
        r=requests.get(self.url)
        with open(self.filename,'wb') as file:
            file.write(r.content)
    
    def play(self):
        data,sampling_rate=soundfile.read(self.filename,dtype='float32')
        sounddevice.play(data,sampling_rate)
        status=sounddevice.wait()
        os.remove(self.filename)

if __name__ == "__main__":
    text=""
    engine=TTSEngine(text)
    engine.play()
    sys.exit()


