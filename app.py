import tkinter as tk
from views.menu_principal import VistaMenuPrincipal
from views.gestor_bingos import VistaGestorBingos
from views.vista_tablas import VistaTablas
from views.vista_asignaciones import VistaAsignaciones

class SistemaBingos:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Bingos")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Frame principal para navegación
        self.frame_principal = tk.Frame(self.root, bg='#1e1e1e')
        self.frame_principal.pack(fill="both", expand=True)
        
        # Diccionario de vistas
        self.vistas = {}
        
        # Inicializar vistas
        self.inicializar_vistas()
        
        # Mostrar menú principal al inicio
        self.mostrar_vista("menu_principal")
    
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