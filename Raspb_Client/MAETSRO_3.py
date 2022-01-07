import pygame
import socket
import sys
from clase_maestro_2 import modo_autonomo
from clase_maestro_2 import modo_manual


def Modo_Autonomo(host,puerto):
     
    def comunicacion_wifi(host, puerto):
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
        
        Control_Del_Bucle = True
               
        while Control_Del_Bucle:
            
            for event in pygame.event.get():
                teclado = pygame.key.get_pressed()
                
                if teclado[pygame.K_0]:
                    rc_manual.PM_teclas(servidor,Control_Del_Bucle)
                    
                elif teclado[pygame.K_1]:
                    rc_manual.PM_volante(servidor,Control_Del_Bucle)
                                   
                elif teclado[pygame.K_2]:
                    rc_autonomo.PA(cliente)
                        
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
            

                
    comunicacion_wifi(host,puerto)

if __name__ == "__main__":
        
    host = '192.168.0.100'              
    puerto_img = 10004
    puerto_pygame = 10005
                    
    Modo_Autonomo(host,puerto_pygame)