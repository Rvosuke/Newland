import cv2
import time
import ipywidgets as widgets
from IPython.display import display
from lib.faceDetect import NLFaceDetect

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, image = cap.read()
time.sleep(2)

imgbox = widgets.Image(format='jpeg')
display(imgbox)
imgbox.value = cv2.imencode('.jpeg', image)[1].tobytes()

cap.release()

libNamePath = 'lib/libNLFaceDetect.so'
nlFaceDetect = NLFaceDetect(libNamePath=libNamePath)

configPath = b"/usr/local/lib/rk3399_AI_model"
nlFaceDetect.NL_FD_ComInit(configPath)

