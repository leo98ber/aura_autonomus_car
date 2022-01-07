class conductor(object):
    
    def __init__(self,cliente):
        
        self.cliente = cliente
        
                
    def decision(self,prediccion):
        
        if prediccion == 1:
            print("Derecha")
            mensaje = b"Desplazate hacia la derecha"
            self.cliente.send(mensaje)
            
        elif prediccion == 0:
            print("Izquierda")
            mensaje = b"Desplazate hacia la izquierda"
            self.cliente.send(mensaje)
            
        elif prediccion == 2:
            print("Adelante")
            mensaje = b"adelante"
            self.cliente.send(mensaje)
                                
        else:
            self.stop()
                
    def stop(self):
        mensaje = b'Nada'
        self.cliente.send(mensaje)   
        