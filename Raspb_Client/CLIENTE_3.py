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
import queue
from clase_cliente_2 import modo_cliente_manual
from clase_cliente_2 import modo_autonomo
from Modelo_red_neuronal import NeuralNetwork

def Envio_img(host, puerto):

    #context = zmq.Context()
    #footage_socket = context.socket(zmq.PUB)
    #footage_socket.connect('tcp://'+host+':'+str(puerto))
    #print("Conectado")
    
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
                imageGray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) 
                alto,ancho = imageGray.shape # Funcion de numpy  que arroja la forma
                img_cortada = imageGray[int(alto/2):alto, :]  # Se corta la mitad de la altura de la imagen (Valores entre la mitad y el maximo del alto, Todos los valores del ancho) - Hay que jugar con el intervalo para obtener la zona de interes
                vector_entrada = img_cortada.reshape(1, int(alto/2) * ancho).astype(np.float32) # Transformo imagen en vector)
                cv2.imshow("gris", img_cortada)
                cv2.waitKey(1)
                frameg.put(vector_entrada)       
                #llama a las funciones que detecta los objetos y asigna los valores retornados a 4 variables
                x,y,w,h = detectStop()  # la funcion devuelve parametros que se usan mas adelante
                x1,y1,w1,h1 = detectLight()
                #crea un cuadro con las coordenadas del objeto detectado
                cv2.rectangle(frame2,(x,y),(x+w,y+h),(0,0,255),2) # Con los parametros dados se construye el rectangulo
                cv2.putText(frame2,'Alto',(x+20,y-10),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),lineType=cv2.LINE_AA)
                cv2.rectangle(frame2,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
                cv2.putText(frame2,'semaforo rojo',(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,5,0),lineType=cv2.LINE_AA)
                cv2.imshow("COLOR", frame2)
                cv2.waitKey(1) 
                
                #encoded, buffer = cv2.imencode('.jpg', frame2) # Convierto en formato jpg
                #jpg_as_text = base64.b64encode(buffer) # Que mando??
                #footage_socket.send(jpg_as_text)
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


def modo_manual_cliente(host,puerto,modelo):

    cliente = socket.socket()
    direccion_cliente = (host, puerto)
    cliente.connect(direccion_cliente)
    
    nn = NeuralNetwork() # Invoco al inicio de la clase que es un modelo vacio
    nn.load_model(modelo) # Y el modelo se carga en esa variable vacia
    print("Modelo cargado")
    
    puerto_serial = "/dev/ttyACM0"
    
    rc_autonomo = modo_autonomo(cliente)


    empezar = time.time()
    ctrl_bucle = True
    Ctrl_drv = False
    Cliente = modo_cliente_manual(puerto_serial,cliente) 
        
    while ctrl_bucle:
            
        Recepcion_Mensaje = cliente.recv(32768)
            
        if Recepcion_Mensaje == b'TECLAS':
            print("Inicio de teclas")
            Cliente.teclas(ctrl_bucle)            
                
        elif Recepcion_Mensaje == b'VOLANTE':
            print("Inicio de teclas")
            Cliente.volante(Ctrl_drv,ctrl_bucle,empezar)
                
        elif Recepcion_Mensaje == b'AUTONOMO':
            print("Inicio del modo autonomo")
            rc_autonomo.PA(nn,frameg,puerto_serial)
                    
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
    
    global frameg                                                
    frameg = queue.Queue()
    
    modelo = "guardar_modelo/red_neuronal_curva_S_rapido.xml"

    g = [0,0,0,0]
    #cargar archivo HAAR cascade a un objeto clasificador
    light_cascade = CascadeClassifier("cascade_xml/TrafficLight_HAAR_16Stages.xml")
    stop_cascade = CascadeClassifier("cascade_xml/Stopsign_HAAR_19_Stages.xml")

    Hilo1 = threading.Thread(name= 'Hilo_img', target= Envio_img,args=(host, puerto_img))
    Hilo2 = threading.Thread(name='Hilo_modo_manual', target= modo_manual_cliente,args=(host, puerto_pygame,modelo))
    Hilo1.start()
    Hilo2.start()