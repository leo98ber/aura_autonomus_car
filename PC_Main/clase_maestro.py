import pygame
import pickle
import numpy as np
import time
from clase_conductor import conductor



class modo_autonomo(object):
    
    def __init__(self,cliente):
        
        self.cliente = cliente
        
    def PA(self,nn,servidor,frameg):
                
        mensaje = b"TECLAS"
        self.cliente.send(mensaje)  
        conduccion = conductor(self.cliente)
        print("MODO AUTONOMO")
        C = True
        
        while C:

            vector_entrada = frameg.get()
            prediccion = nn.predict(vector_entrada)
            conduccion.decision(prediccion)
        
            for event in pygame.event.get():  
        
                teclado = pygame.key.get_pressed()
            
                if teclado[pygame.K_x] or teclado[pygame.K_q]:
                    conduccion.stop()
                    time.sleep(0.2)
                    mensaje = b"fin del teclado"
                    self.cliente.send(mensaje)
                    print("Se ha finalizado el modo autonomo")
                    C = False
                    break
                
                
class modo_manual(object):
    
    def __init__(self,cliente):
        
        self.cliente = cliente
        
    def PM_teclas(self,servidor,C):
        
        mensaje = b"TECLAS"
        self.cliente.send(mensaje)  
        print("MODO MANUAL TECLAS")
        
        while C:         
            
            for event in pygame.event.get():
                teclado = pygame.key.get_pressed()
                    
                # Ordenes Mixtas
                if teclado[pygame.K_UP] and teclado[pygame.K_RIGHT]:
                    mensaje = b"Desplazate hacia la derecha"
                    self.cliente.send(mensaje)
        
                elif teclado[pygame.K_UP] and teclado[pygame.K_LEFT]:
                    mensaje = b"Desplazate hacia la izquierda"
                    self.cliente.send(mensaje)
        
                elif teclado[pygame.K_DOWN] and teclado[pygame.K_LEFT]:
                    mensaje = b"Retrocede hacia la izquierda"
                    self.cliente.send(mensaje)
        
                elif teclado[pygame.K_DOWN] and teclado[pygame.K_RIGHT]:
                    mensaje = b"Retrocede hacia la derecha"
                    self.cliente.send(mensaje)
                
                # Ordenes Simples
                elif teclado[pygame.K_UP]:
                    mensaje = b"adelante"
                    self.cliente.send(mensaje)
                elif teclado[pygame.K_LEFT]:
                    mensaje = b"izquierda"
                    self.cliente.send(mensaje)
                elif teclado[pygame.K_DOWN]:
                    mensaje = b"abajo"
                    self.cliente.send(mensaje)
                elif teclado[pygame.K_RIGHT]:
                    mensaje = b"derecha"
                    self.cliente.send(mensaje)
        
                # Freno
                elif teclado[pygame.K_f]:
                    mensaje = b"Freno"
                    self.cliente.send(mensaje)
                            
                else:
                    mensaje = b'Nada'
                    self.cliente.send(mensaje)
        
                # Orden de escape
                if teclado[pygame.K_q]:
                    mensaje = b'Nada'
                    self.cliente.send(mensaje)
                    time.sleep(0.1)
                    mensaje = b"fin del teclado"
                    self.cliente.send(mensaje)
                    print("Se ha finalizado el modo manual teclas")
                    C = False
                    break
                
    def PM_volante(self,servidor,C):
        
        
        mensaje = b"VOLANTE"
        self.cliente.send(mensaje) 
        print("MODO MANUAL VOLANTE")
        
        numero_de_joysticks = pygame.joystick.get_count() # Contamos el numero de joysticks
        print(numero_de_joysticks)
    
        if numero_de_joysticks == 0: 
            print("No hay control")
        else: 
            control =  pygame.joystick.Joystick(0) 
            control.init()                         
            print("Control iniciado")

        y_coord = 0
        x_coord = 0
        C = True
        
        while C:

            
            if numero_de_joysticks != 0:
                
                horiz_axis_pos = control.get_axis(0)
                vert_axis_pos = control.get_axis(1)   
                                        
                x_coord = int(horiz_axis_pos * 10)                    
                y_coord = int(vert_axis_pos * -10)                       
                matriz = np.array([(x_coord),(y_coord)])
                datos = pickle.dumps(matriz)
                time.sleep(0.15)
                self.cliente.send(datos)   
                
            for event in pygame.event.get():
                teclado = pygame.key.get_pressed()
                
                # Orden de escape
                if teclado[pygame.K_q]:
                    matriz = np.array([0,0])
                    datos = pickle.dumps(matriz)
                    time.sleep(0.15)
                    self.cliente.send(datos)                      
                    mensaje = b"fin del volante"
                    self.cliente.send(mensaje)
                    print("Se ha finalizado el modo manual volante")
                    C = False
                    break