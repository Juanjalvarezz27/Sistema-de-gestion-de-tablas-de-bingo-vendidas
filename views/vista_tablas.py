import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
            'accent_warning': '#f39c12',
            'accent_success': '#27ae60',
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

        btn_exportar_pdf = tk.Button(toolbar_frame,
                                   text="📄 EXPORTAR PDF",
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
        btn_exportar_pdf.pack(side='left', padx=5)

        # Nuevos botones de exportar/importar datos
        btn_exportar_datos = tk.Button(toolbar_frame,
                                     text="💾 EXPORTAR DATOS",
                                     command=self.exportar_datos,
                                     font=('Segoe UI', 11, 'bold'),
                                     bg='#9b59b6',
                                     fg='white',
                                     padx=20,
                                     pady=10,
                                     relief='flat',
                                     cursor='hand2',
                                     bd=0
                                     )
        btn_exportar_datos.pack(side='left', padx=5)

        btn_importar_datos = tk.Button(toolbar_frame,
                                     text="📥 IMPORTAR DATOS",
                                     command=self.importar_datos,
                                     font=('Segoe UI', 11, 'bold'),
                                     bg='#3498db',
                                     fg='white',
                                     padx=20,
                                     pady=10,
                                     relief='flat',
                                     cursor='hand2',
                                     bd=0
                                     )
        btn_importar_datos.pack(side='left', padx=5)

        # Nuevo botón para exportar tablas
        btn_exportar_tablas = tk.Button(toolbar_frame,
                                      text="📊 EXPORTAR TABLAS",
                                      command=self.exportar_tablas,
                                      font=('Segoe UI', 11, 'bold'),
                                      bg='#e67e22',
                                      fg='white',
                                      padx=20,
                                      pady=10,
                                      relief='flat',
                                      cursor='hand2',
                                      bd=0
                                      )
        btn_exportar_tablas.pack(side='left', padx=5)

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
        padding_total = 20 # 10px a cada lado
        ancho_disponible = canvas_width - padding_total
        ancho_boton = (ancho_disponible // COLUMNAS) - 2 # -2 para margen entre botones
        alto_boton = 90 # Altura fija adecuada

        # Crear botones en grid
        for idx, numero in enumerate(cartones_filtrados):
            fila = idx // COLUMNAS
            columna = idx % COLUMNAS

            estado = self.bingo_actual.obtener_estado_carton(numero)
            vendido = estado.get('vendido', False)
            apartado = estado.get('apartado', False)
            nombre = estado.get('nombre', '')

            # Configurar colores según estado
            if vendido:
                texto = f"#{numero}\n✅ {nombre.split()[0] if nombre else 'Vendido'}"
                color_bg = "#27ae60"
                color_hover = "#219a52"
            elif apartado:
                texto = f"#{numero}\n⏳ {nombre.split()[0] if nombre else 'Apartado'}"
                color_bg = "#f39c12" # Color naranja para apartados
                color_hover = "#e67e22"
            else:
                texto = f"#{numero}\n🟢 Disponible"
                color_bg = "#3498db"
                color_hover = "#2980b9"

            # Crear botón redondeado - CAMBIO IMPORTANTE: usar abrir_modal_carton
            btn = RoundedButton(
                self.frame_numeros,
                text=texto,
                command=lambda n=numero: self.abrir_modal_carton(n),
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
        if (estado.get('vendido', False) or estado.get('apartado', False)) and busqueda in estado.get('nombre', '').lower():
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
            try:
                vendidos = self.bingo_actual.obtener_cartones_vendidos()
                apartados = self.bingo_actual.obtener_cartones_apartados()
                ganancias = self.bingo_actual.obtener_ganancias()
                texto = (f"Bingo: {self.bingo_actual.nombre} | "
                        f"Cartones: {len(vendidos)}/{self.bingo_actual.cantidad_cartones} | "
                        f"Apartados: {len(apartados)} | "
                        f"Precio: ${self.bingo_actual.precio_carton:,.2f} | "
                        f"Ganancias: ${ganancias:,.2f}")
                self.lbl_info_bingo.config(text=texto)
            except Exception as e:
                print(f"Error actualizando info bingo: {e}")
                texto = f"Bingo: {self.bingo_actual.nombre} | Error cargando información"
                self.lbl_info_bingo.config(text=texto)

    def abrir_modal_carton(self, numero):
        """Abrir modal para mostrar el cartón con formato de tabla"""
        if not self.bingo_actual:
            return
        
        # Obtener los datos del cartón
        carton_data = self.bingo_actual.obtener_carton(numero)
        estado_actual = self.bingo_actual.obtener_estado_carton(numero)
        
        # Crear modal - REDUCIDO EN ALTURA
        modal = tk.Toplevel(self.parent)
        modal.title(f"🎫 Cartón #{numero}")
        modal.geometry("500x550")  # REDUCIDO DE 650 a 550
        modal.configure(bg=self.colors['bg_primary'])
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centrar el modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (550 // 2)
        modal.geometry(f"500x550+{x}+{y}")
        
        frame_modal = tk.Frame(modal, bg=self.colors['bg_primary'], padx=15, pady=15)  # REDUCIDO PADDING
        frame_modal.pack(fill="both", expand=True)
        
        # Header con información del cartón - REDUCIDO ESPACIADO
        header_frame = tk.Frame(frame_modal, bg=self.colors['bg_secondary'], pady=8)  # REDUCIDO PADDING
        header_frame.pack(fill="x", pady=(0, 10))  # REDUCIDO MARGEN
        
        lbl_titulo = tk.Label(header_frame, 
                             text=f"🎫 Cartón #{numero}",
                             font=("Segoe UI", 16, "bold"),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['accent_primary'])
        lbl_titulo.pack()
        
        # Mostrar estado
        estado_texto = ""
        estado_color = ""
        if estado_actual.get('vendido', False):
            estado_texto = f"✅ VENDIDO a: {estado_actual.get('nombre', '')}"
            estado_color = "#27ae60"
        elif estado_actual.get('apartado', False):
            estado_texto = f"⏳ APARTADO por: {estado_actual.get('nombre', '')}"
            estado_color = "#f39c12"
        else:
            estado_texto = "🟢 DISPONIBLE"
            estado_color = "#3498db"
        
        lbl_estado = tk.Label(header_frame,
                             text=estado_texto,
                             font=("Segoe UI", 12),
                             bg=self.colors['bg_secondary'],
                             fg=estado_color)
        lbl_estado.pack(pady=3)  # REDUCIDO PADDING
        
        # Frame para la tabla del cartón - REDUCIDO ESPACIADO
        frame_tabla = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
        frame_tabla.pack(pady=10)  # REDUCIDO MARGEN
        
        # Crear la tabla del cartón
        self.crear_tabla_carton_compacta(frame_tabla, carton_data)
        
        # Frame para botones de acción - BOTONES UNO AL LADO DEL OTRO
        frame_botones = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
        frame_botones.pack(pady=15, fill='x')  # AUMENTADO MARGEN PARA BOTONES GRANDES
        
        # Lógica de botones según el estado actual - UNO AL LADO DEL OTRO
        if estado_actual.get('vendido', False):
            # Cartón VENDIDO - Solo puede liberarse
            btn_liberar = tk.Button(frame_botones,
                                  text="🔄 LIBERAR CARTÓN",
                                  command=lambda: self.liberar_carton(numero, modal),
                                  bg=self.colors['accent_warning'],
                                  fg='white',
                                  font=("Segoe UI", 12, "bold"),  # TEXTO MÁS GRANDE
                                  padx=25,  # MÁS PADDING
                                  pady=15,  # MÁS PADDING
                                  relief='flat',
                                  cursor='hand2')
            btn_liberar.pack(side='left', padx=10, pady=5, fill='x', expand=True)  # UNO AL LADO DEL OTRO
            
        elif estado_actual.get('apartado', False):
            # Cartón APARTADO - Puede venderse o liberarse
            btn_vender = tk.Button(frame_botones,
                                 text="✅ VENDIDO",
                                 command=lambda: self.cambiar_a_vendido(numero, estado_actual.get('nombre', ''), modal),
                                 bg=self.colors['accent_success'],
                                 fg='white',
                                 font=("Segoe UI", 12, "bold"),  # TEXTO MÁS GRANDE
                                 padx=25,  # MÁS PADDING
                                 pady=15,  # MÁS PADDING
                                 relief='flat',
                                 cursor='hand2')
            btn_vender.pack(side='left', padx=10, pady=5, fill='x', expand=True)  # UNO AL LADO DEL OTRO
            
            btn_liberar = tk.Button(frame_botones,
                                  text="🔄 LIBERAR CARTÓN",
                                  command=lambda: self.liberar_carton(numero, modal),
                                  bg=self.colors['accent_warning'],
                                  fg='white',
                                  font=("Segoe UI", 12, "bold"),  # TEXTO MÁS GRANDE
                                  padx=25,  # MÁS PADDING
                                  pady=15,  # MÁS PADDING
                                  relief='flat',
                                  cursor='hand2')
            btn_liberar.pack(side='left', padx=10, pady=5, fill='x', expand=True)  # UNO AL LADO DEL OTRO
            
        else:
            # Cartón DISPONIBLE - Puede apartarse o venderse
            btn_apartar = tk.Button(frame_botones,
                                  text="⏳ APARTAR CARTÓN",
                                  command=lambda: self.abrir_modal_asignacion(numero, "apartado", modal),
                                  bg=self.colors['accent_warning'],
                                  fg='white',
                                  font=("Segoe UI", 12, "bold"),  # TEXTO MÁS GRANDE
                                  padx=25,  # MÁS PADDING
                                  pady=15,  # MÁS PADDING
                                  relief='flat',
                                  cursor='hand2')
            btn_apartar.pack(side='left', padx=10, pady=5, fill='x', expand=True)  # UNO AL LADO DEL OTRO
            
            btn_vender = tk.Button(frame_botones,
                                 text="✅ VENDER CARTÓN",
                                 command=lambda: self.abrir_modal_asignacion(numero, "vendido", modal),
                                 bg=self.colors['accent_success'],
                                 fg='white',
                                 font=("Segoe UI", 12, "bold"),  # TEXTO MÁS GRANDE
                                 padx=25,  # MÁS PADDING
                                 pady=15,  # MÁS PADDING
                                 relief='flat',
                                 cursor='hand2')
            btn_vender.pack(side='left', padx=10, pady=5, fill='x', expand=True)  # UNO AL LADO DEL OTRO
        
        # Botón cerrar - SIEMPRE A LA DERECHA
        btn_cerrar = tk.Button(frame_botones,
                              text="❌ CERRAR",
                              command=modal.destroy,
                              bg=self.colors['accent_danger'],
                              fg='white',
                              font=("Segoe UI", 12, "bold"),  # TEXTO MÁS GRANDE
                              padx=25,  # MÁS PADDING
                              pady=15,  # MÁS PADDING
                              relief='flat',
                              cursor='hand2')
        btn_cerrar.pack(side='right', padx=10, pady=5)  # SIEMPRE A LA DERECHA

    def crear_tabla_carton_compacta(self, parent, carton_data):
        """Crear la representación visual COMPACTA del cartón en formato de tabla"""
        # Frame principal de la tabla - MÁS COMPACTO
        frame_tabla_principal = tk.Frame(parent, bg='#2d2d4d', padx=8, pady=8)  # REDUCIDO PADDING
        frame_tabla_principal.pack(pady=5)  # REDUCIDO MARGEN
        
        # Título B I N G O con estilo mejorado - MÁS COMPACTO
        frame_header = tk.Frame(frame_tabla_principal, bg='#2d2d4d')
        frame_header.pack()
        
        letras = ['B', 'I', 'N', 'G', 'O']
        colores_letras = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for i, (letra, color) in enumerate(zip(letras, colores_letras)):
            celda = tk.Frame(frame_header, bg=color, width=60, height=30, relief='raised', bd=1)  # REDUCIDO TAMAÑO
            celda.pack_propagate(False)
            celda.grid(row=0, column=i, padx=1, pady=1)  # REDUCIDO PADDING
            
            lbl = tk.Label(celda, 
                          text=letra,
                          font=("Segoe UI", 14, "bold"),  # TEXTO MÁS PEQUEÑO
                          bg=color,
                          fg='#2d2d4d')
            lbl.pack(expand=True, fill='both')
        
        # Crear filas de números con estilo mejorado - MÁS COMPACTO
        for fila in range(5):
            frame_fila = tk.Frame(frame_tabla_principal, bg='#2d2d4d')
            frame_fila.pack()
            
            for col, (letra, color) in enumerate(zip(letras, colores_letras)):
                clave = f'{letra}{fila+1}'
                valor = carton_data.get(clave, '')
                
                # Casilla especial FREE
                if clave == 'N3':
                    bg_color = '#FFEAA7'
                    fg_color = '#2d2d4d'
                    texto = 'FREE'
                    font_size = 10  # TEXTO MÁS PEQUEÑO
                else:
                    bg_color = 'white'
                    fg_color = '#2d2d4d'
                    texto = str(valor)
                    font_size = 12  # TEXTO MÁS PEQUEÑO
                
                celda = tk.Frame(frame_fila, bg=color, width=60, height=45, relief='solid', bd=1)  # REDUCIDO TAMAÑO
                celda.pack_propagate(False)
                celda.grid(row=0, column=col, padx=1, pady=1)  # REDUCIDO PADDING
                
                lbl = tk.Label(celda,
                              text=texto,
                              font=("Segoe UI", font_size, "bold"),
                              bg=bg_color,
                              fg=fg_color)
                lbl.pack(expand=True, fill='both')

    def liberar_carton(self, numero, modal):
        """Liberar un cartón (volver a disponible)"""
        if self.bingo_actual.liberar_carton(numero):
            modal.destroy()
            self.crear_botones_numeros()
            self.actualizar_info_bingo()
            messagebox.showinfo("Éxito", f"✅ Cartón #{numero} liberado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo liberar el cartón")

    def cambiar_a_vendido(self, numero, nombre, modal):
        """Cambiar un cartón de apartado a vendido"""
        if self.bingo_actual.vender_carton(numero, nombre):
            modal.destroy()
            self.crear_botones_numeros()
            self.actualizar_info_bingo()
            messagebox.showinfo("Éxito", f"✅ Cartón #{numero} marcado como VENDIDO")
        else:
            messagebox.showerror("Error", "No se pudo cambiar el estado del cartón")

    def abrir_modal_asignacion(self, numero, tipo, modal_actual=None):
        """Abrir modal para asignar cartón (apartar o vender)"""
        if modal_actual:
            modal_actual.destroy()
            
        modal = tk.Toplevel(self.parent)
        modal.title(f"🎫 {'Vender' if tipo == 'vendido' else 'Apartar'} Cartón #{numero}")
        modal.geometry("500x300")  # MODAL MÁS COMPACTO
        modal.configure(bg=self.colors['bg_primary'])
        modal.transient(self.parent)
        modal.grab_set()

        # Centrar el modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (300 // 2)
        modal.geometry(f"500x300+{x}+{y}")

        frame_modal = tk.Frame(modal, bg=self.colors['bg_primary'], padx=20, pady=20)
        frame_modal.pack(fill="both", expand=True)

        # Título
        titulo_texto = f"🎫 {'VENDER' if tipo == 'vendido' else 'APARTAR'} CARTÓN #{numero}"
        lbl_titulo = tk.Label(frame_modal, text=titulo_texto,
                            font=("Segoe UI", 16, "bold"),
                            bg=self.colors['bg_primary'], fg='#ffffff')
        lbl_titulo.pack(pady=10)  # REDUCIDO PADDING

        # Campo para nombre
        lbl_nombre = tk.Label(frame_modal, text="👤 Nombre completo de la persona:",
                            font=("Segoe UI", 11),
                            bg=self.colors['bg_primary'], fg='#cccccc')
        lbl_nombre.pack(pady=5)  # REDUCIDO PADDING

        entry_nombre = tk.Entry(frame_modal, width=40, font=("Segoe UI", 12),
                              bg='#3d3d3d', fg='white', insertbackground='white',
                              relief='flat')
        entry_nombre.pack(pady=10, ipady=8)  # REDUCIDO PADDING
        entry_nombre.focus()

        # Frame para botones de acción - BOTONES UNO AL LADO DEL OTRO
        frame_botones = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
        frame_botones.pack(pady=20, fill='x')

        def asignar_carton():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "❌ Por favor ingrese un nombre")
                return

            if tipo == "vendido":
                self.bingo_actual.asignar_carton(numero, nombre)
            else:
                self.bingo_actual.apartar_carton(numero, nombre)

            modal.destroy()
            self.crear_botones_numeros()
            self.actualizar_info_bingo()

            estado_texto = "VENDIDO" if tipo == "vendido" else "APARTADO"
            messagebox.showinfo("Éxito", f"✅ Cartón #{numero} {estado_texto.lower()} a:\n{nombre}")

        def cancelar():
            modal.destroy()

        # Botones UNO AL LADO DEL OTRO
        btn_texto = "✅ VENDER" if tipo == "vendido" else "⏳ APARTAR"
        btn_asignar = tk.Button(frame_botones, text=btn_texto,
                              command=asignar_carton,
                              bg="#27ae60" if tipo == "vendido" else "#f39c12",
                              fg="white", font=("Segoe UI", 12, "bold"),
                              padx=25,  # MÁS PADDING
                              pady=15,  # MÁS PADDING
                              relief='flat', cursor="hand2")
        btn_asignar.pack(side='left', padx=10, pady=5, fill='x', expand=True)  # UNO AL LADO DEL OTRO

        btn_cancelar = tk.Button(frame_botones, text="❌ CANCELAR",
                               command=cancelar,
                               bg="#95a5a6", fg="white", font=("Segoe UI", 12, "bold"),
                               padx=25,  # MÁS PADDING
                               pady=15,  # MÁS PADDING
                               relief='flat', cursor="hand2")
        btn_cancelar.pack(side='right', padx=10, pady=5)  # A LA DERECHA

        # Enter para asignar, Escape para cancelar
        modal.bind('<Return>', lambda e: asignar_carton())
        modal.bind('<Escape>', lambda e: cancelar())

        modal.focus_force()
        entry_nombre.focus()

    # ... (el resto de los métodos se mantiene igual)

    def exportar_tablas(self):
        """Exportar todas las tablas del bingo a Excel"""
        if self.bingo_actual:
            self.bingo_actual.exportar_tablas_excel()

    def abrir_modal(self, numero):
        """Abrir modal para asignar/ver cartón (modal original de asignación)"""
        estado_actual = self.bingo_actual.obtener_estado_carton(numero)

        # Si ya está vendido o apartado, redirigir al modal de visualización
        if estado_actual.get('vendido', False) or estado_actual.get('apartado', False):
            self.abrir_modal_carton(numero)
            return

        # Si está disponible, abrir modal de asignación
        self.abrir_modal_asignacion(numero, "vendido")

    def exportar_datos(self):
        """Exportar datos del bingo a archivo JSON"""
        if not self.bingo_actual:
            messagebox.showerror("Error", "No hay bingo activo")
            return

        try:
            # Obtener la carpeta de descargas
            from utils.helpers import obtener_carpeta_descargas
            downloads_path = obtener_carpeta_descargas()

            # Crear nombre de archivo
            nombre_archivo = f"backup_{self.bingo_actual.nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            ruta_archivo = downloads_path / nombre_archivo

            # Obtener todos los datos del bingo
            datos_exportar = {
                'nombre': self.bingo_actual.nombre,
                'cantidad_cartones': self.bingo_actual.cantidad_cartones,
                'precio_carton': self.bingo_actual.precio_carton,
                'cartones_vendidos': self.bingo_actual.cartones_vendidos,
                'cartones_apartados': self.bingo_actual.cartones_apartados,
                'cartones_generados': self.bingo_actual.cartones_generados,
                'fecha_exportacion': datetime.now().isoformat(),
                'version': '1.0'
            }

            # Guardar en archivo JSON
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_exportar, f, indent=2, ensure_ascii=False)

            messagebox.showinfo(
                "Exportación Exitosa",
                f"✅ Datos exportados correctamente:\n\n"
                f"📁 {nombre_archivo}\n\n"
                f"💾 Guardado en: {ruta_archivo}\n\n"
                f"📊 Cartones vendidos: {len(self.bingo_actual.cartones_vendidos)}\n"
                f"⏳ Cartones apartados: {len(self.bingo_actual.cartones_apartados)}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error exportando datos: {e}")

    def importar_datos(self):
        """Importar datos desde archivo JSON"""
        if not self.bingo_actual:
            messagebox.showerror("Error", "No hay bingo activo")
            return

        try:
            # Abrir diálogo para seleccionar archivo
            archivo = filedialog.askopenfilename(
                title="Seleccionar archivo de datos",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
                defaultextension=".json"
            )

            if not archivo:
                return

            # Leer el archivo JSON
            with open(archivo, 'r', encoding='utf-8') as f:
                datos_importar = json.load(f)

            # Validar que el archivo sea compatible
            if 'cartones_vendidos' not in datos_importar or 'cartones_apartados' not in datos_importar:
                messagebox.showerror("Error", "El archivo seleccionado no es un archivo de datos válido")
                return

            # Confirmar importación
            confirmacion = messagebox.askyesno(
                "Confirmar Importación",
                f"¿Estás seguro de importar los datos?\n\n"
                f"📋 Bingo: {datos_importar.get('nombre', 'Desconocido')}\n"
                f"🎫 Cartones vendidos: {len(datos_importar['cartones_vendidos'])}\n"
                f"⏳ Cartones apartados: {len(datos_importar['cartones_apartados'])}\n\n"
                f"⚠️ Esta acción sobrescribirá los datos actuales del bingo."
            )

            if not confirmacion:
                return

            # Aplicar los datos importados
            self.bingo_actual.cartones_vendidos = datos_importar['cartones_vendidos']
            self.bingo_actual.cartones_apartados = datos_importar['cartones_apartados']
            # También importar cartones generados si existen
            if 'cartones_generados' in datos_importar:
                self.bingo_actual.cartones_generados = datos_importar['cartones_generados']

            # Guardar los cambios
            self.bingo_actual.guardar_datos()

            # Actualizar la interfaz
            self.crear_botones_numeros()
            self.actualizar_info_bingo()

            messagebox.showinfo(
                "Importación Exitosa",
                f"✅ Datos importados correctamente:\n\n"
                f"📊 Cartones vendidos: {len(self.bingo_actual.cartones_vendidos)}\n"
                f"⏳ Cartones apartados: {len(self.bingo_actual.cartones_apartados)}\n"
                f"💰 Ganancias actualizadas: ${self.bingo_actual.obtener_ganancias():,.2f}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error importando datos: {e}")

    def exportar_pdf(self):
        """Exportar reporte PDF del bingo actual"""
        if self.bingo_actual:
            self.bingo_actual.exportar_pdf()

    def resetear_bingo(self):
        """Resetear el bingo actual"""
        if self.bingo_actual and messagebox.askyesno("Confirmar",
                "¿Estás seguro de resetear todos los cartones?\n\n"
                "Esta acción liberará todos los cartones vendidos y apartados."):
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