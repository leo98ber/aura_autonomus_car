import serial
import pickle

class modo_cliente(object):
                
    def __init__(self,puerto_serial,cliente):
        self.ser = serial.Serial(puerto_serial, 115200,timeout=1)
        self.cliente = cliente
        
    def teclas(self,ctrl_bucle):
        
        while ctrl_bucle:
            
            Recepcion_Mensaje = self.cliente.recv(32768)
            
            #Ordenes simples
            if Recepcion_Mensaje == b'derecha':
                self.ser.write('D'.encode('utf-8'))
                #print("D")
            
            elif Recepcion_Mensaje == b'izquierda':
                self.ser.write('A'.encode('utf-8'))
                #print("I")
            
            elif Recepcion_Mensaje == b'adelante':
                self.ser.write('W'.encode('utf-8'))
                #print("A")
                    
            elif Recepcion_Mensaje == b'abajo':
                self.ser.write('S'.encode('utf-8'))
                #print("R")
            
                # Ordenes mixtas
            
            elif Recepcion_Mensaje == b'Desplazate hacia la derecha':
                self.ser.write('E'.encode('utf-8'))
                #print("AD")
            
            elif Recepcion_Mensaje == b'Desplazate hacia la izquierda':
                self.ser.write('Q'.encode('utf-8'))
                #print("AI")
            
            elif Recepcion_Mensaje == b'Retrocede hacia la izquierda':
                self.ser.write('Z'.encode('utf-8'))
                #print("RI")
                            
            elif Recepcion_Mensaje == b'Retrocede hacia la derecha':
                self.ser.write('C'.encode('utf-8'))
                #print("RD")
            
                # Freno
            
            elif Recepcion_Mensaje == b'Freno':
                self.ser.write('X'.encode('utf-8'))
                #print("Freno")
                
            elif Recepcion_Mensaje == b'Nada':
                self.ser.write('P'.encode('utf-8'))
                #print("Nada")
                
            if Recepcion_Mensaje == b'fin del teclado':
                ctrl_bucle = False
                print("Se ha finalizado el teclado")
                break

    def volante(self,Ctrl_drv,ctrl_bucle,empezar):
        

        while ctrl_bucle:
            
            Recepcion_Mensaje = self.cliente.recv(32768)
            
            if Recepcion_Mensaje == b'fin del volante':
                ctrl_bucle = False
                print("Se ha finalizado el volante")
                break
            
            mensaje = pickle.loads(Recepcion_Mensaje)
            x,y = mensaje
                
                # Ordenes mixtas
                        
            if x < 0 and y > 0:
                if Ctrl_drv == False:
                    Ctrl_drv = True
                self.ser.write('Q'.encode('utf-8'))
                #print("Desplazate hacia la izquierda")                
                        
            elif x > 0 and y > 0:
                if Ctrl_drv == False:
                    Ctrl_drv = True                
                self.ser.write('E'.encode('utf-8'))
                #print("Desplazate hacia la derecha")
                                             
            elif x < 0 and y <= -1 and y <0 :
                if Ctrl_drv == False:
                    Ctrl_drv = True                
                self.ser.write('Z'.encode('utf-8'))
                #print("Retrocede hacia la izquierda")
                            
            elif x > 0 and y < 0:
                if Ctrl_drv == False:
                    Ctrl_drv = True                
                self.ser.write('C'.encode('utf-8'))
                #print("Retrocede hacia la derecha")
                            
                # Ordenes Simples
                        
            elif x < 0:
                if Ctrl_drv == True:
                    self.ser.write('P'.encode('utf-8'))
                    Ctrl_drv = False
                self.ser.write('A'.encode('utf-8'))
                #print("Carro muevete a la izquierda")    
                             
            elif x > 0:
                if Ctrl_drv == True:
                    self.ser.write('P'.encode('utf-8'))
                    Ctrl_drv = False                
                self.ser.write('D'.encode('utf-8'))
                #print("Carro muevete a la derecha")
                                       
            elif y < 0:
                if Ctrl_drv == True:
                    self.ser.write('P'.encode('utf-8'))
                    Ctrl_drv = False                
                self.ser.write('S'.encode('utf-8'))
                #print("Carro muevete hacia atras")
        
            elif y > 0:
                if Ctrl_drv == True:
                    self.ser.write('P'.encode('utf-8'))
                    Ctrl_drv = False
                self.ser.write('W'.encode('utf-8'))                    
                print("Carro muevete hacia adelante")
                    
                # Carro inmovil
                
            else:
                self.ser.write('P'.encode('utf-8'))
                print("carro inmovil")
                    
                # Orden de finalizacion 
                

                
                #if time.time() - empezar > 10:  # Refrescar para no colapsar la PC
                 #   break   