# app.py
import tkinter as tk
from views.menu_principal import VistaMenuPrincipal
from views.gestor_bingos import VistaGestorBingos
from views.vista_tablas import VistaTablas
from views.vista_asignaciones import VistaAsignaciones
import os
import sys
from pathlib import Path

class SistemaBingos:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Sistema de Gestión de Bingos Profesional")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0f0f23')
        
        # Configurar el icono PRIMERO, antes de centrar
        self.configurar_icono()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Frame principal que ocupará todo el espacio
        self.frame_principal = tk.Frame(self.root, bg='#0f0f23')
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)  # Agregar padding

        # Diccionario de vistas
        self.vistas = {}

        # Inicializar vistas
        self.inicializar_vistas()

        # Mostrar menú principal al inicio
        self.mostrar_vista("menu_principal")

    def configurar_icono(self):
        """Configurar el icono de la aplicación para Windows"""
        try:
            # Buscar en múltiples ubicaciones
            rutas_busqueda = [
                # Rutas relativas
                "assets/logo.ico",
                "logo.ico", 
                "assets/logo.png",
                "logo.png",
                # Rutas absolutas desde el directorio actual
                Path(__file__).parent / "assets" / "logo.ico",
                Path(__file__).parent / "assets" / "logo.png",
                Path(__file__).parent / "logo.ico",
                Path(__file__).parent / "logo.png",
                # Para PyInstaller (archivos empaquetados)
                Path(sys._MEIPASS) / "assets" / "logo.ico" if hasattr(sys, '_MEIPASS') else "",
                Path(sys._MEIPASS) / "logo.ico" if hasattr(sys, '_MEIPASS') else "",
            ]
            
            icono_encontrado = None
            
            for ruta in rutas_busqueda:
                if ruta and os.path.exists(ruta):
                    icono_encontrado = ruta
                    break
            
            if icono_encontrado:
                if icono_encontrado.lower().endswith('.ico'):
                    # Para archivos .ico usar iconbitmap
                    self.root.iconbitmap(icono_encontrado)
                    print(f"✅ Icono ICO cargado: {icono_encontrado}")
                else:
                    # Para archivos PNG usar iconphoto
                    try:
                        icono_img = tk.PhotoImage(file=icono_encontrado)
                        self.root.iconphoto(True, icono_img)
                        # Guardar referencia para evitar garbage collection
                        self._icono_ref = icono_img
                        print(f"✅ Icono PNG cargado: {icono_encontrado}")
                    except Exception as e:
                        print(f"❌ Error cargando PNG: {e}")
            else:
                print("⚠️ No se encontró ningún archivo de icono")
                print("💡 Buscando en:")
                for ruta in rutas_busqueda:
                    if ruta:
                        print(f"   - {ruta}")
                        
        except Exception as e:
            print(f"❌ Error configurando el icono: {e}")

    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        # Usar tamaño fijo para centrado inicial
        ancho = 1400
        alto = 900
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

    def inicializar_vistas(self):
        """Inicializar todas las vistas del sistema"""
        self.vistas["menu_principal"] = VistaMenuPrincipal(self.frame_principal, self)
        self.vistas["gestor_bingos"] = VistaGestorBingos(self.frame_principal, self)
        self.vistas["vista_tablas"] = VistaTablas(self.frame_principal, self)
        self.vistas["vista_asignaciones"] = VistaAsignaciones(self.frame_principal, self)

    def mostrar_vista(self, nombre_vista, datos=None):
        """Mostrar una vista específica"""
        # Ocultar todas las vistas
        for vista in self.vistas.values():
            vista.ocultar()

        # Mostrar la vista solicitada
        if nombre_vista in self.vistas:
            self.vistas[nombre_vista].mostrar(datos)

    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()