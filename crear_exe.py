import PyInstaller.__main__
import os
import sys

def crear_ejecutable():
    """Crear el ejecutable del sistema de bingos"""
    
    # Verificar que el archivo principal existe
    if not os.path.exists('main.py'):
        print("❌ Error: No se encuentra main.py")
        input("Presiona Enter para salir...")
        return
    
    print("🚀 Creando ejecutable con almacenamiento interno...")
    print("📦 Esto puede tomar unos minutos...")
    
    try:
        PyInstaller.__main__.run([
            'main.py',
            '--onefile',
            '--windowed',
            '--name=SistemaBingosProfesional',
            '--clean',
            '--noconfirm',
            '--add-data=views;views',
            '--add-data=models;models', 
            '--add-data=utils;utils',
            '--hidden-import=tkinter',
            '--hidden-import=json',
            '--hidden-import=pathlib',
            '--hidden-import=datetime',
            '--hidden-import=os',
            '--hidden-import=sys',
            '--hidden-import=tempfile'
        ])
        
        print("✅ Ejecutable creado exitosamente!")
        print(f"📁 Encuentra tu .exe en: {os.path.abspath('dist/SistemaBingosProfesional.exe')}")
        print("💾 Los datos se guardarán internamente en el sistema")
        
    except Exception as e:
        print(f"❌ Error creando el ejecutable: {e}")
    
    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    crear_ejecutable()