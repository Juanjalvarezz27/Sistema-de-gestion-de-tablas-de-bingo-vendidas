import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from pathlib import Path

class RoundedButton(tk.Canvas):
    """Botón con bordes redondeados reales usando Canvas"""
    def __init__(self, parent, text, command, width=100, height=80, 
                 bg_color='#3498db', hover_color='#2980b9', 
                 text_color='white', corner_radius=15, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=parent.cget('bg'))
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.draw_button(text)
        
    def draw_button(self, text):
        self.delete("all")
        
        # Dibujar rectángulo con bordes redondeados
        self.create_rounded_rectangle(0, 0, self.width, self.height, 
                                    radius=self.corner_radius, 
                                    fill=self.bg_color, outline="")
        
        # Dividir texto en líneas
        lines = text.split('\n')
        total_lines = len(lines)
        
        for i, line in enumerate(lines):
            y_offset = (self.height / (total_lines + 1)) * (i + 1)
            self.create_text(self.width/2, y_offset, 
                           text=line, fill=self.text_color,
                           font=('Segoe UI', 9, 'bold'),
                           justify='center')
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event):
        self.command()
        
    def on_enter(self, event):
        self.draw_button(self.get_text())
        self.config(cursor="hand2")
        
    def on_leave(self, event):
        self.draw_button(self.get_text())
        
    def get_text(self):
        # Obtener texto actual del botón
        items = self.find_all()
        text_items = [self.itemcget(item, 'text') for item in items if self.type(item) == 'text']
        return '\n'.join([t for t in text_items if t])

