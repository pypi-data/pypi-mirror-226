import unittest
import numpy as np
from Mensajes.hola.saludos import generar_array



class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6))



"""
from Mensajes.hola.saludos import * #Se tiene acceso a todas las definiciones del modulo
from Mensajes.adios.despedidas import *
#from saludos import saludar

#import saludos

saludar()
Saludo()

despedir()
Despedida()
"""


