import cv2
import numpy as np
import queue
import base64
import zmq
import pygame
import socket
import sys
import threading
from cv2 import*
from Modelo_red_neuronal import NeuralNetwork
from clase_maestro import modo_autonomo
from clase_maestro import modo_manual
import time


def Recepcion_img(host,puerto):
    context = zmq.Context()                  
    footage_socket = context.socket(zmq.SUB) 
    footage_socket.bind('tcp://'+host+':'+str(puerto)) 
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode('')) 
    print("Corriendo recepción de imágenes")
    print()
    
    while True:
        try:
            frame = footage_socket.recv_string()   # Recibiendo string
            if frame is not None:
                img = base64.b64decode(frame)   # Codificando con la libreria base64
                npimg = np.frombuffer(img, dtype=np.uint8)  # se utiliza frombuffer por la cantidad de datos sin embargo se puede usar fromstring
                source = cv2.imdecode(npimg, 1) # Para que y porque el 1???
                source2 = np.copy(source)
                img_gris = cv2.cvtColor(source2, cv2.COLOR_BGR2GRAY) 
                alto,ancho = img_gris.shape # Funcion de numpy  que arroja la forma
                img_cortada = img_gris[int(alto/2):alto, :]  # Se corta la mitad de la altura de la imagen (Valores entre la mitad y el maximo del alto, Todos los valores del ancho) - Hay que jugar con el intervalo para obtener la zona de interes
                vector_entrada = img_cortada.reshape(1, int(alto/2) * ancho).astype(np.float32) # Transformo imagen en vector)
                #cv2.imshow("COLOR", source2)
                #cv2.waitKey(1)
                cv2.imshow("gris", img_cortada)
                cv2.waitKey(1)
                frameg.put(vector_entrada)

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break


        k = cv2.waitKey(30) & 0xff
        if k == ord("s"):
            break

    cv2.destroyAllWindows()
    print('Ha finalizado la recepción de imágenes')
    print()

def Modo_Autonomo(host,puerto,modelo):
     
    def comunicacion_wifi(host, puerto,modelo):
        direccion = (host, puerto)          
        servidor = socket.socket()         
        servidor.bind(direccion)            
        servidor.listen(1)   
        print()               
        print("Esperando conexion")
        cliente, direccion_cliente = servidor.accept()  
        print(cliente, direccion_cliente)
        print("CONEXION ESTABLECIDA")
        pygame.init()                       
        pygame.display.set_mode((250, 250)) 
        pygame.key.set_repeat(1, 250)      
        pygame.display.set_caption('NIBIRU')
                       
        rc_autonomo = modo_autonomo(cliente)
        rc_manual = modo_manual(cliente)

        nn = NeuralNetwork() # Invoco al inicio de la clase que es un modelo vacio
        nn.load_model(modelo) # Y el modelo se carga en esa variable vacia

        Control_Del_Bucle = True
               
        while Control_Del_Bucle:
            
            for event in pygame.event.get():
                teclado = pygame.key.get_pressed()
                
                if teclado[pygame.K_0]:
                    rc_manual.PM_teclas(servidor,Control_Del_Bucle)
                    
                elif teclado[pygame.K_1]:
                    rc_manual.PM_volante(servidor,Control_Del_Bucle)
                                   
                elif teclado[pygame.K_2]:
                    rc_autonomo.PA(nn,servidor,frameg)
                        
                if teclado[pygame.K_x]:
                    print("Se ha finalizado el modo manual")
                    mensaje = b"El master ha finalizado la conexion"
                    cliente.send(mensaje)
                    servidor.close()
                    print("Se ha finalizado la conexion pygame Maestro")
                    Control_Del_Bucle = False
                    pygame.joystick.quit
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                    break
            

                
    comunicacion_wifi(host,puerto,modelo)

if __name__ == "__main__":
        
    global frameg                                                
    frameg = queue.Queue()

    host = '192.168.0.100'              
    puerto_img = 10004
    puerto_pygame = 10005
    
    modelo = "guardar_modelo/red_neuronal_curva_S_rapido.xml"
    
    # Se fonfigura el hilo    
    Hilo_1 =  threading.Thread(name='Recepcion_img', target= Recepcion_img,args=(host,puerto_img))
    Hilo_1.start()                    
    Modo_Autonomo(host,puerto_pygame,modelo)