# crear_exe.py
import PyInstaller.__main__
import os
import sys
from pathlib import Path

def crear_ejecutable():
    """Crear el ejecutable del sistema de bingos"""

    # Verificar que el archivo principal existe
    if not os.path.exists('main.py'):
        print("❌ Error: No se encuentra main.py")
        input("Presiona Enter para salir...")
        return

    print("🚀 Creando ejecutable con icono...")
    print("📦 Esto puede tomar unos minutos...")

    # Buscar icono en diferentes ubicaciones y formatos
    rutas_icono = [
        "assets/logo.ico",  # Prioridad 1: .ico
        "logo.ico",
        "assets/logo.png",  # Prioridad 2: .png  
        "logo.png",
        Path(__file__).parent / "assets" / "logo.ico",
        Path(__file__).parent / "logo.ico",
        Path(__file__).parent / "assets" / "logo.png",
        Path(__file__).parent / "logo.png"
    ]
    
    icon_arg = ""
    icono_encontrado = None
    
    for ruta in rutas_icono:
        if os.path.exists(ruta):
            icono_encontrado = ruta
            icon_arg = f'--icon={ruta}'
            print(f"🎯 Icono encontrado: {ruta}")
            break
    
    if not icon_arg:
        print("⚠️ No se encontró ningún archivo de icono")
        print("💡 Crea un archivo 'logo.ico' en la carpeta 'assets/'")
    else:
        # Verificar si es PNG y sugerir conversión
        if icono_encontrado and icono_encontrado.lower().endswith('.png'):
            print("⚠️ Se encontró un PNG, pero se recomienda usar .ico para mejor compatibilidad")
            print("💡 Convierte tu PNG a ICO usando: https://convertio.co/es/png-ico/")

    try:
        # Argumentos base de PyInstaller
        args = [
            'main.py',
            '--onefile',
            '--windowed',
            '--name=SistemaBingosProfesional',
            '--clean',
            '--noconfirm',
            '--add-data=views;views',
            '--add-data=models;models', 
            '--add-data=utils;utils',
            '--add-data=assets;assets',
            '--hidden-import=tkinter',
            '--hidden-import=json',
            '--hidden-import=pathlib', 
            '--hidden-import=datetime',
            '--hidden-import=os',
            '--hidden-import=sys',
            '--hidden-import=tempfile',
            '--noconsole'
        ]

        # Agregar icono si existe
        if icon_arg:
            args.append(icon_arg)

        print("🛠️ Ejecutando PyInstaller...")
        PyInstaller.__main__.run(args)

        print("\n✅ Ejecutable creado exitosamente!")
        print(f"📁 Ubicación: {os.path.abspath('dist/SistemaBingosProfesional.exe')}")
        
        if icon_arg:
            print("🎯 El icono debería aparecer en:")
            print("   • El archivo .exe")
            print("   • La barra de tareas de Windows")
            print("   • El administrador de tareas")
        else:
            print("⚠️ El ejecutable usará el icono por defecto de Python")

    except Exception as e:
        print(f"❌ Error creando el ejecutable: {e}")
        print("💡 Solución: Asegúrate de que PyInstaller esté instalado: pip install pyinstaller")

    input("\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    crear_ejecutable()