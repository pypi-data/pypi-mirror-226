import numpy as np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

#def prueba():
#    print("Esto es una prueba de la nueva versión")

#Función para comprobar una actualización 

def prueba():
    print("Esto es una nueva prueba de la nueva versión 6.0")

def generar_array(numeros):
    return np.arange(numeros)


class Saludo:
    def __init__(self):
        print("Hola, te saludo desde Saludo.__init__()")

        
#if __name__ == '__main__': 
#    saludar()

if __name__ == '__main__':
    print(generar_array(5))

#PARA INDICAR QUE EL MODULO MENSAJES ES UN PAQUETE ES "IMPORTANTE INDICARLE EL __INIT__ DENTRO DE ESTE"