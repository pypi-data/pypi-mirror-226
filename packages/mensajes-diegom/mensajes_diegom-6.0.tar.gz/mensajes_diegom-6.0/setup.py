"""
#from struct import pack
from setuptools import setup

setup(name="Mensajes",  # Nombre
      version="2.0",  # Versión de desarrollo
      description="Un paquete para saludar y despedir",  # Descripción del funcionamiento
      author="Diego Merino Correa",  # Nombre del autor
      author_email='diegom.correa0@gmail.com',  # Email del autor
#     license="GPL",  # Licencia: MIT, GPL, GPL 2.0...
      url="http://ejemplo.com",  # Página oficial (si la hay)
      packages=['Mensajes','Mensajes.hola','Mensajes.adios'],
      scripts=['test.py']
)"""
from setuptools import setup, find_packages

setup(
      name='mensajes_diegom',  # Nombre
      version="6.0",  # Versión de desarrollo
      description="Un paquete para saludar y despedir",  # Descripción del funcionamiento
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author="Diego Merino Correa",  # Nombre del autor
      author_email='diegom.correa0@gmail.com',  # Email del autor
#     license="GPL",  # Licencia: MIT, GPL, GPL 2.0...
      url="http://ejemplo.com",  # Página oficial (si la hay)
      license_files=['LICENSE'],
      packages=find_packages(),
#     scripts=['test.py'],
      scripts=[],
      test_suite='tests',
      install_requires=[paquete.strip()
                         for paquete in open("requirements.txt").readlines()],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Utilities',
      ]
)     

#PIP INSTALL BUILD and TWINE para hacer la consutrucción y la publicación
# -m BUILD para lanzar el modulo  
# -m twine check dist/* para confirmar si todos los paquetes estan bien construidos para publicar
#python -m twine upload -r testpypi dist/* -> esto se hace para subir el modulo al servidor pero en la 
      # seccion del respositorio y comprobar que todos los modulos esten bien construidos
#-m twine upload dist/* -> Se utiliza para subir el modulo al servidor publico  