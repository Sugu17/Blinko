import sounddevice,soundfile

def play(filename):
    data,sampling_rate=soundfile.read(filename,dtype='float32')
    sounddevice.play(data,sampling_rate)
    status=sounddevice.wait()

play("Left_immedaite.wav")
