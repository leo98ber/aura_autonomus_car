import cv2
import zmq
import base64
import numpy as np
import pygame
import socket
import threading
import serial
import sys
import time
from cv2 import *
import pickle
from clase_cliente import modo_cliente

def Envio_img(host, puerto):

    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.connect('tcp://'+host+':'+str(puerto))
    print("Conectado")
    #deteccion de señal de alto
    def detectStop():
        #detectar la señal de alto y crear una tupla con los valores x,y,w,h del objeto detectado 
        StopRect = stop_cascade.detectMultiScale(imageGray, scaleFactor=1.3, minNeighbors=3, minSize=(1,1))
        #si detecta el objeto asigna los valores de la tupla a cuatro variables y los retorna a la funcion principal
        StopRect2 = np.copy(StopRect)
        if len(StopRect2) <= 0:
            return g
        if len(StopRect2)>0:
            return StopRect2[0]
            
    def detectLight():
        lightRect = light_cascade.detectMultiScale(imageGray, scaleFactor=1.3, minNeighbors=3, minSize=(1,1))
        lightRect2 = np.copy(lightRect)
        if len(lightRect2) <= 0:
            return g
        if len(lightRect2)>0:
            return lightRect2[0]
    while True:
        cap = cv2.VideoCapture(0)
        start = time.time()
        control = True
        
        while control:
            try:
                grabbed, frame = cap.read()
                frame = cv2.resize(frame, (320,240))
                frame2 = np.copy(frame)
                #Transformo a escala de grises para procesar y definir los cuadros, y luego esos cuadros se introducen en la imagen a color
                imageGray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) 
                #llama a las funciones que detecta los objetos y asigna los valores retornados a 4 variables
                x,y,w,h = detectStop()  # la funcion devuelve parametros que se usan mas adelante
                x1,y1,w1,h1 = detectLight()
                #crea un cuadro con las coordenadas del objeto detectado
                cv2.rectangle(frame2,(x,y),(x+w,y+h),(0,0,255),2) # Con los parametros dados se construye el rectangulo
                cv2.putText(frame2,'Alto',(x+20,y-10),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),lineType=cv2.LINE_AA)
                cv2.rectangle(frame2,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
                cv2.putText(frame2,'semaforo rojo',(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,5,0),lineType=cv2.LINE_AA)
                encoded, buffer = cv2.imencode('.jpg', frame2) # Convierto en formato jpg
                jpg_as_text = base64.b64encode(buffer) # Que mando??
                footage_socket.send(jpg_as_text)
                if time.time() - start > 10: 
                    break
                

            except KeyboardInterrupt:
                cap.release()
                cv2.destroyAllWindows()
                break

            k = cv2.waitKey(30) & 0xff
            if k == ord("s"):
                break
        cap.release()
        cv2.destroyAllWindows()


def modo_manual_cliente(host, puerto):

    cliente = socket.socket()
    direccion_cliente = (host, puerto)
    cliente.connect(direccion_cliente)
    puerto_serial = "/dev/ttyACM0"
    empezar = time.time()
    ctrl_bucle = True
    Ctrl_drv = False
    Cliente = modo_cliente(puerto_serial,cliente) 
    
    while ctrl_bucle:
            
        Recepcion_Mensaje = cliente.recv(32768)
            
        if Recepcion_Mensaje == b'TECLAS':
            print("Inicio de teclas")
            Cliente.teclas(ctrl_bucle)            
                
        elif Recepcion_Mensaje == b'VOLANTE':
            print("Inicio de teclas")
            Cliente.volante(Ctrl_drv,ctrl_bucle,empezar)
                    
        # Orden de finalizacion 
                
        if Recepcion_Mensaje == b'El master ha finalizado la conexion':
            print(Recepcion_Mensaje)
            ctrl_bucle = False
            print("Se ha finalizado la conexion")
            cliente.close()  
            sys.exit()
            break

if __name__ == "__main__":
    
    host = '192.168.0.100'
    puerto_img = 10004
    puerto_pygame = 10005

    g = [0,0,0,0]
    #cargar archivo HAAR cascade a un objeto clasificador
    light_cascade = CascadeClassifier("cascade_xml/TrafficLight_HAAR_16Stages.xml")
    stop_cascade = CascadeClassifier("cascade_xml/Stopsign_HAAR_19_Stages.xml")

    Hilo1 = threading.Thread(name= 'Hilo_img', target= Envio_img,args=(host, puerto_img))
    Hilo2 = threading.Thread(name='Hilo_modo_manual', target= modo_manual_cliente,args=(host, puerto_pygame))
    Hilo1.start()
    Hilo2.start()