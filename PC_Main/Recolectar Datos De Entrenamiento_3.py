import cv2
import numpy as np
import time
import queue
import base64
import zmq
import numpy as np
import pygame
import socket
import sys
import threading
from cv2 import*
import os


    
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



def Modo_Manual(host,puerto,dim_img):
    
    direccion = (host, puerto)          # Direccion IP y pùerto en el que el cliente debe conectarse para escuchar
    servidor = socket.socket()          # Descriptor para crear el socket - Se crea un socket - como los parametros estan vacios por defecto queda como un socket TCP IP
    servidor.bind(direccion)            # Asocia la direccion local (IP) con un socket
    servidor.listen(1)                  # Crea una lista de espera para almacenar solicitudes de conexion,
                                                # recordemos que wifi es half duplex, por lo cual el master gestiona a quien escucha en un determinado momento por lo cual se debe espesificar el numero de clientes, en este caso por simplicidad ponemos 1 cliente nada mas
    print("Esperando conexion")
    print()
    cliente, direccion_cliente = servidor.accept()  # Se genera un socket del cliente y se asigna una nueva direccion que pertenece al cliente(Recordemos que un cliente wifi tiene una MAC y una IP, que no son mas que el nombre que identifica al cliente)
    print(cliente, direccion_cliente)
    print("CONEXION ESTABLECIDA")
    print()
     
    pygame.init()                       # La clase o función principal que crea o ejecuta el juego
    pygame.display.set_mode((250, 250)) # Se crea y configura la ventana
    pygame.key.set_repeat(1,500)       # Sirve para leer las teclas repetidas y los parametros son el delay y las repeticones en ese delay respectivamente
    pygame.display.set_caption('Coche autónomo')
    print("MODO MANUAL")  
    print()

    x = np.empty((0,dim_img))
    y = np.empty((0,4))
               
    Control_Del_Bucle = True
    Ctrl_drv = False
    k = np.zeros((4, 4), 'float')
    
    for i in range(4):
        k[i, i] = 1
        
    saved_frame = 0
    frame = 0
    total_frame = 0
    
    
    print("Empezando recoleccion de datos...")
    print()
    print("Presionar 'q' para finalizar...")
    print()
    empezar = cv2.getTickCount()
    
    try:
    
        while Control_Del_Bucle:  # El bucle principal del juego -  En este caso se usa una interfaz para juegos para manejar el carro real (prporcionada por pygames)
        
            vector_entrada = frameg.get() # echarle un ojo
            frame += 1
            total_frame += 1
                        
            for event in pygame.event.get():  # Posibles entradas del teclado y mouse, la instruccion es una lista con todos los eventos que registra pygame
            
                teclado = pygame.key.get_pressed()  # obtener el estado de todos los botones del teclado
                                
                # Condiciones en funcion del teclado
                
                # Ordenes Mixtas
                if teclado[pygame.K_UP] and teclado[pygame.K_RIGHT]:
                    if Ctrl_drv == False:
                        Ctrl_drv = True
                    #print("Derecha y adelante")
                    mensaje = b"Desplazate hacia la derecha"
                    x = np.vstack((x,vector_entrada))
                    y = np.vstack((y,k[1]))
                    saved_frame += 1
                    cliente.send(mensaje)
                
                elif teclado[pygame.K_UP] and teclado[pygame.K_LEFT]:
                    if Ctrl_drv == False:
                        Ctrl_drv = True
                    mensaje = b"Desplazate hacia la izquierda"
                    x = np.vstack((x,vector_entrada))
                    y = np.vstack((y,k[0]))
                    saved_frame += 1
                    cliente.send(mensaje)
    
           
                elif teclado[pygame.K_DOWN] and teclado[pygame.K_LEFT]:
                    if Ctrl_drv == False:
                        Ctrl_drv = True
                    mensaje = b"Retrocede hacia la izquierda"
                    cliente.send(mensaje)
                    
                elif teclado[pygame.K_DOWN] and teclado[pygame.K_RIGHT]:
                    if Ctrl_drv == False:
                        Ctrl_drv = True
                    mensaje = b"Retrocede hacia la derecha"
                    cliente.send(mensaje)
                
                # Ordenes Simples
                elif teclado[pygame.K_UP]:
                    if Ctrl_drv == True:
                        mensaje = b'Nada'
                        cliente.send(mensaje)
                        Ctrl_drv = False
                    mensaje = b"adelante"
                    x = np.vstack((x,vector_entrada))                
                    y = np.vstack((y,k[2]))              
                    saved_frame += 1
                    cliente.send(mensaje)
                
                elif teclado[pygame.K_LEFT]:
                    if Ctrl_drv == True:
                        mensaje = b'Nada'
                        cliente.send(mensaje)
                        Ctrl_drv = False
                    mensaje = b"izquierda"
                    x = np.vstack((x,vector_entrada))
                    y = np.vstack((y,k[0]))
                    saved_frame += 1
                    cliente.send(mensaje)
              
                elif teclado[pygame.K_DOWN]:
                    if Ctrl_drv == True:
                        mensaje = b'Nada'
                        cliente.send(mensaje)
                        Ctrl_drv = False
                    mensaje = b"abajo"
                    cliente.send(mensaje)
                    
                elif teclado[pygame.K_RIGHT]:
                    if Ctrl_drv == True:
                        mensaje = b'Nada'
                        cliente.send(mensaje)
                        Ctrl_drv = False
                    mensaje = b"derecha"
                    x = np.vstack((x,vector_entrada))                
                    y = np.vstack((y,k[1]))              
                    saved_frame += 1
                    cliente.send(mensaje)
                    
                    
                elif teclado[pygame.K_f]:
                    mensaje = b"Freno"
                    x = np.vstack((x,vector_entrada))                
                    y = np.vstack((y,k[3]))              
                    saved_frame += 1
                    cliente.send(mensaje)
                    
                else:
                    mensaje = b'Nada'
                    cliente.send(mensaje)
                    
                # Orden de escape
                if teclado[pygame.K_x] or teclado[pygame.K_q]:
                    print("Se ha finalizado el modo manual")
                    print()
                    mensaje = b"El master ha finalizado la conexion"
                    cliente.send(mensaje)
                    servidor.close()
                    print("Se ha finalizado la conexion pygame Maestro")
                    print()
                    Control_Del_Bucle = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                    break    
    
    
    finally:
        
        # Guardando los datos en la carpeta 
        
        nombre_del_archivo = str(int(time.time()))
        carpeta = "datos_de_entrenamiento"
                
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            
        try:
            np.savez(carpeta + '/' + nombre_del_archivo + '.npz', train=x, train_labels=y)
            
            # Lo primero es la direccion, como hay una diagonal, esto permite que la primera direccion sea la de la carpeta y la segunda la del archivo
            # El nombre del archivoff corresponde a un instante de tiuempo pasado a texto, esto se realiza mediante la funciontime.time y el punto me denota la extension del archivo
            
#### NOTA: pienso que esta linea deberia estar dentro del while #######
            
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
        
    global frameg                               
    frameg = queue.Queue()

    host = '192.168.0.102'
    puerto_img = 10002
    puerto_pygame = 10003

    capa_de_entrada = 320*120 

    Hilo_1 =  threading.Thread(name='Recepcion_img', target= Recepcion_img,args=(host,puerto_img))
    Hilo_1.start()
    Modo_Manual(host,puerto_pygame,capa_de_entrada)
 
#Hilo_2 = threading.Thread(name='Modo_Manual', target= Modo_Manual,args=(host_2,puerto_pygame,capa_de_entrada))
#Hilo_2.start() 1
    
# print(k[1]) # Arroja una columna,(pudiera ser fila nose la realidad es que como esta eslada en forma de matriz identidad seria lo mismo si fuera una sola fila o columna). 
             # Basicamente esto agarrando el vector de salida
                       
# izquierda= [1 0 0 0]
# derecha  = [0 1 0 0]
# adelante = [0 0 1 0]
# retroceso= [0 0 0 1]


