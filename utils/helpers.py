# utils/helpers.py
import os
import sys
from pathlib import Path

def obtener_ruta_base():
    """Obtener la ruta base dependiendo si es .exe o script"""
    if getattr(sys, 'frozen', False):
        # Ejecutando como .exe - datos van junto al ejecutable
        return Path(sys.executable).parent
    else:
        # Ejecutando como script
        return Path(__file__).parent.parent

def obtener_carpeta_descargas():
    """Obtener la carpeta de Descargas del usuario"""
    try:
        if os.name == 'nt':  # Windows
            import ctypes
            from ctypes import wintypes, windll

            CSIDL_PERSONAL = 5
            SHGFP_TYPE_CURRENT = 0

            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

            documents_path = buf.value
            downloads_path = Path(documents_path) / "Descargas"

            if not downloads_path.exists():
                downloads_path = Path.home() / "Downloads"
        else:  # Linux/Mac
            downloads_path = Path.home() / "Downloads"

        downloads_path.mkdir(exist_ok=True)
        return downloads_path

    except Exception:
        return obtener_ruta_base()

def crear_directorio_bingos():
    """Crear directorio interno para guardar datos de bingos"""
    ruta_base = obtener_ruta_base()
    
    if getattr(sys, 'frozen', False):
        # En .exe: crear carpeta oculta junto al ejecutable
        directorio_bingos = ruta_base / ".bingos_data"
    else:
        # En desarrollo: en carpeta data
        directorio_bingos = ruta_base / "data" / "bingos"
    
    directorio_bingos.mkdir(parents=True, exist_ok=True)
    
    # En Windows, ocultar la carpeta si es .exe
    if getattr(sys, 'frozen', False) and os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(str(directorio_bingos), 2)  # FILE_ATTRIBUTE_HIDDEN
        except:
            pass
            
    return directorio_bingos