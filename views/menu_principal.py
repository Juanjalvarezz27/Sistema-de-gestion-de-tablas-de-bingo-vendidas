# views/menu_principal.py
import tkinter as tk
from tkinter import ttk

class VistaMenuPrincipal:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.frame = tk.Frame(parent, bg='#0f0f23')
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crear interfaz simplificada del menú principal"""
        # Frame principal
        main_frame = tk.Frame(self.frame, bg='#0f0f23')
        main_frame.pack(fill='both', expand=True)
        
        # Título principal
        title_label = tk.Label(main_frame,
            text="🎯 SISTEMA BINGOS PRO",
            font=('Segoe UI', 28, 'bold'),
            bg='#0f0f23',
            fg='#00ff88',
            pady=40
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(main_frame,
            text="Gestión Profesional de Cartones",
            font=('Segoe UI', 14),
            bg='#0f0f23',
            fg='#b0b0b0',
            pady=10
        )
        subtitle_label.pack()
        
        # Frame para botones
        buttons_frame = tk.Frame(main_frame, bg='#0f0f23')
        buttons_frame.pack(expand=True, pady=50)
        
        # Botón Crear Nuevo Bingo
        btn_crear = tk.Button(buttons_frame,
            text="🆕 CREAR NUEVO BINGO",
            command=self.crear_nuevo_bingo,
            font=('Segoe UI', 14, 'bold'),
            bg='#00ff88',
            fg='#0f0f23',
            width=25,
            height=2,
            relief='flat',
            cursor='hand2'
        )
        btn_crear.pack(pady=20)
        
        # Botón Gestionar Bingos
        btn_gestionar = tk.Button(buttons_frame,
            text="📊 GESTIONAR BINGOS",
            command=self.gestionar_bingos,
            font=('Segoe UI', 14, 'bold'),
            bg='#0099ff',
            fg='white',
            width=25,
            height=2,
            relief='flat',
            cursor='hand2'
        )
        btn_gestionar.pack(pady=20)
        
        # Footer
        footer_label = tk.Label(main_frame,
            text="Sistema de Gestión de Bingos Profesional v1.0",
            font=('Segoe UI', 10),
            bg='#0f0f23',
            fg='#666666',
            pady=20
        )
        footer_label.pack(side='bottom')

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