import PyInstaller.__main__
import os

# Configuración para crear el ejecutable
PyInstaller.__main__.run([
    'main.py',  # Usa el archivo correcto
    '--onefile',                    # Un solo archivo ejecutable
    '--windowed',                   # Sin consola
    '--name=SistemaGestionTablas',  # Nombre del ejecutable
    '--clean',                      # Limpiar archivos temporales
])