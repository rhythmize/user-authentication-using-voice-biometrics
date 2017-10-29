from ltsd import LTSD_VAD
import numpy as np
from newvad import VoiceActivityDetector

class ActivityDetection:

    def __init__(self):
        self.initted = False
        #self.nr = NoiseReduction()
        self.ltsd = LTSD_VAD()
        self.vad = VoiceActivityDetector()

    def init_noise(self, fs, signal):
        self.initted = True
        #self.nr.init_noise(fs, signal)
        self.ltsd.init_params_by_noise(fs, signal)
        #nred = self.nr.filter(fs, signal)
        #self.ltsd.init_params_by_noise(fs, nred)

    def filter(self, fs, signal):
        if not self.initted:
            raise "NoiseFilter Not Initialized"
#        nred = self.nr.filter(fs, signal)
#        removed = remove_silence(fs, nred)
#        self.ltsd.plot_ltsd(fs, nred)
        orig_len = len(signal)
        filtered, intervals = self.ltsd.filter(signal)
        #print 'signal lengths', len(filtered), orig_len
        if len(filtered) > orig_len / 3:
            return filtered
        return np.array([])
    '''
    def newfilter(self, fs, data):
        speech = self.vad.detect_speech(fs, data)
        filtered = []
        for [start, end] in speech:
            filtered.extend(data[start:end])
        filtered = np.array(filtered)
        return filtered
    '''
    def remove_silence(self,fs, signal, frame_duration = 0.02, frame_shift = 0.01, perc = 0.15):
        orig_dtype = type(signal[0])
        siglen = len(signal)
        retsig = np.zeros(siglen, dtype = np.int64)
        frame_length = int(frame_duration * fs)
        frame_shift_length = int(frame_shift * fs)
        new_siglen = 0
        i = 0
        average_energy = np.sum(signal ** 2) / float(siglen)
        
        #print "Avg Energy of signal: ", average_energy
        while i < siglen:
            subsig = signal[i:i + frame_length]
            ave_energy = np.sum(subsig ** 2) / float(len(subsig))
            if ave_energy < average_energy * perc:
                i += frame_length
            else:
                sigaddlen = min(frame_shift_length, len(subsig))
                retsig[new_siglen:new_siglen + sigaddlen] = subsig[:sigaddlen]
                new_siglen += sigaddlen
                i += frame_shift_length
        retsig = retsig[:new_siglen]
        return retsig.astype(orig_dtype)
