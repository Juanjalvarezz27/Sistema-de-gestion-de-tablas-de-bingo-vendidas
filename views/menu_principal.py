import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class VistaMenuPrincipal:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        
        # Crear frame principal
        self.frame = tk.Frame(parent, bg='#1e1e1e')
        
        # Configurar estilo moderno
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def configurar_estilo(self):
        """Configurar estilos modernos"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores modernos
        self.style.configure('Modern.TFrame', background='#1e1e1e')
        self.style.configure('Title.TLabel', 
                           background='#1e1e1e', 
                           foreground='#ffffff',
                           font=('Segoe UI', 24, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background='#1e1e1e',
                           foreground='#cccccc',
                           font=('Segoe UI', 14))
    
    def crear_interfaz(self):
        """Crear la interfaz del menú principal"""
        # Frame central
        frame_central = tk.Frame(self.frame, bg='#1e1e1e', padx=50, pady=50)
        frame_central.pack(expand=True)
        
        # Título principal
        titulo = tk.Label(frame_central, 
                         text="🎯 SISTEMA DE BINGOS PROFESIONAL",
                         font=('Segoe UI', 28, 'bold'),
                         bg='#1e1e1e',
                         fg='#ffffff')
        titulo.pack(pady=(0, 10))
        
        subtitulo = tk.Label(frame_central,
                           text="Gestión completa de cartones y asignaciones",
                           font=('Segoe UI', 14),
                           bg='#1e1e1e',
                           fg='#bbbbbb')
        subtitulo.pack(pady=(0, 50))
        
        # Frame de botones
        frame_botones = tk.Frame(frame_central, bg='#1e1e1e')
        frame_botones.pack(pady=20)
        
        # Botón Crear Nuevo Bingo
        btn_nuevo_bingo = tk.Button(frame_botones,
                                  text="🆕 CREAR NUEVO BINGO",
                                  command=self.crear_nuevo_bingo,
                                  font=('Segoe UI', 12, 'bold'),
                                  bg='#4CAF50',
                                  fg='white',
                                  padx=30,
                                  pady=15,
                                  relief='flat',
                                  bd=0,
                                  cursor='hand2')
        btn_nuevo_bingo.pack(pady=10, fill='x')
        
        # Botón Gestionar Bingos Existentes
        btn_gestionar = tk.Button(frame_botones,
                                text="📊 GESTIONAR BINGOS EXISTENTES",
                                command=self.gestionar_bingos,
                                font=('Segoe UI', 12, 'bold'),
                                bg='#2196F3',
                                fg='white',
                                padx=30,
                                pady=15,
                                relief='flat',
                                bd=0,
                                cursor='hand2')
        btn_gestionar.pack(pady=10, fill='x')
        
        # Información del sistema
        frame_info = tk.Frame(frame_central, bg='#2d2d2d', relief='raised', bd=1)
        frame_info.pack(pady=30, fill='x')
        
        info_text = tk.Label(frame_info,
                           text="💡 Crea y gestiona múltiples bingos simultáneamente\n"
                                "🎫 Asigna cartones a participantes\n"
                                "🔍 Busca y filtra información fácilmente\n"
                                "💾 Exporta e importa datos entre dispositivos",
                           font=('Segoe UI', 10),
                           bg='#2d2d2d',
                           fg='#cccccc',
                           justify='left')
        info_text.pack(padx=20, pady=15)
    
    def crear_nuevo_bingo(self):
        """Navegar a la vista de creación de nuevo bingo"""
        self.controlador.mostrar_vista("gestor_bingos", {"accion": "crear"})
    
    def gestionar_bingos(self):
        """Navegar a la vista de gestión de bingos"""
        self.controlador.mostrar_vista("gestor_bingos", {"accion": "gestionar"})
    
    def mostrar(self, datos=None):
        """Mostrar esta vista"""
        self.frame.pack(fill="both", expand=True)
    
    def ocultar(self):
        """Ocultar esta vista"""
        self.frame.pack_forget()