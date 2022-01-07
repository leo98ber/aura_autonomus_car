import serial

class conductor(object):
    
    def __init__(self,puerto_serial,cliente):
        
        self.ser = serial.Serial(puerto_serial, 115200,timeout=1)    
                
    def decision(self,prediccion):
        
        if prediccion == 1:
            print("Derecha")
            self.ser.write('E'.encode('utf-8'))
            
        elif prediccion == 0:
            print("Izquierda")
            self.ser.write('Q'.encode('utf-8'))
            
        elif prediccion == 2:
            print("Adelante")
            self.ser.write('W'.encode('utf-8'))
                                
        else:
            self.stop()
                
    def stop(self):
        self.ser.write('P'.encode('utf-8')) 
        