import pyaudio
import time
import numpy as np
import scipy.io.wavfile as wavfile

FORMAT=pyaudio.paInt16
NPDtype = 'int16'
FS=8000

class RecorderThread():
    def __init__(self, main):
        self.main = main

    def run(self, end_time):
        self.start_time = time.time()
        while(time.time()-self.start_time <= end_time):
            data = self.main.stream.read(1)
            i = ord(data[0]) + 256 * ord(data[1])
            if i > 32768:							# permissible 16 bit audio data value is -32768 to 32767
                i -= 65536
            self.main.recordData.append(i)

class RecordAudio:
    def __init__(self):
        self.reco = RecorderThread(self)
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(format=FORMAT, channels=1, rate=FS,
                        input=True, frames_per_buffer=1)
        self.recordData = []
        
    def start_record(self, time):
        print("Recording...")
        
        self.reco.run(time)
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
        print("Done Recording...")
        data = np.array(self.recordData, dtype=NPDtype)
        wavfile.write('myaudio.wav', FS, data)
        return FS, data

