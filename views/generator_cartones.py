import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pathlib import Path
import time
import webbrowser
import sys

# Manejo robusto de importaciones de PIL
try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    PIL_AVAILABLE = True
    print("✅ PIL cargado correctamente")
except ImportError as e:
    PIL_AVAILABLE = False
    print(f"⚠️ PIL no disponible: {e}")
    # Crear clases dummy para evitar errores
    class DummyImage:
        def __init__(self, *args, **kwargs): pass
        def save(self, *args, **kwargs): pass
    class DummyImageDraw:
        def __init__(self, *args, **kwargs): pass
        def text(self, *args, **kwargs): pass
        def rectangle(self, *args, **kwargs): pass
        def textbbox(self, *args, **kwargs): return [0, 0, 0, 0]
    class DummyImageFont:
        @staticmethod
        def truetype(*args, **kwargs): return None
        @staticmethod
        def load_default(): return None
    
    Image = DummyImage
    ImageDraw = DummyImageDraw
    ImageFont = DummyImageFont
    ImageOps = DummyImage

class GeneradorCartones:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.bingo_actual = None
        
        self.colors = {
            'bg_primary': '#0f0f23',
            'bg_secondary': '#1a1a2e',
            'bg_card': '#16213e',
            'accent_primary': '#00ff88',
            'accent_secondary': '#0099ff',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
        }
        
        self.background_path = None
        self.logo_path = None
        
    def abrir_modal_generador(self, bingo):
        """Abrir modal para generar cartones personalizados"""
        self.bingo_actual = bingo
        
        # Crear modal MÁS ANCHO
        self.modal = tk.Toplevel(self.parent)
        self.modal.title("🎨 Generar Cartones Personalizados")
        self.modal.geometry("1200x700")  # MÁS ANCHO para dos columnas
        self.modal.configure(bg=self.colors['bg_primary'])
        self.modal.transient(self.parent)
        self.modal.grab_set()
        self.modal.resizable(False, False)
        
        # Centrar el modal
        self.modal.update_idletasks()
        x = (self.modal.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.modal.winfo_screenheight() // 2) - (700 // 2)
        self.modal.geometry(f"1200x700+{x}+{y}")
        
        # Frame principal con dos columnas
        frame_principal = tk.Frame(self.modal, bg=self.colors['bg_primary'], padx=30, pady=30)
        frame_principal.pack(fill="both", expand=True)
        
        # Configurar grid para dos columnas
        frame_principal.grid_columnconfigure(0, weight=0)  # Columna izquierda (controles) - no expandir
        frame_principal.grid_columnconfigure(1, weight=1)  # Columna derecha (preview) - expandir
        frame_principal.grid_rowconfigure(0, weight=1)
        
        # COLUMNA IZQUIERDA - CONTROLES (más estrecha)
        frame_controles = tk.Frame(frame_principal, bg=self.colors['bg_primary'], width=400)
        frame_controles.grid(row=0, column=0, padx=(0, 30), sticky="nsew")
        frame_controles.grid_propagate(False)  # Mantener ancho fijo
        
        # Título
        titulo = tk.Label(frame_controles, 
                         text="🎨 GENERAR CARTONES PERSONALIZADOS",
                         font=("Segoe UI", 16, "bold"),
                         bg=self.colors['bg_primary'],
                         fg=self.colors['accent_primary'],
                         wraplength=350)
        titulo.pack(pady=(0, 20))
        
        # Información del bingo
        info_text = f"Bingo: {bingo.nombre} | Cartones: {bingo.cantidad_cartones}"
        lbl_info = tk.Label(frame_controles, 
                           text=info_text,
                           font=("Segoe UI", 12),
                           bg=self.colors['bg_primary'],
                           fg=self.colors['text_secondary'])
        lbl_info.pack(pady=(0, 30))
        
        # Advertencia si PIL no está disponible
        if not PIL_AVAILABLE:
            lbl_advertencia = tk.Label(frame_controles,
                                     text="⚠️ MODO HTML ACTIVADO\n(PIL no disponible - Se usarán cartones HTML)",
                                     font=("Segoe UI", 10, "bold"),
                                     bg='#f39c12',
                                     fg='white',
                                     pady=10,
                                     justify='center')
            lbl_advertencia.pack(fill="x", pady=(0, 20))
        
        # Sección de fondo personalizado
        self.crear_seccion_archivo(frame_controles, 
                                  "Fondo Personalizado", 
                                  "background",
                                  "Seleccionar imagen de fondo...")
        
        # Sección de logo
        self.crear_seccion_archivo(frame_controles, 
                                  "Logo de Empresa", 
                                  "logo",
                                  "Seleccionar logo...")
        
        # Sección de cantidad - MÁS ALTO
        frame_cantidad = tk.Frame(frame_controles, bg=self.colors['bg_primary'])
        frame_cantidad.pack(fill="x", pady=25)  # Más espacio
        
        lbl_cantidad = tk.Label(frame_cantidad,
                              text="Cantidad de cartones a generar:",
                              font=("Segoe UI", 12, "bold"),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        lbl_cantidad.pack(anchor="w", pady=(0, 12))
        
        frame_entrada = tk.Frame(frame_cantidad, bg=self.colors['bg_primary'])
        frame_entrada.pack(fill="x")
        
        # Frame para alinear entrada y botón a la misma altura
        frame_entrada_botones = tk.Frame(frame_entrada, bg=self.colors['bg_primary'])
        frame_entrada_botones.pack(fill="x")
        
        self.entry_cantidad = tk.Entry(frame_entrada_botones,
                                     font=("Segoe UI", 12),
                                     bg='#2d2d4d',
                                     fg='white',
                                     insertbackground='white',
                                     relief='flat',
                                     width=15)
        self.entry_cantidad.pack(side="left", padx=(0, 10))
        self.entry_cantidad.insert(0, str(min(50, bingo.cantidad_cartones)))
        
        btn_maximo = tk.Button(frame_entrada_botones,
                             text="MÁXIMO",
                             command=self.establecer_maximo,
                             font=("Segoe UI", 10, "bold"),
                             bg='#9b59b6',
                             fg='white',
                             padx=20,
                             pady=10,  # Más alto para igualar botones
                             relief='flat',
                             cursor='hand2')
        btn_maximo.pack(side="left")
        
        # Botones de acción - MEJOR DISTRIBUCIÓN
        self.crear_botones_accion(frame_controles)
        
        # COLUMNA DERECHA - PREVIEW (más ancha)
        frame_preview = tk.Frame(frame_principal, bg=self.colors['bg_primary'])
        frame_preview.grid(row=0, column=1, sticky="nsew")
        
        # Título del preview
        lbl_preview_titulo = tk.Label(frame_preview,
                                    text="VISTA PREVIA DEL CARTÓN",
                                    font=("Segoe UI", 16, "bold"),
                                    bg=self.colors['bg_primary'],
                                    fg=self.colors['accent_primary'])
        lbl_preview_titulo.pack(pady=(0, 20))
        
        # Frame para el preview más grande
        frame_preview_container = tk.Frame(frame_preview, bg='#2d2d4d', relief='sunken', bd=2, width=650, height=550)
        frame_preview_container.pack(pady=10, fill="both", expand=True)
        frame_preview_container.pack_propagate(False)
        
        # Canvas para el preview MÁS GRANDE
        self.canvas_preview = tk.Canvas(frame_preview_container, 
                                      bg='#1a1a2e', 
                                      highlightthickness=0,
                                      width=650, 
                                      height=550)
        self.canvas_preview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información del preview
        lbl_info_preview = tk.Label(frame_preview,
                                  text="• Diseño moderno y elegante\n• Solo tabla y número del cartón\n• Fondo y logo personalizables",
                                  font=("Segoe UI", 11),
                                  bg=self.colors['bg_primary'],
                                  fg=self.colors['text_secondary'],
                                  justify='left')
        lbl_info_preview.pack(pady=15)
        
        # Dibujar preview inicial
        self.dibujar_preview_carton()
    
    def crear_seccion_archivo(self, parent, titulo, tipo, placeholder):
        """Crear sección para seleccionar archivo"""
        frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        frame.pack(fill="x", pady=15)
        
        # Título de la sección
        lbl_titulo = tk.Label(frame,
                            text=titulo,
                            font=("Segoe UI", 12, "bold"),
                            bg=self.colors['bg_primary'],
                            fg=self.colors['text_primary'])
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        # Frame para botón y label
        frame_archivo = tk.Frame(frame, bg=self.colors['bg_primary'])
        frame_archivo.pack(fill="x")
        
        # Botón seleccionar
        btn_seleccionar = tk.Button(frame_archivo,
                                  text="📁 SELECCIONAR",
                                  command=lambda: self.seleccionar_archivo(tipo),
                                  font=("Segoe UI", 10, "bold"),
                                  bg=self.colors['accent_secondary'],
                                  fg='white',
                                  padx=20,
                                  pady=8,
                                  relief='flat',
                                  cursor='hand2')
        btn_seleccionar.pack(side="left")
        
        # Label con la ruta del archivo
        texto_archivo = tk.StringVar()
        texto_archivo.set(placeholder)
        
        lbl_archivo = tk.Label(frame_archivo,
                             textvariable=texto_archivo,
                             font=("Segoe UI", 10),
                             bg=self.colors['bg_primary'],
                             fg=self.colors['text_secondary'],
                             wraplength=250,  # Ajustado para columna más estrecha
                             justify='left')
        lbl_archivo.pack(side="left", padx=(15, 0), fill="x", expand=True)
        
        # Botón limpiar
        btn_limpiar = tk.Button(frame_archivo,
                              text="✕",
                              command=lambda: self.limpiar_archivo(tipo),
                              font=("Segoe UI", 10, "bold"),
                              bg='#666666',
                              fg='white',
                              width=3,
                              relief='flat',
                              cursor='hand2')
        btn_limpiar.pack(side="right")
        
        # Guardar referencia al label
        if tipo == "background":
            self.lbl_background = texto_archivo
        else:
            self.lbl_logo = texto_archivo
    
    def crear_botones_accion(self, parent):
        """Crear botones de acción - MEJOR DISTRIBUCIÓN"""
        frame_botones = tk.Frame(parent, bg=self.colors['bg_primary'])
        frame_botones.pack(fill="x", pady=30)
        
        # Frame para botones en línea
        frame_botones_linea = tk.Frame(frame_botones, bg=self.colors['bg_primary'])
        frame_botones_linea.pack(fill="x")
        
        # Botón generar - texto dinámico según disponibilidad de PIL
        if PIL_AVAILABLE:
            btn_texto = "🎨 GENERAR CARTONES PNG"
        else:
            btn_texto = "🎨 GENERAR CARTONES HTML"
            
        btn_generar = tk.Button(frame_botones_linea,
                              text=btn_texto,
                              command=self.iniciar_generacion,
                              font=("Segoe UI", 12, "bold"),
                              bg=self.colors['accent_primary'],
                              fg='#0f0f23',
                              padx=20,
                              pady=12,
                              relief='flat',
                              cursor='hand2')
        btn_generar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón cancelar - MEJOR ESTILO
        btn_cancelar = tk.Button(frame_botones_linea,
                               text="❌ CERRAR",
                               command=self.modal.destroy,
                               font=("Segoe UI", 12, "bold"),
                               bg='#e74c3c',
                               fg='white',
                               padx=20,
                               pady=12,
                               relief='flat',
                               cursor='hand2')
        btn_cancelar.pack(side="right", fill="x", expand=True, padx=(10, 0))
    
    def seleccionar_archivo(self, tipo):
        """Seleccionar archivo de imagen"""
        tipos_archivo = [
            ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("Todos los archivos", "*.*")
        ]
        
        archivo = filedialog.askopenfilename(
            title=f"Seleccionar {tipo}",
            filetypes=tipos_archivo
        )
        
        if archivo:
            if tipo == "background":
                self.background_path = archivo
                self.lbl_background.set(os.path.basename(archivo))
            else:
                self.logo_path = archivo
                self.lbl_logo.set(os.path.basename(archivo))
            
            self.actualizar_preview()
    
    def limpiar_archivo(self, tipo):
        """Limpiar archivo seleccionado"""
        if tipo == "background":
            self.background_path = None
            self.lbl_background.set("Seleccionar imagen de fondo...")
        else:
            self.logo_path = None
            self.lbl_logo.set("Seleccionar logo...")
        
        self.actualizar_preview()
    
    def establecer_maximo(self):
        """Establecer cantidad máxima de cartones"""
        if self.bingo_actual:
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, str(self.bingo_actual.cantidad_cartones))
    
    def dibujar_preview_carton(self):
        """Dibujar preview del cartón en el canvas - DISEÑO MEJORADO"""
        self.canvas_preview.delete("all")
        
        # Dimensiones del canvas
        canvas_width = 650
        canvas_height = 550
        
        # Margen para el cartón
        margin = 40
        carton_width = canvas_width - (2 * margin)
        carton_height = canvas_height - (2 * margin)
        
        # Dibujar fondo del canvas
        self.canvas_preview.create_rectangle(0, 0, canvas_width, canvas_height, fill='#1a1a2e', outline='')
        
        # Dibujar cartón con esquinas redondeadas (simuladas)
        self.canvas_preview.create_rectangle(margin, margin, 
                                           margin + carton_width, margin + carton_height,
                                           fill='#ffffff', outline='#e0e0e0', width=2)
        
        # Dibujar header BINGO con diseño moderno
        letras = ['B', 'I', 'N', 'G', 'O']
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFD93D']
        
        ancho_celda = carton_width / 5
        alto_header = carton_height * 0.18  # Header más alto para diseño moderno
        
        # Header BINGO con diseño moderno
        for i, (letra, color) in enumerate(zip(letras, colores)):
            x1 = margin + (i * ancho_celda)
            x2 = x1 + ancho_celda
            y1 = margin
            y2 = margin + alto_header
            
            # Celda de letra con gradiente simulado
            self.canvas_preview.create_rectangle(x1, y1, x2, y2, 
                                               fill=color, outline='#ffffff', width=2)
            
            # Texto de letra moderno
            self.canvas_preview.create_text(x1 + ancho_celda/2, y1 + alto_header/2,
                                          text=letra, font=('Arial', 24, 'bold'),
                                          fill='white')
        
        # Obtener datos del cartón de ejemplo para el preview
        try:
            carton_data = self.bingo_actual.obtener_carton(1)
        except:
            # Si no se puede obtener un cartón real, usar datos de ejemplo
            carton_data = {}
            for letra in letras:
                for i in range(1, 6):
                    carton_data[f'{letra}{i}'] = (ord(letra) - 64) * 10 + i
        
        # Dibujar celdas de números
        alto_celda = (carton_height - alto_header) / 5
        
        for fila in range(5):
            for col, letra in enumerate(letras):
                x1 = margin + (col * ancho_celda)
                x2 = x1 + ancho_celda
                y1 = margin + alto_header + (fila * alto_celda)
                y2 = y1 + alto_celda
                
                # Celda FREE en el centro con fondo BLANCO
                if fila == 2 and col == 2:
                    # Fondo BLANCO para FREE (donde va el logo)
                    self.canvas_preview.create_rectangle(x1, y1, x2, y2,
                                                       fill='#ffffff', outline='#e0e0e0', width=2)
                    
                    # Texto FREE elegante en gris claro
                    self.canvas_preview.create_text(x1 + ancho_celda/2, y1 + alto_celda/2,
                                                  text='FREE', font=('Arial', 14, 'bold'),
                                                  fill='#888888')
                    
                    # Indicar que aquí va el logo
                    if self.logo_path:
                        self.canvas_preview.create_text(x1 + ancho_celda/2, y1 + alto_celda/2 + 20,
                                                      text='(Logo aquí)', font=('Arial', 9, 'italic'),
                                                      fill='#666666')
                else:
                    # Celdas normales con diseño limpio
                    self.canvas_preview.create_rectangle(x1, y1, x2, y2,
                                                       fill='#f8f9fa', outline='#e0e0e0', width=1)
                    
                    # Obtener el número REAL del cartón
                    clave = f'{letra}{fila+1}'
                    valor = carton_data.get(clave, '')
                    
                    # Mostrar el número real
                    self.canvas_preview.create_text(x1 + ancho_celda/2, y1 + alto_celda/2,
                                                  text=str(valor), font=('Arial', 16, 'bold'),
                                                  fill='#2d2d4d')
        
        # NUEVO DISEÑO: Número del cartón en esquina superior derecha - CUADRADO PERFECTO
        square_size = 40  # Tamaño del cuadrado
        numero_carton_x = margin + carton_width - 25  # Más hacia la esquina
        numero_carton_y = margin + 25  # Más hacia la esquina
        
        # Cuadrado perfecto
        self.canvas_preview.create_rectangle(
            numero_carton_x - square_size/2, 
            numero_carton_y - square_size/2,
            numero_carton_x + square_size/2, 
            numero_carton_y + square_size/2,
            fill='#667eea', 
            outline='#764ba2', 
            width=2
        )
        
        # Número del cartón - CENTRADO PERFECTO
        self.canvas_preview.create_text(
            numero_carton_x, 
            numero_carton_y,
            text="1", 
            font=('Arial', 16, 'bold'),
            fill='white',
            anchor="center"  # Centrado perfecto
        )
        
        # Indicador de fondo personalizado
        if self.background_path:
            self.canvas_preview.create_text(canvas_width/2, canvas_height - 15,
                                          text="🎨 Fondo personalizado activo", 
                                          font=('Arial', 10, 'bold'),
                                          fill=self.colors['accent_primary'])
    
    def actualizar_preview(self):
        """Actualizar la vista previa"""
        self.dibujar_preview_carton()
    
    def iniciar_generacion(self):
        """Iniciar proceso de generación de cartones"""
        try:
            cantidad = int(self.entry_cantidad.get().strip())
            if cantidad <= 0 or cantidad > self.bingo_actual.cantidad_cartones:
                messagebox.showerror("Error", 
                                   f"La cantidad debe estar entre 1 y {self.bingo_actual.cantidad_cartones}")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida")
            return
        
        # Mostrar frame de progreso
        self.mostrar_progreso()
        
        # Iniciar generación en hilo separado
        thread = threading.Thread(target=self.generar_cartones_thread, 
                                args=(cantidad,), daemon=True)
        thread.start()
    
    def mostrar_progreso(self):
        """Mostrar interfaz de progreso"""
        # Ocultar controles principales
        for widget in self.modal.winfo_children():
            widget.pack_forget()
        
        # Frame principal para progreso
        frame_progreso_principal = tk.Frame(self.modal, bg=self.colors['bg_primary'], padx=30, pady=30)
        frame_progreso_principal.pack(fill="both", expand=True)
        
        # Contenido del progreso
        tk.Label(frame_progreso_principal, 
                text="🔄 GENERANDO CARTONES...",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['accent_primary']).pack(pady=20)
        
        # Spinner
        self.lbl_estado = tk.Label(frame_progreso_principal,
                                  text="Preparando...",
                                  font=("Segoe UI", 12),
                                  bg=self.colors['bg_primary'],
                                  fg=self.colors['text_secondary'])
        self.lbl_estado.pack(pady=10)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(frame_progreso_principal, 
                                      mode='indeterminate',
                                      length=400)
        self.progress.pack(pady=20)
        self.progress.start()
    
    def generar_cartones_thread(self, cantidad):
        """Generar cartones en un hilo separado"""
        try:
            downloads_path = Path.home() / "Downloads"
            carpeta_cartones = downloads_path / f"cartones_{self.bingo_actual.nombre.replace(' ', '_')}"
            carpeta_cartones.mkdir(exist_ok=True)
            
            cartones_generados = 0
            
            # Decidir qué método usar
            if PIL_AVAILABLE:
                # Usar PNG si PIL está disponible
                self.actualizar_estado_progreso("Generando cartones PNG...")
                cartones_generados = self.generar_cartones_png(cantidad, carpeta_cartones)
                formato = "PNG"
            else:
                # Usar HTML como fallback
                self.actualizar_estado_progreso("Generando cartones HTML...")
                cartones_generados = self.generar_cartones_html(cantidad, carpeta_cartones)
                formato = "HTML"
            
            # Completado
            self.progress.stop()
            self.actualizar_estado_progreso("✅ ¡Generación completada!")
            
            # Mostrar mensaje de éxito
            self.parent.after(0, lambda: self.mostrar_resultado(cartones_generados, carpeta_cartones, formato))
            
        except Exception as e:
            self.parent.after(0, lambda: messagebox.showerror("Error", f"Error generando cartones: {e}"))
    
    def generar_cartones_png(self, cantidad, carpeta_cartones):
        """Generar cartones en formato PNG - DISEÑO MEJORADO"""
        cartones_generados = 0
        
        for numero in range(1, cantidad + 1):
            if numero > self.bingo_actual.cantidad_cartones:
                break
            
            # Obtener datos del cartón
            carton_data = self.bingo_actual.obtener_carton(numero)
            
            # Generar imagen del cartón
            imagen_carton = self.generar_imagen_carton(numero, carton_data)
            
            # Guardar imagen
            nombre_archivo = f"carton_{numero:03d}.png"
            ruta_archivo = carpeta_cartones / nombre_archivo
            imagen_carton.save(ruta_archivo, "PNG")
            
            cartones_generados += 1
            
            # Actualizar progreso
            self.actualizar_estado_progreso(f"Generando cartón {numero}/{cantidad}...")
            time.sleep(0.1)
            
        return cartones_generados
    
    def generar_cartones_html(self, cantidad, carpeta_cartones):
        """Generar cartones en formato HTML"""
        # Generar archivo HTML principal
        html_content = self.generar_html_principal(cantidad)
        archivo_html = carpeta_cartones / "cartones.html"
        
        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Abrir en navegador
        webbrowser.open(f'file://{archivo_html}')
        
        return cantidad
    
    def actualizar_estado_progreso(self, mensaje):
        """Actualizar mensaje de progreso desde el hilo principal"""
        def actualizar():
            self.lbl_estado.config(text=mensaje)
        self.parent.after(0, actualizar)
    
    def mostrar_resultado(self, cartones_generados, carpeta_destino, formato):
        """Mostrar resultado de la generación"""
        self.modal.destroy()
        
        if formato == "PNG":
            mensaje = (f"✅ ¡Generación completada!\n\n"
                      f"Se han generado {cartones_generados} cartones personalizados\n\n"
                      f"📁 Guardados en: {carpeta_destino}\n\n"
                      f"🎨 Características:\n"
                      f"   • Formato: PNG de alta calidad\n"
                      f"   • Diseño: Moderno y elegante\n"
                      f"   • Fondo personalizado: {'✅' if self.background_path else '❌'}\n"
                      f"   • Logo en FREE: {'✅' if self.logo_path else '❌'}")
        else:
            mensaje = (f"✅ ¡Generación completada!\n\n"
                      f"Se han generado {cartones_generados} cartones en formato HTML\n\n"
                      f"📁 Guardados en: {carpeta_destino}\n\n"
                      f"📄 Archivo: cartones.html\n\n"
                      f"El archivo se ha abierto en tu navegador.\n"
                      f"Puedes imprimirlo o guardarlo como PDF.")
        
        messagebox.showinfo("Generación Completada", mensaje)
    
    def generar_imagen_carton(self, numero, carton_data):
        """Generar imagen PNG del cartón - DISEÑO MEJORADO"""
        if not PIL_AVAILABLE:
            return type('DummyImage', (), {'save': lambda self, *args, **kwargs: None})()
        
        # Tamaño del cartón VERTICAL (formato retrato)
        width, height = 600, 800  # Vertical
        
        # Crear imagen base
        if self.background_path and os.path.exists(self.background_path):
            try:
                # Cargar fondo y adaptarlo al tamaño vertical
                fondo_original = Image.open(self.background_path).convert('RGBA')
                # Redimensionar manteniendo relación de aspecto
                fondo_original = ImageOps.fit(fondo_original, (width, height), method=Image.Resampling.LANCZOS)
                imagen = fondo_original.copy()
            except Exception as e:
                print(f"Error cargando fondo: {e}")
                imagen = Image.new('RGB', (width, height), color='#f8f9fa')
        else:
            # Fondo blanco limpio por defecto
            imagen = Image.new('RGB', (width, height), color='#f8f9fa')
        
        draw = ImageDraw.Draw(imagen)
        
        try:
            # Cargar fuentes modernas
            try:
                letra_font = ImageFont.truetype("arialbd.ttf", 32)
                numero_font = ImageFont.truetype("arialbd.ttf", 24)
                free_font = ImageFont.truetype("arialbd.ttf", 20)
                badge_font = ImageFont.truetype("arialbd.ttf", 18)
            except:
                # Fuentes por defecto
                letra_font = ImageFont.load_default()
                numero_font = ImageFont.load_default()
                free_font = ImageFont.load_default()
                badge_font = ImageFont.load_default()
            
            # Dimensiones de la tabla (formato vertical centrado)
            tabla_width = width - 80
            tabla_height = height - 120
            tabla_x = (width - tabla_width) // 2
            tabla_y = (height - tabla_height) // 2
            
            # Colores modernos para las letras BINGO
            colores_letras = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFD93D']
            letras = ['B', 'I', 'N', 'G', 'O']
            
            ancho_celda = tabla_width / 5
            alto_celda = tabla_height / 6
            
            # Dibujar header BINGO con diseño moderno
            for i, (letra, color) in enumerate(zip(letras, colores_letras)):
                x1 = tabla_x + i * ancho_celda
                y1 = tabla_y
                x2 = x1 + ancho_celda
                y2 = tabla_y + alto_celda
                
                # Fondo de la letra con diseño moderno
                draw.rectangle([x1, y1, x2, y2], fill=color, outline='#ffffff', width=3)
                
                # Texto de la letra centrado
                try:
                    letra_bbox = draw.textbbox((0, 0), letra, font=letra_font)
                    letra_width = letra_bbox[2] - letra_bbox[0]
                    letra_height = letra_bbox[3] - letra_bbox[1]
                    draw.text((x1 + (ancho_celda - letra_width) // 2, 
                              y1 + (alto_celda - letra_height) // 2),
                             letra, 
                             fill='white', 
                             font=letra_font)
                except:
                    draw.text((x1 + ancho_celda // 2, y1 + alto_celda // 2), 
                             letra, fill='white', anchor="mm")
            
            # Dibujar números del cartón
            for fila in range(5):
                for col, letra in enumerate(letras):
                    clave = f'{letra}{fila+1}'
                    valor = carton_data.get(clave, '')
                    
                    x1 = tabla_x + col * ancho_celda
                    y1 = tabla_y + (fila + 1) * alto_celda
                    x2 = x1 + ancho_celda
                    y2 = y1 + alto_celda
                    
                    # Casilla FREE en el centro - FONDO BLANCO para el logo
                    if fila == 2 and col == 2:
                        # FONDO BLANCO para mejor visualización del logo
                        draw.rectangle([x1, y1, x2, y2], fill='#ffffff', outline='#e0e0e0', width=2)
                        
                        # Agregar logo si está disponible - MÁS GRANDE
                        if self.logo_path and os.path.exists(self.logo_path):
                            try:
                                logo = Image.open(self.logo_path).convert('RGBA')
                                # Redimensionar logo MÁS GRANDE para que ocupe más espacio
                                logo_size = min(int(ancho_celda * 0.8), int(alto_celda * 0.8))  # 80% en lugar de 60%
                                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                                # Pegar logo en el centro de FREE
                                logo_x = x1 + (ancho_celda - logo_size) // 2
                                logo_y = y1 + (alto_celda - logo_size) // 2
                                imagen.paste(logo, (int(logo_x), int(logo_y)), logo)
                            except Exception as e:
                                print(f"Error agregando logo: {e}")
                                # Si falla el logo, poner texto FREE elegante
                                draw.text((x1 + ancho_celda // 2, y1 + alto_celda // 2), 
                                         "FREE", fill='#888888', anchor="mm", font=free_font)
                        else:
                            # Sin logo, poner texto FREE elegante en gris
                            draw.text((x1 + ancho_celda // 2, y1 + alto_celda // 2), 
                                     "FREE", fill='#888888', anchor="mm", font=free_font)
                    else:
                        # Celdas normales con diseño limpio
                        draw.rectangle([x1, y1, x2, y2], fill='#ffffff', outline='#e0e0e0', width=1)
                        if valor:
                            try:
                                num_bbox = draw.textbbox((0, 0), str(valor), font=numero_font)
                                num_width = num_bbox[2] - num_bbox[0]
                                num_height = num_bbox[3] - num_bbox[1]
                                draw.text((x1 + (ancho_celda - num_width) // 2, 
                                          y1 + (alto_celda - num_height) // 2),
                                         str(valor), 
                                         fill='#2d2d4d', 
                                         font=numero_font)
                            except:
                                draw.text((x1 + ancho_celda // 2, y1 + alto_celda // 2), 
                                         str(valor), fill='#2d2d4d', anchor="mm")
            
            # NUEVO DISEÑO: Número del cartón en esquina superior derecha - CUADRADO PERFECTO
            square_size = 40  # Tamaño del cuadrado
            badge_x = width - 45  # Más hacia la esquina
            badge_y = 45  # Más hacia la esquina
            
            # Cuadrado perfecto
            draw.rectangle([
                badge_x - square_size/2, 
                badge_y - square_size/2,
                badge_x + square_size/2, 
                badge_y + square_size/2
            ], fill='#667eea', outline='#764ba2', width=2)
            
            # Texto del badge - CENTRADO PERFECTO
            badge_text = f"{numero}"
            try:
                # Método más preciso para centrado
                draw.text((badge_x, badge_y), badge_text, fill='white', font=badge_font, anchor="mm")
            except:
                # Método de respaldo
                badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
                badge_text_width = badge_bbox[2] - badge_bbox[0]
                badge_text_height = badge_bbox[3] - badge_bbox[1]
                draw.text((
                    badge_x - badge_text_width/2, 
                    badge_y - badge_text_height/2
                ), badge_text, fill='white', font=badge_font)
            
        except Exception as e:
            print(f"Error dibujando cartón: {e}")
        
        return imagen

    def generar_html_principal(self, cantidad):
        """Generar archivo HTML principal con todos los cartones - DISEÑO MEJORADO"""
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Cartones de Bingo - {self.bingo_actual.nombre}</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .page {{
                    background: white;
                    padding: 40px;
                    margin-bottom: 30px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                    page-break-after: always;
                }}
                .carton-container {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 40px;
                    margin: 30px 0;
                }}
                .carton {{
                    border: 3px solid #e0e0e0;
                    border-radius: 15px;
                    margin: 0 auto;
                    width: 340px;
                    background: white;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
                    position: relative;
                    overflow: hidden;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }}
                .carton:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
                }}
                .carton-badge {{
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    width: 40px;
                    height: 40px;
                    border-radius: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 16px;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    z-index: 10;
                    border: 2px solid #764ba2;
                }}
                .carton-header {{
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                    border-bottom: 2px solid #f0f0f0;
                }}
                .carton-cell {{
                    padding: 20px;
                    text-align: center;
                    border: 1px solid #f0f0f0;
                    font-size: 18px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    background: #ffffff;
                }}
                .carton-cell:hover {{
                    background-color: #f8f9fa;
                    transform: scale(1.05);
                }}
                .carton-header-cell {{
                    padding: 20px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                    border: none;
                }}
                .b {{ background: #FF6B6B; }}
                .i {{ background: #4ECDC4; }}
                .n {{ background: #45B7D1; }}
                .g {{ background: #96CEB4; }}
                .o {{ background: #FFD93D; color: #2d2d4d; }}
                .free {{
                    background: #ffffff !important;
                    font-weight: bold;
                    color: #888888;
                    font-size: 16px;
                    border: 2px dashed #e0e0e0;
                }}
                .numero {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #2d2d4d;
                    background: #f8f9fa;
                }}
                @media print {{
                    body {{
                        background: white;
                        margin: 0;
                        padding: 20px;
                    }}
                    .page {{
                        box-shadow: none;
                        border-radius: 0;
                        margin: 0;
                    }}
                    .carton-container {{
                        grid-template-columns: repeat(2, 1fr);
                    }}
                    .carton:hover {{
                        transform: none;
                        box-shadow: none;
                    }}
                    .carton-cell:hover {{
                        background-color: transparent;
                        transform: none;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
        """
        
        cartones_por_pagina = 4
        for pagina in range(0, cantidad, cartones_por_pagina):
            html += f'<div class="page">'
            html += '<div class="carton-container">'
            
            for i in range(pagina, min(pagina + cartones_por_pagina, cantidad)):
                numero_carton = i + 1
                if numero_carton > self.bingo_actual.cantidad_cartones:
                    break
                    
                carton_data = self.bingo_actual.obtener_carton(numero_carton)
                html += self.generar_carton_html(numero_carton, carton_data)
            
            html += '</div></div>'
        
        html += """
            </div>
        </body>
        </html>
        """
        return html

    def generar_carton_html(self, numero, carton_data):
        """Generar HTML para un cartón individual - DISEÑO MEJORADO"""
        letras = ['B', 'I', 'N', 'G', 'O']
        colores_clases = ['b', 'i', 'n', 'g', 'o']
        
        html = f'<div class="carton">'
        html += f'<div class="carton-badge">{numero}</div>'
        
        # Header BINGO con colores modernos
        html += '<div class="carton-header">'
        for i, (letra, color_class) in enumerate(zip(letras, colores_clases)):
            html += f'<div class="carton-header-cell {color_class}">{letra}</div>'
        html += '</div>'
        
        # Números
        for fila in range(5):
            html += '<div style="display: grid; grid-template-columns: repeat(5, 1fr);">'
            for col, letra in enumerate(letras):
                clave = f'{letra}{fila+1}'
                valor = carton_data.get(clave, '')
                
                if fila == 2 and col == 2:  # Casilla FREE
                    html += '<div class="carton-cell free">FREE</div>'
                else:
                    html += f'<div class="carton-cell numero">{valor}</div>'
            html += '</div>'
        
        html += '</div>'
        return html