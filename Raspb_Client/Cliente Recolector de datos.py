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
import queue
import os

def Envio_img(dimension):

    while True:
        cap = cv2.VideoCapture(0)
        start = time.time()
        control = True
        
        while control:
            try:
                grabbed, frame = cap.read()
                frame = cv2.resize(frame, (dimension))
                frame2 = np.copy(frame)
                imageGray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) 
                alto,ancho = imageGray.shape # Funcion de numpy  que arroja la forma
                img_cortada = imageGray[int(alto/2):alto, :]  # Se corta la mitad de la altura de la imagen (Valores entre la mitad y el maximo del alto, Todos los valores del ancho) - Hay que jugar con el intervalo para obtener la zona de interes
                vector_entrada = img_cortada.reshape(1, int(alto/2) * ancho).astype(np.float32) # Transformo imagen en vector)
                cv2.imshow("gris", img_cortada)
                cv2.waitKey(1)
                frameg.put(vector_entrada)                

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


def modo_manual_cliente(host, puerto,dim_img):

    cliente = socket.socket()
    direccion_cliente = (host, puerto)
    cliente.connect(direccion_cliente)
    ser = serial.Serial("/dev/ttyACM0", 9600)
    ctrl_bucle = True

    x = np.empty((0,dim_img))
    y = np.empty((0,4))

    k = np.zeros((4, 4), 'float')
    
    for i in range(4):
        k[i, i] = 1
        
    saved_frame = 0
    frame = 0
    total_frame = 0
    
    empezar = cv2.getTickCount()
        
    try:

        while ctrl_bucle:
            
            vector_entrada = frameg.get() 
            frame += 1
            total_frame += 1

            Recepcion_Mensaje = cliente.recv(1024)
            print(Recepcion_Mensaje)

            #Ordenes simples

            if Recepcion_Mensaje == b'derecha':
                x = np.vstack((x,vector_entrada))                
                y = np.vstack((y,k[1]))              
                saved_frame += 1
                ser.write('D'.encode('utf-8'))

            elif Recepcion_Mensaje == b'izquierda':
                x = np.vstack((x,vector_entrada))
                y = np.vstack((y,k[0]))
                saved_frame += 1
                ser.write('A'.encode('utf-8'))

            elif Recepcion_Mensaje == b'adelante':
                x = np.vstack((x,vector_entrada))                
                y = np.vstack((y,k[2]))              
                saved_frame += 1
                ser.write('W'.encode('utf-8'))

            elif Recepcion_Mensaje == b'abajo':
                ser.write('S'.encode('utf-8'))

            # Ordenes mixtas

            elif Recepcion_Mensaje == b'Desplazate hacia la derecha':
                x = np.vstack((x,vector_entrada))
                y = np.vstack((y,k[1]))
                saved_frame += 1
                ser.write('E'.encode('utf-8'))

            elif Recepcion_Mensaje == b'Desplazate hacia la izquierda':
                x = np.vstack((x,vector_entrada))
                y = np.vstack((y,k[0]))
                saved_frame += 1
                ser.write('Q'.encode('utf-8'))

            elif Recepcion_Mensaje == b'Retrocede hacia la izquierda':
                ser.write('Z'.encode('utf-8'))
                
            elif Recepcion_Mensaje == b'Retrocede hacia la derecha':
                ser.write('C'.encode('utf-8'))

            # Freno

            elif Recepcion_Mensaje == b'Freno':
                x = np.vstack((x,vector_entrada))                
                y = np.vstack((y,k[3]))              
                saved_frame += 1
                ser.write('X'.encode('utf-8'))
               
            elif Recepcion_Mensaje == b'Nada':
                ser.write('P'.encode('utf-8'))
                
            print(y.shape)

            # Orden de finalizacion
            if Recepcion_Mensaje == b'El master ha finalizado la conexion':
                ctrl_bucle = False
                print("Se ha finalizado la conexion")
                cliente.close()
                sys.exit()
                # ser.write(chr(0).encode())
                # ser.close()


    finally:
        
        # Guardando los datos en la carpeta 
        
        nombre_del_archivo = str(int(time.time()))
        carpeta = "datos_de_entrenamiento"
                
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            
        try:
            np.savez(carpeta + '/' + nombre_del_archivo + '.npz', train=x, train_labels=y)

            
        except IOError as e:
            print(e)         
                
        terminar = cv2.getTickCount()
        
        # Calculo de la duracion de transmision
        print("Duracion de Transmision: , %.2fs" % ((terminar - empezar) / cv2.getTickFrequency()))
    
        print(x.shape)
        print(y.shape)
        print()
        print("Total frame: ", total_frame)
        print("Saved frame: ", saved_frame)
        print("Dropped frame: ", total_frame - saved_frame)                





if __name__ == "__main__":
    
    host = '192.168.0.100'
    puerto_pygame = 10003
    
    resolucion = 320*240
    capa_de_entrada = 320*120 
    
    global frameg                               
    frameg = queue.Queue()

    g = [0,0,0,0]
    #cargar archivo HAAR cascade a un objeto clasificador
    light_cascade = CascadeClassifier("cascade_xml/TrafficLight_HAAR_16Stages.xml")
    stop_cascade = CascadeClassifier("cascade_xml/Stopsign_HAAR_19_Stages.xml")

    Hilo1 = threading.Thread(name= 'Hilo_img', target= Envio_img,args=(resolucion))
    Hilo2 = threading.Thread(name='Hilo_modo_manual', target= modo_manual_cliente,args=(host, puerto_pygame,capa_de_entrada))
    Hilo1.start()
    Hilo2.start()