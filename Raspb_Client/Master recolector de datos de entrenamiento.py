import pygame
import socket
import sys
from cv2 import*



def Modo_Manual(host,puerto):
    
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
    print("RECOLECCION DE DATOS")  
    print()

    Control_Del_Bucle = True
    Ctrl_drv = False
  
    print("Empezando recoleccion de datos...")
    print()
    print("Presionar 'q' para finalizar...")
    print()
    
    while Control_Del_Bucle:  # El bucle principal del juego -  En este caso se usa una interfaz para juegos para manejar el carro real (prporcionada por pygames)
                        
        for event in pygame.event.get():  # Posibles entradas del teclado y mouse, la instruccion es una lista con todos los eventos que registra pygame
            
            teclado = pygame.key.get_pressed()  # obtener el estado de todos los botones del teclado
                
            # Ordenes Mixtas
            if teclado[pygame.K_UP] and teclado[pygame.K_RIGHT]:
                if Ctrl_drv == False:
                    Ctrl_drv = True
                #print("Derecha y adelante")
                mensaje = b"Desplazate hacia la derecha"
                cliente.send(mensaje)
                
            elif teclado[pygame.K_UP] and teclado[pygame.K_LEFT]:
                if Ctrl_drv == False:
                    Ctrl_drv = True
                mensaje = b"Desplazate hacia la izquierda"
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
                cliente.send(mensaje)
                
            elif teclado[pygame.K_LEFT]:
                if Ctrl_drv == True:
                    mensaje = b'Nada'
                    cliente.send(mensaje)
                    Ctrl_drv = False
                mensaje = b"izquierda"
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
                cliente.send(mensaje)
                           
            elif teclado[pygame.K_f]:
                mensaje = b"Freno"
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
        
        
if __name__ == "__main__":
        
    host = '192.168.0.100'
    puerto_img = 10002
    puerto_pygame = 10003
    
    Modo_Manual(host,puerto_pygame)
 


