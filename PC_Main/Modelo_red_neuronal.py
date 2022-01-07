import cv2
import numpy as np
import glob
import sys
import time
import os
from sklearn.model_selection import train_test_split


def load_data(neuronas_de_entrada, datos):
    print("Cargando datos de entrenamiento...")
    empezar = time.time()
    
    # Inicializamos variables
    x = np.empty((0, neuronas_de_entrada))
    y = np.empty((0, 4))
    # print(datos) # Imprime el nombre de la carpeta (texto)
    datos_de_entrenamiento = glob.glob(datos)   # Permite cargar la carpeta como tal, y no el nombre (texto)  
     # print(datos_de_entrenamiento)  # Muestra el directorio y sus archivos ejemplo: ['datos_de_entrenamiento\\1576000790.npz']
    
    
    if not datos_de_entrenamiento:
        print("No hay datos, Saliendo")
        sys.exit()
        
    for single_npz in datos_de_entrenamiento:        # El For es para cargar todos los archivos npz, si fuera solo 1 se obvia      
        with np.load(single_npz) as datos:           # trabajo la carga de informacion(npo.load) como variable datos, numpy loads carga el nombre del archivo guardado como numpy savez              
            
            # El texto en corchetes asigna la variable asociada a la etiqueta,  cuando guarde los datos en el scrip(programa codigo) en recoleccion de datos
            entrada_red_neuronal = datos['train']    # X = 'train'      
            etiquetas = datos['train_labels']         # Y = 'train_labels'
            
        # Una vez cargado los datos se procede a llenar las matrices con los datos guardados en el archivo npz
        x = np.vstack((x, entrada_red_neuronal))   # Con vstack se agregan datos verticalmente, es decir se agregan filas.  
        y = np.vstack((y, etiquetas))

    print("forma del array de la imagen: ", x.shape)
    print("forma de la etiqueta: ", y.shape)

    terminar = time.time()
    print("Duracion de la carga: %.2fs" % (terminar - empezar))

    # Normalizar la data
    x = x / 255			           #lo normalizamos para que tengan un valor entre 0 y 1, por eso dividimos en 255.                            

    # Divido los datos en 70 30
    return train_test_split(x, y, test_size=0.3)


# NOTA: Si la carpeta de datos de entrenamiento, no esta en la misma carpeta que el script, no encontrara la data 

# witch es para determinar la configuración local que tendrá un bloque de código, lo que se conoce como "contexto".

# Un "contexto" básicamente se establece con una configuración inicial y una finalización para recuperar los valores anteriores

# un erro comun es  que la variable no tiene definidos los métodos de gestor de contextos
    
# Np.load si el archivo es un archivo .npz , el valor devuelto admite el protocolo del administrador de contexto de manera similar a la función abierta ":"
    
# glob Es útil en cualquier situación donde un programa necesita buscar una lista de archivos en el sistema de archivos con nombres que coinciden con un patrón
    
# Para crear una lista de nombres de archivos que tengan una cierta extensión, prefijo, o cualquier cadena común en el medio, usa glob en lugar de escribir código personalizado para escanear los contenidos del directorio

class NeuralNetwork(object):
    def __init__(self):
        self.modelo = None

    def create(self, layer_sizes):
        # Crear red neuronal
        self.modelo = cv2.ml.ANN_MLP_create()  # MLP es perceptron multicapa
        self.modelo.setLayerSizes(np.int32(layer_sizes)) 
        self.modelo.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        self.modelo.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)
        self.modelo.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 0.01))

    def train(self, x, y):
        # Empezar entrenamiento
        empezar = time.time()

        print("Entrenando ...")
        self.modelo.train(np.float32(x), cv2.ml.ROW_SAMPLE, np.float32(y))

        # set end time
        terminar = time.time()
        print("Duracion de entrenamiento: %.2fs" % (terminar - empezar))

    def evaluate(self, x, y):
        ret, resp = self.modelo.predict(x)
        prediction = resp.argmax(-1)
        true_labels = y.argmax(-1)
        precision = np.mean(prediction == true_labels)
        return precision

    def save_model(self, datos):
        carpeta = "guardar_modelo"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        self.modelo.save(datos)
        print("Red neuronal guardada en: " , "'" , datos , "'")

    def load_model(self, datos):
        if not os.path.exists(datos):
            print("No existe red neuronal, salir")
            sys.exit()
        self.modelo = cv2.ml.ANN_MLP_load(datos)


    def predict(self, x):
        resp = None
        try:
            ret, resp = self.modelo.predict(x)
        except Exception as e:
            print(e)
        return resp.argmax(-1)


