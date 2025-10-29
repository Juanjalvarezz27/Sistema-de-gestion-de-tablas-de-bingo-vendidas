import PyInstaller.__main__
import os

# Configuración para crear el ejecutable
PyInstaller.__main__.run([
    'sistema_final_descargas.py',
    '--onefile',  # Un solo archivo ejecutable
    '--windowed',  # Sin consola
    '--name=SistemaGestionTablas',
    '--icon=NONE',  # Puedes agregar un icono .ico si quieres
    '--add-data=tablas_vendidas.json;.',  # Incluir el archivo de datos
])