import os
import time
import pyaudio
import numpy as np
from Main import Main
from scipy.io import wavfile
import traceback as tb

from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class RecorderThread(QThread):
    def __init__(self, ui):
        QThread.__init__(self)
        self.ui = ui

    def run(self):
        self.start_time = time.time()
        while True:
            data = self.ui.stream.read(1)
            i = ord(data[0]) + 256 * ord(data[1])
            if i > 32768:
                i -= 65536
            self.ui.recordData.append(i)
            if self.ui.stopped:
                break

class UI(QMainWindow):
    
    CONV_INTERVAL = 0.4
    CONV_DURATION = 1.5
    CONV_FILTER_DURATION = CONV_DURATION
    TEST_DURATION = 3

    def __init__(self, parent=None):
               
        QWidget.__init__(self, parent)
        uic.loadUi("new.ui", self)
        
        try :
            self.main = Main.load('02-09-2017.model')
        except :
            self.main = Main()

        self.task = None
        self.recordData = []

        self.statusBar()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_callback)

        self.Startrecord.clicked.connect(self.startenrollrecord)
        self.Stoprecord.clicked.connect(self.stopenrollrecord)
        self.Choosefile.clicked.connect(self.chooseenrollfile)
        
        self.Register.clicked.connect(self.register)
        self.Clear.clicked.connect(self.clear)
        self.Exit.clicked.connect(self.exit)

        self.Startrecordreco.clicked.connect(self.startrecorecord)
        self.Stoprecordreco.clicked.connect(self.stoprecorecord)
        self.Choosefilereco.clicked.connect(self.chooserecofile)

        self.Startrecordconv.clicked.connect(self.startconvrecord)
        self.Stoprecordconv.clicked.connect(self.stopconvrecord)
        self.Exitconv.clicked.connect(self.exit)
        self.Clearconv.clicked.connect(self.clear)
        
        fs, signal = wavfile.read('background earphone.wav')
        self.main.ad.init_noise(fs, signal)

    def timer_callback(self):
        self.record_time += 1
        #self.status("Recording..." + time_str(self.record_time))
        minutes = int(self.record_time / 60)
        sec = int(self.record_time % 60)
        s = "{:02d}:{:02d}".format(minutes, sec)
        #s = time_str(self.record_time)
        ''' Instead of updating all the timers try updating only the required one'''
        if self.task == 'enroll' :
            self.Recordtime.setText(s)
        elif self.task == 'recognise':
            self.Recordtimereco.setText(s)
        elif self.task == 'conversation':
            self.Recordtimeconv.setText(s)

    def startrecord(self):
        self.statusBar().showMessage("Recording...")
        self.pyaudio = pyaudio.PyAudio()
        
        self.recordData = []
        self.stream = self.pyaudio.open(format=self.main.FORMAT, channels=1, rate=self.main.FS,
                        input=True, frames_per_buffer=1)
        self.stopped = False
        self.reco_th = RecorderThread(self)
        self.reco_th.start()

        self.timer.start(1000)
        self.record_time = 0
        
    def stoprecord(self):
        self.stopped = True
        self.reco_th.wait()
        self.timer.stop()
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
        self.statusBar().showMessage("Recording Stopped.")
        self.recordData = np.array(self.recordData, dtype=self.main.NPDtype)
        wavfile.write('myaudio.wav', self.main.FS, self.recordData)

    def startenrollrecord(self):
        self.task = 'enroll'
        self.main.name = str(self.Username.text().trimmed())
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter your name first.")
            self.statusBar().showMessage('')
        elif self.main.name == 'Unknown':
            QMessageBox.warning(self, "Warning", "Please enter a valid name.")
            self.statusBar().showMessage('')
        else:
            self.startrecord()
        
    def stopenrollrecord(self):
        self.stoprecord()
        ''' remove silence here and wait for regitser button click for further'''
        self.main.name = str(self.Username.text().trimmed())
        self.main.signal = self.main.ad.filter(self.main.FS, self.recordData)
        wavfile.write('silence removed.wav', self.main.FS, self.main.signal) 
        if len(self.main.signal) > 50:
            self.main.getFeatures()
        else :
            QMessageBox.warning(self, "Warning", "Audio was silent.Try Again.")
        #print "features extracted"
        
    def chooseenrollfile(self):
        self.main.name = str(self.Username.text().trimmed())
        if not self.main.name:
            QMessageBox.warning(self, "Warning", "Please enter your name first.")
            self.statusBar().showMessage('')
        elif self.main.name == 'Unknown':
            QMessageBox.warning(self, "Warning", "Please enter a valid name.")
            self.statusBar().showMessage('')
        else:
            fname = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Files (*.wav)")
            if not fname:
                return
            
            self.statusBar().showMessage('Loaded '+ fname)
            self.Filename.setText(fname)
            ''' remove silence here and wait for register button click for further '''
            self.main.FS, self.recordData = wavfile.read(fname)
            self.main.signal = self.main.ad.filter(self.main.FS, self.recordData)
            self.main.getFeatures()
            #print "features extracted"

    def startrecorecord(self):
        self.task = 'recognise'
        self.startrecord()
        
    def stoprecorecord(self):
        self.stoprecord()
        user = None
        ''' remove silence and proceed with recognition here only'''
        self.main.signal = self.main.ad.filter(self.main.FS, self.recordData)
        if len(self.main.signal) > 50:
            user = self.main.predict()
        self.IdentifiedUser.setText(user)

    def chooserecofile(self):
        self.IdentifiedUser.setText('Unknown')
        fname = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Files (*.wav)")
        if not fname:
            return
        user = None
        self.statusBar().showMessage('Loaded '+ fname)
        self.Filenamereco.setText(fname)
        ''' remove silence and extract features '''
        self.main.FS, self.recordData = wavfile.read(fname)
        self.main.signal = self.main.ad.filter(self.main.FS, self.recordData)
        if len(self.main.signal) > 50:
            user = self.main.predict()
        self.IdentifiedUser.setText(user)
        self.statusBar().showMessage('')

    def startconvrecord(self):
        self.task = 'conversation'
        self.conv_result_list = []
        self.startrecord()
        self.conv_now_pos = 0
        self.conv_timer = QTimer(self)
        self.conv_timer.timeout.connect(self.do_conversation)
        self.conv_timer.start(self.CONV_INTERVAL * 1000)

    def stopconvrecord(self):
        self.statusBar().showMessage("Recording Stopped.")
        self.stoprecord()
        self.conv_timer.stop()
    
    def do_conversation(self):
        interval_len = int(self.CONV_INTERVAL * self.main.FS)
        segment_len = int(self.CONV_DURATION * self.main.FS)
        self.conv_now_pos += interval_len
        to_filter = self.recordData[max([self.conv_now_pos - segment_len, 0]):
                                   self.conv_now_pos]
        signal = np.array(to_filter, dtype=self.main.NPDtype)
        label = None
        print label, "in do_conversation"
        '''
        try:
            signal = self.backend.filter(self.main.FS, signal)
            if len(signal) > 50:
                label = self.backend.predict(self.main.FS, signal, True)
        except Exception as e:
            print tb.format_exc()
            print str(e)
        '''
        try:
            self.main.signal = self.main.ad.filter(self.main.FS, signal)
            if len(self.main.signal) > 50:
                 label = self.main.predict()
        except Exception as e:
            print tb.format_exc()
            print str(e)

        global last_label_to_show
        label_to_show = label
        if label and self.conv_result_list:
            last_label = self.conv_result_list[-1]
            if last_label and last_label != label:
                label_to_show = last_label_to_show
        self.conv_result_list.append(label)

        print label_to_show, "label to show"
        last_label_to_show = label_to_show
        
        #ADD FOR GRAPH
        if label_to_show is None:
            label_to_show = 'Nobody'
        '''
        if len(NAMELIST) and NAMELIST[-1] != label_to_show:
            NAMELIST.append(label_to_show)
        '''
        self.IdentifiedConvUser.setText(label_to_show)
        
    def register(self):
        if not self.Username.text().trimmed():
            QMessageBox.warning(self, "Warning", "Please enter your name.")
        elif len(self.main.signal) == 0:
            QMessageBox.warning(self, "Warning", "Input signal is silent. Try again.")
        else:
            self.statusBar().showMessage('Registration started...')
            self.main.train()
            self.main.dump()
            self.statusBar().showMessage('Registration complete.')

    def clear(self):
        self.Username.setText("")
        self.Filenamereco.setText("")
        self.Filename.setText("")
        self.Recordtime.setText("00:00")
        self.Recordtimereco.setText("00:00")
        self.Recordtimeconv.setText("00:00")
        self.main.FS = 8000
        self.main.signal = []
        self.statusBar().showMessage('')
        self.recordData = []
        self.IdentifiedUser.setText("Unknown")
        self.IdentifiedConvUser.setText("Unknown")

    def exit(self):
        self.close();

