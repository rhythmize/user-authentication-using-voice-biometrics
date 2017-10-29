# user-authentication-using-voice-biometrics
Project involving Voice Signal Processing of users to recognise them using Voice Biometrics

scikit-learn
scikits.talkbox
pyssp
PyQt4
PyAudio
Python bindings for bob
	
In order to use `fast-gmm` instead of `sklearn.mixture.GaussianMixture` :
  run `make -C gmm/` in terminal to configure your system for fast-gmm
  
In order to run the application in command line :
    Train:
          python __init__.py -t enroll
    Prediction:
          python __init__.py -t predict
    
NOTE : Put all the wavfiles in the directory mentioned in the __init__.py file (for both training and prediction) and can be modifies accordingly.
