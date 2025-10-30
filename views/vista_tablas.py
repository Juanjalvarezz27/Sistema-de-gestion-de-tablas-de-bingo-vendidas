import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from pathlib import Path

class VistaTablas:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.bingo_actual = None
        self.busqueda_actual = ""
        
        self.frame = tk.Frame(parent, bg='#1e1e1e')
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz principal de tablas con diseño mejorado"""
        # Frame de navegación superior
        frame_nav = tk.Frame(self.frame, bg='#2d2d2d', height=80)
        frame_nav.pack(fill='x', padx=20, pady=10)
        frame_nav.pack_propagate(False)
        
        # Botón volver al gestor
        self.btn_volver = tk.Button(frame_nav,
                                  text="← VOLVER A BINGOS",
                                  command=self.volver_gestor,
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#666666',
                                  fg='white',
                                  padx=20,
                                  pady=12,
                                  relief='flat',
                                  cursor='hand2')
        self.btn_volver.pack(side='left', padx=10, pady=10)
        
        # Información del bingo actual
        self.lbl_info_bingo = tk.Label(frame_nav,
                                     text="Bingo: [Nombre] | Cartones: 0/0",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#2d2d2d',
                                     fg='#4CAF50')
        self.lbl_info_bingo.pack(side='left', padx=20, pady=10)
        
        # Frame de búsqueda mejorado
        frame_busqueda = tk.Frame(frame_nav, bg='#2d2d2d')
        frame_busqueda.pack(side='right', padx=10, pady=10)
        
        # Contenedor de búsqueda con bordes redondeados
        frame_contenedor_busqueda = tk.Frame(frame_busqueda, bg='#3d3d3d', relief='flat', bd=1)
        frame_contenedor_busqueda.pack(padx=5, pady=5)
        
        lbl_buscar = tk.Label(frame_contenedor_busqueda,
                            text="🔍",
                            font=('Segoe UI', 14),
                            bg='#3d3d3d',
                            fg='#cccccc',
                            padx=8,
                            pady=6)
        lbl_buscar.pack(side='left')
        
        self.entry_busqueda = tk.Entry(frame_contenedor_busqueda,
                                     font=('Segoe UI', 11),
                                     bg='#2d2d2d',
                                     fg='white',
                                     insertbackground='white',
                                     relief='flat',
                                     width=25,
                                     bd=0,
                                     highlightthickness=0)
        self.entry_busqueda.pack(side='left', padx=5, pady=6)
        self.entry_busqueda.bind('<KeyRelease>', self.filtrar_tablas)
        
        # Botón limpiar búsqueda con diseño mejorado
        self.btn_limpiar_busqueda = tk.Button(frame_contenedor_busqueda,
                                            text="✕",
                                            command=self.limpiar_busqueda,
                                            font=('Segoe UI', 12, 'bold'),
                                            bg='#666666',
                                            fg='white',
                                            width=3,
                                            relief='flat',
                                            cursor='hand2',
                                            bd=0)
        self.btn_limpiar_busqueda.pack(side='left', padx=5, pady=2)
        
        # Frame de controles
        frame_controles = tk.Frame(self.frame, bg='#1e1e1e')
        frame_controles.pack(fill='x', padx=20, pady=15)
        
        # Botones de acción con más padding
        btn_exportar_pdf = tk.Button(frame_controles,
                                   text="📄 GENERAR REPORTE PDF",
                                   command=self.exportar_pdf,
                                   font=('Segoe UI', 10, 'bold'),
                                   bg='#FF9800',
                                   fg='white',
                                   padx=20,
                                   pady=12,
                                   relief='flat',
                                   cursor='hand2')
        btn_exportar_pdf.pack(side='left', padx=8)
        
        btn_reset = tk.Button(frame_controles,
                            text="🔄 RESETEAR BINGO",
                            command=self.resetear_bingo,
                            font=('Segoe UI', 10, 'bold'),
                            bg='#e74c3c',
                            fg='white',
                            padx=20,
                            pady=12,
                            relief='flat',
                            cursor='hand2')
        btn_reset.pack(side='left', padx=8)
        
        # Frame principal de tablas
        self.frame_tablas = tk.Frame(self.frame, bg='#1e1e1e')
        self.frame_tablas.pack(fill='both', expand=True, padx=15, pady=10)
    
    def crear_tablas(self, bingo):
        """Crear la visualización de tablas"""
        self.bingo_actual = bingo
        self.actualizar_info_bingo()
        
        # Limpiar frame de tablas
        for widget in self.frame_tablas.winfo_children():
            widget.destroy()
        
        # Frame contenedor con scroll
        contenedor = tk.Frame(self.frame_tablas, bg='#1e1e1e')
        contenedor.pack(fill='both', expand=True)
        
        # Canvas con scrollbar
        self.canvas = tk.Canvas(contenedor, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)
        
        self.frame_numeros = tk.Frame(self.canvas, bg='#1e1e1e')
        
        self.frame_numeros.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame_numeros, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar scroll con mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.frame_numeros.bind("<MouseWheel>", self._on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar grid y crear botones
        self.crear_botones_numeros()
        self.canvas.bind("<Configure>", self.redimensionar_botones)
    
    def _on_mousewheel(self, event):
        """Manejar scroll del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def crear_botones_numeros(self):
        """Crear botones de números que ocupen el 100% del espacio"""
        if not self.bingo_actual:
            return
            
        for widget in self.frame_numeros.winfo_children():
            widget.destroy()
        
        # Obtener cartones que cumplen con la búsqueda
        cartones_filtrados = []
        for numero in range(1, self.bingo_actual.cantidad_cartones + 1):
            if self.cumple_busqueda(numero):
                cartones_filtrados.append(numero)
        
        if not cartones_filtrados:
            # Mostrar mensaje si no hay resultados
            lbl_sin_resultados = tk.Label(self.frame_numeros,
                                        text="🔍 No se encontraron cartones que coincidan con la búsqueda",
                                        font=('Segoe UI', 12),
                                        bg='#1e1e1e',
                                        fg='#666666')
            lbl_sin_resultados.pack(pady=50)
            return
        
        # Siempre usar 10 columnas para ocupar todo el espacio
        columnas = 10
        filas = (len(cartones_filtrados) + columnas - 1) // columnas
        
        # Configurar grid para que ocupe el 100% del espacio
        for i in range(filas):
            self.frame_numeros.grid_rowconfigure(i, weight=1)
        for i in range(columnas):
            self.frame_numeros.grid_columnconfigure(i, weight=1)
        
        # Calcular dimensiones basadas en el espacio disponible
        ancho_canvas = max(800, self.canvas.winfo_width())
        ancho_boton = (ancho_canvas - 20) // columnas  # 20px de padding total
        alto_boton = 85  # Altura fija adecuada
        
        # Crear botones en orden secuencial ocupando todo el espacio
        for idx, numero in enumerate(cartones_filtrados):
            fila = idx // columnas
            columna = idx % columnas
            
            estado = self.bingo_actual.obtener_estado_carton(numero)
            vendido = estado.get('vendido', False)
            nombre = estado.get('nombre', '')
            
            # Diseño moderno de botones con bordes redondeados
            if vendido:
                texto = f"#{numero}\n✅ {nombre.split()[0] if nombre else 'Vendido'}"
                color_bg = "#27ae60"
                color_hover = "#219a52"
            else:
                texto = f"#{numero}\n🟢 Disponible"
                color_bg = "#3498db"
                color_hover = "#2980b9"
            
            btn = HoverButton(
                self.frame_numeros,
                text=texto,
                command=lambda n=numero: self.abrir_modal(n),
                bg=color_bg,
                fg="white",
                font=('Segoe UI', 9, 'bold'),
                relief="flat",
                bd=0,
                cursor="hand2",
                justify='center',
                hover_color=color_hover,
                border_radius=15,  # Bordes más redondeados
                wraplength=ancho_boton - 20
            )
            
            # Usar sticky="nsew" para que expanda y ocupe todo el espacio
            btn.grid(row=fila, column=columna, padx=1, pady=1, sticky="nsew")
    
    def cumple_busqueda(self, numero):
        """Verificar si un cartón cumple con la búsqueda actual"""
        if not self.busqueda_actual:
            return True
            
        busqueda = self.busqueda_actual.lower()
        
        # Buscar por número
        if busqueda.isdigit() and busqueda in str(numero):
            return True
        
        # Buscar por nombre
        estado = self.bingo_actual.obtener_estado_carton(numero)
        if estado.get('vendido', False) and busqueda in estado.get('nombre', '').lower():
            return True
            
        return False
    
    def filtrar_tablas(self, event=None):
        """Filtrar tablas según la búsqueda"""
        self.busqueda_actual = self.entry_busqueda.get().strip().lower()
        self.crear_botones_numeros()
    
    def limpiar_busqueda(self):
        """Limpiar la búsqueda y mostrar todas las tablas"""
        self.entry_busqueda.delete(0, tk.END)
        self.busqueda_actual = ""
        self.crear_botones_numeros()
    
    def actualizar_info_bingo(self):
        """Actualizar la información del bingo en la barra superior"""
        if self.bingo_actual:
            vendidos = self.bingo_actual.obtener_cartones_vendidos()
            ganancias = self.bingo_actual.obtener_ganancias()
            texto = (f"Bingo: {self.bingo_actual.nombre} | "
                    f"Cartones: {len(vendidos)}/{self.bingo_actual.cantidad_cartones} | "
                    f"Precio: ${self.bingo_actual.precio_carton:,.2f} | "
                    f"Ganancias: ${ganancias:,.2f}")
            self.lbl_info_bingo.config(text=texto)
    
    def abrir_modal(self, numero):
        """Abrir modal para asignar/ver cartón con botones más altos"""
        estado_actual = self.bingo_actual.obtener_estado_carton(numero)
        
        # Si ya está vendido, mostrar información con opción de cancelar
        if estado_actual.get('vendido', False):
            modal = tk.Toplevel(self.parent)
            modal.title(f"🎫 Información del Cartón #{numero}")
            modal.geometry("500x400")  # Más alto para los botones
            modal.configure(bg='#1e1e1e')
            modal.transient(self.parent)
            modal.grab_set()
            
            # Centrar el modal
            modal.update_idletasks()
            x = (modal.winfo_screenwidth() // 2) - (500 // 2)
            y = (modal.winfo_screenheight() // 2) - (400 // 2)
            modal.geometry(f"500x400+{x}+{y}")
            
            frame_modal = tk.Frame(modal, bg='#1e1e1e', padx=25, pady=25)
            frame_modal.pack(fill="both", expand=True)
            
            # Icono de cartón vendido
            lbl_icono = tk.Label(frame_modal, text="✅", font=("Arial", 24), bg='#1e1e1e', fg='#27ae60')
            lbl_icono.pack(pady=10)
            
            # Información del cartón
            lbl_titulo = tk.Label(frame_modal, text=f"CARTÓN #{numero} - VENDIDO", 
                                 font=("Segoe UI", 16, "bold"), bg='#1e1e1e', fg='#27ae60')
            lbl_titulo.pack(pady=5)
            
            lbl_nombre = tk.Label(frame_modal, text=f"👤 Asignado a: {estado_actual.get('nombre', '')}", 
                                font=("Segoe UI", 14), bg='#1e1e1e', fg='#ffffff')
            lbl_nombre.pack(pady=15)
            
            # Frame para botones con más altura
            frame_botones = tk.Frame(frame_modal, bg='#1e1e1e')
            frame_botones.pack(pady=30)
            
            def cancelar_venta():
                if self.bingo_actual.liberar_carton(numero):
                    modal.destroy()
                    self.crear_botones_numeros()
                    self.actualizar_info_bingo()
                    messagebox.showinfo("Éxito", f"✅ Venta del cartón #{numero} cancelada")
                else:
                    messagebox.showerror("Error", "No se pudo cancelar la venta")
            
            btn_cancelar = tk.Button(frame_botones, text="❌ CANCELAR VENTA", 
                                   command=cancelar_venta,
                                   bg="#e74c3c", fg="white", font=("Segoe UI", 12, "bold"),
                                   width=18, height=2, padx=25, pady=20,  # Mucho más padding
                                   relief='flat', cursor="hand2")
            btn_cancelar.pack(side="left", padx=10)
            
            btn_cerrar = tk.Button(frame_botones, text="👌 CERRAR", 
                                 command=modal.destroy,
                                 bg="#95a5a6", fg="white", font=("Segoe UI", 12, "bold"),
                                 width=14, height=2, padx=25, pady=20,  # Mucho más padding
                                 relief='flat', cursor="hand2")
            btn_cerrar.pack(side="left", padx=10)
            
            return
        
        # Modal para nueva venta
        modal = tk.Toplevel(self.parent)
        modal.title(f"🎫 Asignar Cartón #{numero}")
        modal.geometry("500x350")  # Más alto para los botones
        modal.configure(bg='#1e1e1e')
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar el modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (350 // 2)
        modal.geometry(f"500x350+{x}+{y}")
        
        frame_modal = tk.Frame(modal, bg='#1e1e1e', padx=25, pady=25)
        frame_modal.pack(fill="both", expand=True)
        
        # Título
        lbl_titulo = tk.Label(frame_modal, text=f"🎫 ASIGNAR CARTÓN #{numero}", 
                             font=("Segoe UI", 16, "bold"), bg='#1e1e1e', fg='#ffffff')
        lbl_titulo.pack(pady=15)
        
        # Campo para nombre
        lbl_nombre = tk.Label(frame_modal, text="👤 Nombre completo de la persona:", 
                             font=("Segoe UI", 11), bg='#1e1e1e', fg='#cccccc')
        lbl_nombre.pack(pady=8)
        
        entry_nombre = tk.Entry(frame_modal, width=40, font=("Segoe UI", 12), 
                               bg='#3d3d3d', fg='white', insertbackground='white',
                               relief='flat')
        entry_nombre.pack(pady=15, ipady=10)
        entry_nombre.focus()
        
        # Frame para botones con más altura
        frame_botones = tk.Frame(frame_modal, bg='#1e1e1e')
        frame_botones.pack(pady=25)
        
        def asignar_venta():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "❌ Por favor ingrese un nombre")
                return
            
            # Asignar el cartón
            self.bingo_actual.asignar_carton(numero, nombre)
            modal.destroy()
            self.crear_botones_numeros()
            self.actualizar_info_bingo()
            
            messagebox.showinfo("Éxito", f"✅ Cartón #{numero} asignado a:\n{nombre}")
        
        def cancelar():
            modal.destroy()
        
        # Botones con mucho más padding
        btn_asignar = tk.Button(frame_botones, text="✅ ASIGNAR", 
                               command=asignar_venta, 
                               bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"),
                               width=14, height=2, padx=25, pady=20,  # Mucho más padding
                               relief='flat', cursor="hand2")
        btn_asignar.pack(side="left", padx=15)
        
        btn_cancelar = tk.Button(frame_botones, text="❌ CANCELAR", 
                                command=cancelar, 
                                bg="#95a5a6", fg="white", font=("Segoe UI", 12, "bold"),
                                width=14, height=2, padx=25, pady=20,  # Mucho más padding
                                relief='flat', cursor="hand2")
        btn_cancelar.pack(side="left", padx=15)
        
        # Enter para asignar, Escape para cancelar
        modal.bind('<Return>', lambda e: asignar_venta())
        modal.bind('<Escape>', lambda e: cancelar())
        
        modal.focus_force()
        entry_nombre.focus()
    
    def exportar_pdf(self):
        """Exportar reporte PDF del bingo actual"""
        if self.bingo_actual:
            self.bingo_actual.exportar_pdf()
    
    def resetear_bingo(self):
        """Resetear el bingo actual"""
        if self.bingo_actual and messagebox.askyesno("Confirmar", 
                                                   "¿Estás seguro de resetear todos los cartones?\n\n"
                                                   "Esta acción liberará todos los cartones vendidos."):
            self.bingo_actual.resetear()
            self.crear_botones_numeros()
            self.actualizar_info_bingo()
            messagebox.showinfo("Éxito", "✅ Bingo reseteado correctamente")
    
    def redimensionar_botones(self, event=None):
        """Redimensionar botones al cambiar tamaño para ocupar el 100%"""
        self.crear_botones_numeros()
    
    def volver_gestor(self):
        """Volver al gestor de bingos"""
        self.controlador.mostrar_vista("gestor_bingos")
    
    def mostrar(self, datos=None):
        """Mostrar esta vista"""
        self.frame.pack(fill="both", expand=True)
        if datos and "bingo" in datos:
            self.crear_tablas(datos["bingo"])
    
    def ocultar(self):
        """Ocultar esta vista"""
        self.frame.pack_forget()

class HoverButton(tk.Button):
    """Botón con efecto hover moderno y bordes muy redondeados"""
    def __init__(self, *args, **kwargs):
        self.hover_color = kwargs.pop('hover_color', None)
        self.border_radius = kwargs.pop('border_radius', 15)  # Más redondeado
        self.original_color = kwargs.get('bg', '#3498db')
        super().__init__(*args, **kwargs)
        
        # Configurar bordes redondeados
        self.config(
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=8
        )
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        if self.hover_color:
            self.config(bg=self.hover_color)
    
    def on_leave(self, e):
        self.config(bg=self.original_color)