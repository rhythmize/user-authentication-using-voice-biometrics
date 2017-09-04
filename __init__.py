import sys
import glob
import argparse
from RecordAudio import RecordAudio
from ActivityDetection import ActivityDetection
import scipy.io.wavfile as wavfile

from Main import Main

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--task',
                       help='Task to do. Either "enroll" or "predict"',
                       required=True)

    ret = parser.parse_args()
    return ret

def enroll():
    try :
        m = Main.load('02-09-2017.model')
    except :
        m = Main()
    
    #ra=RecordAudio()
    #fs, data = ra.start_record(10.0)
    '''
    fs, data = wavfile.read('system generated voice/google assistant.wav')
    m.signal = m.ad.filter(fs, data)
    m.name = 'Computer'
    if len(m.signal) > 50:
        m.getFeatures()
    else:
        print 'signal is silent'
        return
    '''
    audios = glob.glob('audio samples/*.wav')
    if len(audios) is 0:
        print "No audio file found"
        exit()
    for audio in audios:
        fs, data = wavfile.read(audio)
        #signal = ad.remove_silence(fs, signal)
        m.signal = m.ad.filter(fs, data)
        m.name = audio.split('/')[-1].split('.')[0]
        print m.name, "processing"
        #print 'signal length after silence remove', len(m.signal)
        if len(m.signal) > 50:
           features = m.getFeatures()
        else:
           print name,"signal is silent"
    print "features saved"
    
    m.train()
    m.dump()

def predict():
    try :
        m = Main.load('02-09-2017.model')
    except :
        print "Trained Model not found."
        exit()
    
    #ra=RecordAudio()
    #fs, data = ra.start_record(10.0)
    '''
    audios = glob.glob('audio test samples/*.wav')
    if len(audios) is 0:
        print "No audio file found"
        exit()
    for audio in audios:
        user = None
        fs, data = wavfile.read(audio)
        #signal = ad.remove_silence(fs, signal)
        m.signal = m.ad.filter(fs, data)
        #print 'signal length after silence remove', len(m.signal)
        name = audio.split('/')[-1].split('.')[0]
        #print len(m.signal)
        if len(m.signal) > 50:
            user = m.predict()
        print name, '-->', user
    
    '''
    fs, data = wavfile.read('test samples/Iqra mam2.wav')
    #signal = ad.remove_silence(fs, data)
    
    user = None
    m.signal = m.ad.filter(fs, data)
    #print len(m.signal)
    if len(m.signal) > 50:
        user = m.predict()
    print "Current speaker is identified as ", user
    

if __name__ == '__main__':
    global ra
    args = get_args()
    task = args.task
    if task == 'enroll':
        enroll()
    if task == 'predict':
        predict()
    
