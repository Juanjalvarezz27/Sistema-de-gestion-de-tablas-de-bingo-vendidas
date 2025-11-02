# views/menu_principal.py
import tkinter as tk
from tkinter import ttk
from utils.excel_generator import GeneradorExcel

class VistaMenuPrincipal:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.frame = tk.Frame(parent, bg='#0f0f23')
        self.generador_excel = GeneradorExcel(parent)
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
        
        # Frame para botones en 2 columnas
        buttons_container = tk.Frame(main_frame, bg='#0f0f23')
        buttons_container.pack(expand=True, pady=50)
        
        # Frame para la primera fila de botones (2 columnas)
        buttons_row1 = tk.Frame(buttons_container, bg='#0f0f23')
        buttons_row1.pack(pady=10)
        
        # Frame para la segunda fila de botones (centrado)
        buttons_row2 = tk.Frame(buttons_container, bg='#0f0f23')
        buttons_row2.pack(pady=10)
        
        # Botón Crear Nuevo Bingo (columna 1)
        btn_crear = tk.Button(buttons_row1,
            text="🆕 CREAR NUEVO BINGO",
            command=self.crear_nuevo_bingo,
            font=('Segoe UI', 14, 'bold'),
            bg='#00ff88',
            fg='#0f0f23',
            width=20,
            height=2,
            relief='flat',
            cursor='hand2'
        )
        btn_crear.pack(side='left', padx=15)
        
        # Botón Gestionar Bingos (columna 2)
        btn_gestionar = tk.Button(buttons_row1,
            text="📊 GESTIONAR BINGOS",
            command=self.gestionar_bingos,
            font=('Segoe UI', 14, 'bold'),
            bg='#0099ff',
            fg='white',
            width=20,
            height=2,
            relief='flat',
            cursor='hand2'
        )
        btn_gestionar.pack(side='left', padx=15)
        
        # Nuevo botón Generar Excel (centrado en segunda fila)
        btn_excel = tk.Button(buttons_row2,
            text="📊 GENERAR EXCEL",
            command=self.generar_excel,
            font=('Segoe UI', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            width=20,
            height=2,
            relief='flat',
            cursor='hand2'
        )
        btn_excel.pack(pady=10)
        
        # Footer
        footer_label = tk.Label(main_frame,
            text="Sistema de Gestión de Bingos Profesional - Creado por Juan Alvarez",
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

    def generar_excel(self):
        """Abrir modal para generar Excel con tablas de bingo"""
        self.generador_excel.mostrar_modal_cantidad()

    def mostrar(self, datos=None):
        """Mostrar esta vista"""
        self.frame.pack(fill="both", expand=True)

    def ocultar(self):
        """Ocultar esta vista"""
        self.frame.pack_forget()