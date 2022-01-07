from cv2 import *
import numpy as np

g = [0,0,0,0]
#lectura de video
vc = VideoCapture(0)
#cargar archivo HAAR cascade a un objeto clasificador
light_cascade = CascadeClassifier("cascade_xml/TrafficLight_HAAR_16Stages.xml")
stop_cascade = CascadeClassifier("cascade_xml/Stopsign_HAAR_19Stages.xml")

#deteccion de señal de alto
def detectStop():
    #detectar la señal de alto y crear una tupla con los valores x,y,w,h del objeto detectado 
    StopRect = stop_cascade.detectMultiScale(imageGray, scaleFactor=1.2, minNeighbors=3, minSize=(1,1))
    #si detecta el objeto asigna los valores de la tupla a cuatro variables y los retorna a la funcion principal
    if len(StopRect) <= 0:
        return g
    if len(StopRect)>0:
        for j,k,l,n in StopRect:
        
            return j,k,l,n
        
def detectLight():
    
    lightRect = light_cascade.detectMultiScale(imageGray, scaleFactor=1.2, minNeighbors=3, minSize=(1,1))

    if len(lightRect) <= 0:
        return g
    if len(lightRect)>0:
        for j,k,l,n in lightRect:
        
            return j,k,l,n
#funcion principal        
while True:
    next, frame = vc.read()
    result = np.copy(frame)
    imageGray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    #llama a las funciones que detecta los objetos y asigna los valores retornados a 4 variables
    x,y,w,h = detectStop()
    x1,y1,w1,h1 = detectLight()
    #crea un cuadro con las coordenadas del objeto detectado
    if h>1:
        cv2.rectangle(result,(x,y),(x+w,y+h),(0,0,255),2)
    if h1>1:
        cv2.rectangle(result,(x1,y1),(x1+w1,y1+h1),(255,0,255),2)
    imshow("webcam2", result)
    # Romper video 
    if waitKey(1) & 0xFF == ord('s'):
        break
vc.release()
destroyAllWindows()