class VistaTablas:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.bingo_actual = None
        self.busqueda_actual = ""
        
        self.colors = {
            'bg_primary': '#0f0f23',
            'bg_secondary': '#1a1a2e', 
            'bg_card': '#16213e',
            'accent_primary': '#00ff88',
            'accent_secondary': '#0099ff',
            'accent_danger': '#ff4757',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'border': '#00ff88'
        }
        
        self.frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crear interfaz moderna de tablas"""
        # Header moderno
        header_frame = tk.Frame(self.frame, bg=self.colors['bg_secondary'], height=100)
        header_frame.pack(fill='x', padx=20, pady=15)
        header_frame.pack_propagate(False)

        # Botón volver
        btn_volver = tk.Button(header_frame,
            text="‹ VOLVER A BINGOS",
            command=self.volver_gestor,
            font=('Segoe UI', 11, 'bold'),
            bg='#2d2d4d',
            fg=self.colors['text_secondary'],
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_volver.pack(side='left', padx=10, pady=10)

        # Información del bingo
        self.lbl_info_bingo = tk.Label(header_frame,
            text="Bingo: [Cargando...]",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_primary']
        )
        self.lbl_info_bingo.pack(side='left', padx=20, pady=10)

        # Búsqueda moderna
        frame_busqueda = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        frame_busqueda.pack(side='right', padx=10, pady=10)

        # Contenedor de búsqueda con estilo moderno
        search_container = tk.Frame(frame_busqueda, bg='#2d2d4d', relief='flat', bd=1)
        search_container.pack()

        lbl_search_icon = tk.Label(search_container,
            text="🔍",
            font=('Segoe UI', 14),
            bg='#2d2d4d',
            fg=self.colors['text_secondary'],
            padx=12,
            pady=8
        )
        lbl_search_icon.pack(side='left')

        self.entry_busqueda = tk.Entry(search_container,
            font=('Segoe UI', 11),
            bg='#2d2d4d',
            fg='white',
            insertbackground='white',
            relief='flat',
            width=25,
            bd=0
        )
        self.entry_busqueda.pack(side='left', padx=5, pady=8)
        self.entry_busqueda.bind('<KeyRelease>', self.filtrar_tablas)

        # Botón limpiar búsqueda
        btn_limpiar = tk.Button(search_container,
            text="✕",
            command=self.limpiar_busqueda,
            font=('Segoe UI', 12, 'bold'),
            bg='#666666',
            fg='white',
            width=3,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_limpiar.pack(side='left', padx=5, pady=2)

        # Barra de herramientas
        toolbar_frame = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        toolbar_frame.pack(fill='x', padx=20, pady=10)

        btn_exportar = tk.Button(toolbar_frame,
            text="📄 GENERAR REPORTE PDF",
            command=self.exportar_pdf,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent_secondary'],
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_exportar.pack(side='left', padx=5)

        btn_reset = tk.Button(toolbar_frame,
            text="🔄 RESETEAR BINGO",
            command=self.resetear_bingo,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent_danger'],
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_reset.pack(side='left', padx=5)

        # Frame principal para tablas
        self.frame_tablas = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        self.frame_tablas.pack(fill='both', expand=True, padx=10, pady=10)

    def crear_tablas(self, bingo):
        """Crear la visualización moderna de tablas"""
        self.bingo_actual = bingo
        self.actualizar_info_bingo()

        # Limpiar frame de tablas
        for widget in self.frame_tablas.winfo_children():
            widget.destroy()

        # Frame contenedor con scroll
        contenedor = tk.Frame(self.frame_tablas, bg=self.colors['bg_primary'])
        contenedor.pack(fill='both', expand=True)

        # Canvas con scrollbar
        self.canvas = tk.Canvas(contenedor, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)

        self.frame_numeros = tk.Frame(self.canvas, bg=self.colors['bg_primary'])

        self.frame_numeros.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame_numeros, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Configurar scroll
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.frame_numeros.bind("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crear botones
        self.crear_botones_numeros()
        self.canvas.bind("<Configure>", self.redimensionar_botones)

    def _on_mousewheel(self, event):
        """Manejar scroll del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def crear_botones_numeros(self):
        """Crear botones de números que ocupen el 100% del ancho"""
        if not self.bingo_actual:
            return

        # Limpiar frame
        for widget in self.frame_numeros.winfo_children():
            widget.destroy()

        # Obtener cartones filtrados
        cartones_filtrados = []
        for numero in range(1, self.bingo_actual.cantidad_cartones + 1):
            if self.cumple_busqueda(numero):
                cartones_filtrados.append(numero)

        if not cartones_filtrados:
            lbl_sin_resultados = tk.Label(self.frame_numeros,
                text="🔍 No se encontraron cartones que coincidan con la búsqueda",
                font=('Segoe UI', 14),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']
            )
            lbl_sin_resultados.pack(pady=50)
            return

        # Siempre 10 columnas para ocupar todo el ancho
        COLUMNAS = 10
        filas = (len(cartones_filtrados) + COLUMNAS - 1) // COLUMNAS

        # Configurar grid para expansión total
        for i in range(filas):
            self.frame_numeros.grid_rowconfigure(i, weight=1)
        for i in range(COLUMNAS):
            self.frame_numeros.grid_columnconfigure(i, weight=1)

        # Calcular dimensiones dinámicas
        canvas_width = max(1200, self.canvas.winfo_width())
        padding_total = 20  # 10px a cada lado
        ancho_disponible = canvas_width - padding_total
        ancho_boton = (ancho_disponible // COLUMNAS) - 2  # -2 para margen entre botones
        alto_boton = 90  # Altura fija adecuada

        # Crear botones en grid
        for idx, numero in enumerate(cartones_filtrados):
            fila = idx // COLUMNAS
            columna = idx % COLUMNAS

            estado = self.bingo_actual.obtener_estado_carton(numero)
            vendido = estado.get('vendido', False)
            nombre = estado.get('nombre', '')

            # Configurar colores según estado
            if vendido:
                texto = f"#{numero}\n✅ {nombre.split()[0] if nombre else 'Vendido'}"
                color_bg = "#27ae60"
                color_hover = "#219a52"
            else:
                texto = f"#{numero}\n🟢 Disponible"
                color_bg = "#3498db"
                color_hover = "#2980b9"

            # Crear botón redondeado
            btn = RoundedButton(
                self.frame_numeros,
                text=texto,
                command=lambda n=numero: self.abrir_modal(n),
                width=ancho_boton,
                height=alto_boton,
                bg_color=color_bg,
                hover_color=color_hover,
                text_color="white",
                corner_radius=20
            )

            # Usar sticky="nsew" para expansión total
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
        """Actualizar la información del bingo"""
        if self.bingo_actual:
            vendidos = self.bingo_actual.obtener_cartones_vendidos()
            ganancias = self.bingo_actual.obtener_ganancias()
            texto = (f"Bingo: {self.bingo_actual.nombre} | "
                    f"Cartones: {len(vendidos)}/{self.bingo_actual.cantidad_cartones} | "
                    f"Precio: ${self.bingo_actual.precio_carton:,.2f} | "
                    f"Ganancias: ${ganancias:,.2f}")
            self.lbl_info_bingo.config(text=texto)

    def abrir_modal(self, numero):
        """Abrir modal para asignar/ver cartón"""
        estado_actual = self.bingo_actual.obtener_estado_carton(numero)

        # Si ya está vendido, mostrar información con opción de cancelar
        if estado_actual.get('vendido', False):
            modal = tk.Toplevel(self.parent)
            modal.title(f"🎫 Información del Cartón #{numero}")
            modal.geometry("500x400")
            modal.configure(bg=self.colors['bg_primary'])
            modal.transient(self.parent)
            modal.grab_set()

            # Centrar el modal
            modal.update_idletasks()
            x = (modal.winfo_screenwidth() // 2) - (500 // 2)
            y = (modal.winfo_screenheight() // 2) - (400 // 2)
            modal.geometry(f"500x400+{x}+{y}")

            frame_modal = tk.Frame(modal, bg=self.colors['bg_primary'], padx=25, pady=25)
            frame_modal.pack(fill="both", expand=True)

            # Icono de cartón vendido
            lbl_icono = tk.Label(frame_modal, text="✅", font=("Arial", 24), 
                               bg=self.colors['bg_primary'], fg='#27ae60')
            lbl_icono.pack(pady=10)

            # Información del cartón
            lbl_titulo = tk.Label(frame_modal, text=f"CARTÓN #{numero} - VENDIDO",
                                font=("Segoe UI", 16, "bold"), 
                                bg=self.colors['bg_primary'], fg='#27ae60')
            lbl_titulo.pack(pady=5)

            lbl_nombre = tk.Label(frame_modal, 
                                text=f"👤 Asignado a: {estado_actual.get('nombre', '')}",
                                font=("Segoe UI", 14), 
                                bg=self.colors['bg_primary'], fg='#ffffff')
            lbl_nombre.pack(pady=15)

            # Frame para botones
            frame_botones = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
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
                                   width=18, height=2, padx=25, pady=20,
                                   relief='flat', cursor="hand2")
            btn_cancelar.pack(side="left", padx=10)

            btn_cerrar = tk.Button(frame_botones, text="👌 CERRAR",
                                 command=modal.destroy,
                                 bg="#95a5a6", fg="white", font=("Segoe UI", 12, "bold"),
                                 width=14, height=2, padx=25, pady=20,
                                 relief='flat', cursor="hand2")
            btn_cerrar.pack(side="left", padx=10)

            return

        # Modal para nueva venta
        modal = tk.Toplevel(self.parent)
        modal.title(f"🎫 Asignar Cartón #{numero}")
        modal.geometry("500x350")
        modal.configure(bg=self.colors['bg_primary'])
        modal.transient(self.parent)
        modal.grab_set()

        # Centrar el modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (350 // 2)
        modal.geometry(f"500x350+{x}+{y}")

        frame_modal = tk.Frame(modal, bg=self.colors['bg_primary'], padx=25, pady=25)
        frame_modal.pack(fill="both", expand=True)

        # Título
        lbl_titulo = tk.Label(frame_modal, text=f"🎫 ASIGNAR CARTÓN #{numero}",
                            font=("Segoe UI", 16, "bold"), 
                            bg=self.colors['bg_primary'], fg='#ffffff')
        lbl_titulo.pack(pady=15)

        # Campo para nombre
        lbl_nombre = tk.Label(frame_modal, text="👤 Nombre completo de la persona:",
                            font=("Segoe UI", 11), 
                            bg=self.colors['bg_primary'], fg='#cccccc')
        lbl_nombre.pack(pady=8)

        entry_nombre = tk.Entry(frame_modal, width=40, font=("Segoe UI", 12),
                              bg='#3d3d3d', fg='white', insertbackground='white',
                              relief='flat')
        entry_nombre.pack(pady=15, ipady=10)
        entry_nombre.focus()

        # Frame para botones
        frame_botones = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
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
                              width=14, height=2, padx=25, pady=20,
                              relief='flat', cursor="hand2")
        btn_asignar.pack(side="left", padx=15)

        btn_cancelar = tk.Button(frame_botones, text="❌ CANCELAR",
                               command=cancelar,
                               bg="#95a5a6", fg="white", font=("Segoe UI", 12, "bold"),
                               width=14, height=2, padx=25, pady=20,
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
        """Redimensionar botones al cambiar tamaño"""
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