import sys
import glob
import argparse
from RecordAudio import RecordAudio
from ActivityDetection import ActivityDetection
from UI import UI
import scipy.io.wavfile as wavfile
import traceback as tb
import numpy as np
from gmmset import GMM

from PyQt4.QtGui import *
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
        m = Main.load('test.gmm')
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
           #np.savetxt('data/mfcc-lpc-data/'+m.name+'.mfcc-lpc', features)
        else:
           print name,"signal is silent"
    print "features saved"

	# train UBM Model prior to GMM Model    
	#m.train_ubm()
    m.train()
    m.dump()

def predict():
    try :
        m = Main.load('test.gmm')
    except Exception as e:
        print tb.format_exc()
        exit()
    #ra=RecordAudio()
    #fs, data = ra.start_record(10.0)
    
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
        
        if len(m.signal) > 50:
            try :
                user = m.predict()
            except Exception as e :
                print tb.format_exc()
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
    '''

if __name__ == '__main__':
    '''
    app = QApplication(sys.argv)
    ui=UI()
    ui.show()
    sys.exit(app.exec_())
    '''
    global ra
    args = get_args()
    task = args.task
    if task == 'enroll':
        enroll()
    if task == 'predict':
        predict()
    
