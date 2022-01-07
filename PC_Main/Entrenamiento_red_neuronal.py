from Modelo_red_neuronal import load_data, NeuralNetwork

if __name__ == '__main__':

    neuronas_de_entrada = 120 * 320
    datos_de_entrenamiento = "datos_de_entrenamiento/*.npz"    
    x_train, x_valid, y_train, y_valid = load_data(neuronas_de_entrada,datos_de_entrenamiento)
        
    # Entrenar una red neuronal
    layer_sizes = [neuronas_de_entrada,32,8, 4]              # 32 neuronas en la capa oculta elegidas de forma arbitraria
    nn = NeuralNetwork()
    nn.create(layer_sizes)
    modelo = nn.train(x_train, y_train)

    # evaluar el entrenamiento
    presicion_entrenamiento = nn.evaluate(x_train, y_train)
    print("Precision de entrenamiento: ", "{0:.2f}%".format(presicion_entrenamiento * 100))
    
    # evaluar con los datos de validacion 
    presicion_validacion = nn.evaluate(x_valid, y_valid)
    print("Presicion de la validacion: ", "{0:.2f}%".format(presicion_validacion * 100))
    
    # Guardar modelo
    guardar_modelo = "guardar_modelo/modelo_red_neuronal_8.xml"
    modelo_2 = nn.save_model(guardar_modelo)
