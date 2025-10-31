import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path

class VistaAsignaciones:
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
            'accent_danger': '#ff4757',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'border': '#00ff88'
        }
        
        self.frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crear interfaz moderna de la vista de asignaciones"""
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

        # Información del bingo actual
        self.lbl_info_bingo = tk.Label(header_frame,
            text="👥 ASIGNACIONES - Bingo: [Nombre]",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_primary']
        )
        self.lbl_info_bingo.pack(side='left', padx=20, pady=10)

        # Barra de herramientas moderna
        toolbar_frame = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        toolbar_frame.pack(fill='x', padx=20, pady=15)

        btn_exportar_vendidos = tk.Button(toolbar_frame,
            text="📄 EXPORTAR VENDIDOS (TXT)",
            command=self.exportar_tablas_vendidas,
            font=('Segoe UI', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_exportar_vendidos.pack(side='left', padx=8)

        btn_exportar_disponibles = tk.Button(toolbar_frame,
            text="📄 EXPORTAR DISPONIBLES (TXT)",
            command=self.exportar_tablas_disponibles,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent_secondary'],
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_exportar_disponibles.pack(side='left', padx=8)

        # Estadísticas rápidas
        stats_frame = tk.Frame(toolbar_frame, bg=self.colors['bg_primary'])
        stats_frame.pack(side='right', padx=10)

        self.lbl_stats = tk.Label(stats_frame,
            text="🎯 0 personas | 🎫 0 cartones vendidos",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        self.lbl_stats.pack()

        # Frame principal de asignaciones - CENTRADO
        self.frame_asignaciones = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        self.frame_asignaciones.pack(fill='both', expand=True, padx=20, pady=10)

    def mostrar_asignaciones(self, bingo):
        """Mostrar las asignaciones del bingo actual con diseño moderno"""
        self.bingo_actual = bingo
        self.actualizar_info_bingo()

        # Limpiar frame de asignaciones
        for widget in self.frame_asignaciones.winfo_children():
            widget.destroy()

        # Obtener asignaciones agrupadas por persona
        asignaciones_por_persona = self.obtener_asignaciones_por_persona()

        if not asignaciones_por_persona:
            # Mostrar mensaje moderno CENTRADO si no hay asignaciones
            frame_vacio = tk.Frame(self.frame_asignaciones, 
                                 bg=self.colors['bg_primary'], 
                                 padx=30, 
                                 pady=50)
            frame_vacio.pack(fill='both', expand=True)
            
            lbl_vacio = tk.Label(frame_vacio,
                text="👥 No hay asignaciones registradas\n\nLos cartones asignados aparecerán aquí",
                font=('Segoe UI', 14),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary'],
                justify='center')
            lbl_vacio.place(relx=0.5, rely=0.5, anchor='center')
            return

        # Frame con scroll para la lista
        frame_contenedor = tk.Frame(self.frame_asignaciones, bg=self.colors['bg_primary'])
        frame_contenedor.pack(fill='both', expand=True)

        # Crear canvas y scrollbar
        canvas = tk.Canvas(frame_contenedor, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        
        # Frame principal para la cuadrícula - CENTRADO
        self.frame_lista = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        # Configurar el canvas para centrar el contenido
        self.frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Crear ventana en el canvas CENTRADA
        canvas_frame = canvas.create_window((0, 0), window=self.frame_lista, anchor="nw", tags="frame")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Función para centrar el frame_lista cuando cambie el tamaño
        def centrar_contenido(event=None):
            canvas.update_idletasks()
            # Obtener el ancho del canvas
            canvas_width = canvas.winfo_width()
            # Obtener el ancho requerido por el frame_lista
            lista_width = self.frame_lista.winfo_reqwidth()
            
            # Si el frame_lista es más pequeño que el canvas, centrarlo
            if lista_width < canvas_width:
                new_x = (canvas_width - lista_width) // 2
                canvas.coords("frame", new_x, 0)
            else:
                canvas.coords("frame", 0, 0)
        
        # Vincular el evento de redimensionamiento
        canvas.bind("<Configure>", centrar_contenido)
        self.frame_lista.bind("<Configure>", centrar_contenido)

        # Configurar scroll con mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        self.frame_lista.bind("<MouseWheel>", on_mousewheel)

        # Empacar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crear tarjetas
        self.crear_tarjetas_personas(asignaciones_por_persona)

    def crear_tarjetas_personas(self, asignaciones_por_persona):
        """Crear tarjetas para todas las personas - 4 COLUMNAS PERO CENTRADAS Y MÁS GRANDES"""
        # Limpiar frame
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        personas = sorted(asignaciones_por_persona.items())
        if not personas:
            return

        # CONFIGURACIÓN FIJA DE 4 COLUMNAS (como antes)
        COLUMNAS = 4
        PADDING_HORIZONTAL = 20
        MARGEN_ENTRE_TARJETAS = 15
        
        # Tamaño MÁS GRANDE de tarjetas
        ancho_tarjeta = 380  # Aumentado de 320 a 380 (más ancho)
        alto_tarjeta = 280   # Aumentado de 240 a 280 (más alto)

        # Calcular número de filas necesarias
        total_personas = len(personas)
        filas = (total_personas + COLUMNAS - 1) // COLUMNAS

        # Configurar grid para CENTRADO - todas las columnas con mismo peso
        for i in range(filas):
            self.frame_lista.grid_rowconfigure(i, weight=0)
        
        # Configurar 4 columnas con el mismo peso para centrado
        for i in range(COLUMNAS):
            self.frame_lista.grid_columnconfigure(i, weight=1)

        # Crear tarjetas en grid - 4 COLUMNAS CENTRADAS Y MÁS GRANDES
        for idx, (nombre, cartones) in enumerate(personas):
            fila = idx // COLUMNAS
            columna = idx % COLUMNAS

            # Crear tarjeta con tamaño MÁS GRANDE
            self.crear_tarjeta_persona(nombre, cartones, fila, columna, ancho_tarjeta, alto_tarjeta)

        # Forzar actualización del layout
        self.frame_lista.update_idletasks()

    def crear_tarjeta_persona(self, nombre, cartones, fila, columna, ancho, alto):
        """Crear tarjeta moderna para una persona con tamaño MÁS GRANDE"""
        # Frame principal de la tarjeta
        frame_persona = tk.Frame(self.frame_lista, 
                               bg=self.colors['bg_card'],
                               relief='flat',
                               bd=1,
                               width=ancho,
                               height=alto)
        frame_persona.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")  # Padding aumentado
        frame_persona.grid_propagate(False)
        
        # Contenedor principal dentro de la tarjeta - MÁS ESPACIO INTERNO
        frame_contenido = tk.Frame(frame_persona, bg=self.colors['bg_card'], padx=18, pady=15)
        frame_contenido.pack(fill='both', expand=True)

        # Header de la persona
        frame_header = tk.Frame(frame_contenido, bg=self.colors['bg_card'])
        frame_header.pack(fill='x', pady=(0, 12))  # Más espacio

        # Icono y nombre
        lbl_icono = tk.Label(frame_header, text="👤", font=('Segoe UI', 14),  # Icono más grande
                           bg=self.colors['bg_card'], fg=self.colors['accent_primary'])
        lbl_icono.pack(side='left', padx=(0, 12))

        # Nombre con ajuste automático - FUENTE MÁS GRANDE
        lbl_nombre = tk.Label(frame_header,
            text=nombre,
            font=('Segoe UI', 13, 'bold'),  # Fuente más grande
            bg=self.colors['bg_card'],
            fg=self.colors['accent_primary'],
            wraplength=ancho - 150,  # Ajustado para el nuevo ancho
            justify='left'
        )
        lbl_nombre.pack(side='left', fill='x', expand=True)

        # Badge de cantidad - MÁS GRANDE
        badge_frame = tk.Frame(frame_header, bg=self.colors['accent_secondary'], 
                             relief='flat', bd=1)
        badge_frame.pack(side='right')

        lbl_badge = tk.Label(badge_frame,
            text=f"{len(cartones)}",
            font=('Segoe UI', 11, 'bold'),  # Fuente más grande
            bg=self.colors['accent_secondary'],
            fg='white',
            padx=8,  # Más padding
            pady=4   # Más padding
        )
        lbl_badge.pack()

        # Información de pago
        frame_pago = tk.Frame(frame_contenido, bg=self.colors['bg_card'])
        frame_pago.pack(fill='x', pady=(0, 15))  # Más espacio

        total_pagado = len(cartones) * self.bingo_actual.precio_carton
        lbl_pago = tk.Label(frame_pago,
            text=f"💰 Total pagado: ${total_pagado:,.2f}",
            font=('Segoe UI', 11, 'bold'),  # Fuente más grande
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        lbl_pago.pack(anchor='w')

        # Frame para los cartones
        frame_cartones = tk.Frame(frame_contenido, bg=self.colors['bg_card'])
        frame_cartones.pack(fill='both', expand=True)

        lbl_cartones_titulo = tk.Label(frame_cartones,
            text="🎫 Cartones asignados:",
            font=('Segoe UI', 11, 'bold'),  # Fuente más grande
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        lbl_cartones_titulo.pack(anchor='w', pady=(0, 10))  # Más espacio

        # CARTONES EN FILAS DE MÁXIMO 4 (FIJO) Y CENTRADOS
        CARTONES_POR_FILA = 4  # SIEMPRE 4 CARTONES POR FILA

        # Mostrar cartones en grid
        cartones_ordenados = sorted(cartones)
        total_cartones = len(cartones_ordenados)
        filas_cartones = (total_cartones + CARTONES_POR_FILA - 1) // CARTONES_POR_FILA

        # Frame para el grid de cartones - CENTRADO
        frame_grid_cartones = tk.Frame(frame_cartones, bg=self.colors['bg_card'])
        frame_grid_cartones.pack(anchor='center', pady=5)  # CENTRADO

        # Configurar grid para cartones - 4 columnas fijas
        for i in range(filas_cartones):
            frame_grid_cartones.grid_rowconfigure(i, weight=1)
        for i in range(CARTONES_POR_FILA):
            frame_grid_cartones.grid_columnconfigure(i, weight=1)

        # Crear botones de cartones en grid - BOTONES MÁS GRANDES Y UNIFORMES
        for idx, carton in enumerate(cartones_ordenados):
            fila_carton = idx // CARTONES_POR_FILA
            columna_carton = idx % CARTONES_POR_FILA

            btn_carton = tk.Button(frame_grid_cartones,
                text=f"#{carton}",
                command=lambda c=carton: self.ver_detalle_carton(c),
                font=('Segoe UI', 10, 'bold'),  # Fuente más grande
                bg=self.colors['accent_secondary'],
                fg='white',
                relief='flat',
                cursor='hand2',
                bd=0,
                width=6,  # Botones más anchos (aumentado de 5 a 6)
                height=1  # Botones más altos
            )
            btn_carton.grid(row=fila_carton, column=columna_carton, padx=4, pady=3, sticky="nsew")  # Más padding

        # Si hay menos de 4 cartones en la última fila, crear frames vacíos para mantener el layout CENTRADO
        ultima_fila_cartones = total_cartones % CARTONES_POR_FILA
        if ultima_fila_cartones > 0 and ultima_fila_cartones < CARTONES_POR_FILA:
            for col in range(ultima_fila_cartones, CARTONES_POR_FILA):
                frame_vacio = tk.Frame(frame_grid_cartones, bg=self.colors['bg_card'])
                frame_vacio.grid(row=filas_cartones-1, column=col, sticky="nsew")

    def obtener_asignaciones_por_persona(self):
        """Obtener asignaciones agrupadas por persona"""
        asignaciones = {}

        if not self.bingo_actual:
            return asignaciones

        for numero in range(1, self.bingo_actual.cantidad_cartones + 1):
            estado = self.bingo_actual.obtener_estado_carton(numero)
            if estado.get('vendido', False):
                nombre = estado.get('nombre', 'Sin nombre')
                if nombre not in asignaciones:
                    asignaciones[nombre] = []
                asignaciones[nombre].append(numero)

        return asignaciones

    def ver_detalle_carton(self, numero):
        """Ver detalle de un cartón específico con modal moderno"""
        if not self.bingo_actual:
            return

        estado = self.bingo_actual.obtener_estado_carton(numero)
        if estado.get('vendido', False):
            # Crear modal moderno
            modal = tk.Toplevel(self.parent)
            modal.title(f"🎫 Detalle Cartón #{numero}")
            modal.geometry("450x300")
            modal.configure(bg=self.colors['bg_primary'])
            modal.transient(self.parent)
            modal.grab_set()

            # Centrar el modal
            modal.update_idletasks()
            x = (modal.winfo_screenwidth() // 2) - (450 // 2)
            y = (modal.winfo_screenheight() // 2) - (300 // 2)
            modal.geometry(f"450x300+{x}+{y}")

            frame_modal = tk.Frame(modal, bg=self.colors['bg_primary'], padx=25, pady=25)
            frame_modal.pack(fill="both", expand=True)

            # Icono
            lbl_icono = tk.Label(frame_modal, text="🎫", font=("Arial", 28), 
                               bg=self.colors['bg_primary'], fg=self.colors['accent_primary'])
            lbl_icono.pack(pady=10)

            # Información del cartón
            lbl_titulo = tk.Label(frame_modal, text=f"CARTÓN #{numero}",
                                font=("Segoe UI", 18, "bold"), 
                                bg=self.colors['bg_primary'], fg=self.colors['accent_primary'])
            lbl_titulo.pack(pady=5)

            lbl_estado = tk.Label(frame_modal, text="✅ VENDIDO",
                                font=("Segoe UI", 12, "bold"), 
                                bg=self.colors['bg_primary'], fg='#27ae60')
            lbl_estado.pack(pady=5)

            # Detalles
            frame_detalles = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
            frame_detalles.pack(pady=20)

            detalles = [
                f"👤 {estado.get('nombre', '')}",
                f"💰 ${self.bingo_actual.precio_carton:,.2f}",
                f"📅 {estado.get('fecha_asignacion', 'No disponible')}"
            ]

            for detalle in detalles:
                lbl_detalle = tk.Label(frame_detalles,
                    text=detalle,
                    font=("Segoe UI", 12),
                    bg=self.colors['bg_primary'],
                    fg=self.colors['text_primary'],
                    pady=5
                )
                lbl_detalle.pack()

            # Botón cerrar
            btn_cerrar = tk.Button(frame_modal, text="👌 CERRAR",
                                 command=modal.destroy,
                                 bg=self.colors['accent_secondary'], 
                                 fg="white", 
                                 font=("Segoe UI", 12, "bold"),
                                 padx=30,
                                 pady=12,
                                 relief='flat', 
                                 cursor="hand2",
                                 bd=0)
            btn_cerrar.pack(pady=20)

    def exportar_tablas_vendidas(self):
        """Exportar tablas vendidas a archivo TXT con asignaciones centradas"""
        if not self.bingo_actual:
            messagebox.showerror("Error", "No hay bingo activo")
            return

        try:
            from utils.helpers import obtener_carpeta_descargas
            downloads_path = obtener_carpeta_descargas()

            nombre_archivo = f"tablas_vendidas_{self.bingo_actual.nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta_archivo = downloads_path / nombre_archivo

            asignaciones = self.obtener_asignaciones_por_persona()

            contenido = []
            contenido.append("# EXPORTAR VENDIDOS (TXT)")
            contenido.append("")

            if asignaciones:
                for idx, (nombre, cartones) in enumerate(sorted(asignaciones.items()), 1):
                    contenido.append(f"## {idx}. {nombre}")
                    total_pagado = len(cartones) * self.bingo_actual.precio_carton
                    contenido.append(f"- **Total pagado:** ${total_pagado:.2f}")
                    contenido.append(f"- **Cartones asignados:**")
                    contenido.append("")
                    
                    # Centrar los números de cartones en formato de tabla
                    cartones_ordenados = sorted(cartones)
                    
                    # Calcular el ancho máximo para centrado
                    if cartones_ordenados:
                        # Si hay pocos cartones, mostrarlos en una sola fila
                        if len(cartones_ordenados) <= 6:
                            linea = "   " + "   ".join(f"{carton:4}" for carton in cartones_ordenados)
                            contenido.append(linea)
                        else:
                            # Para muchos cartones, dividir en filas de 4 cartones
                            CARTONES_POR_FILA = 4
                            for i in range(0, len(cartones_ordenados), CARTONES_POR_FILA):
                                grupo = cartones_ordenados[i:i + CARTONES_POR_FILA]
                                linea = "   " + "   ".join(f"{carton:4}" for carton in grupo)
                                contenido.append(linea)
                    
                    contenido.append("")
                    contenido.append("---")
                    contenido.append("")

            else:
                contenido.append("No hay tablas vendidas")
                contenido.append("")

            # Agregar resumen final
            total_personas = len(asignaciones)
            total_cartones = sum(len(cartones) for cartones in asignaciones.values())
            contenido.append(f"### {total_personas} personas | EBI {total_cartones} cartones vendidos")
            contenido.append("")
            contenido.append("---")

            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contenido))

            messagebox.showinfo(
                "Exportación Exitosa",
                f"✅ Archivo de tablas vendidas generado:\n\n"
                f"📁 {nombre_archivo}\n\n"
                f"👥 Personas: {len(asignaciones)}\n"
                f"🎫 Cartones vendidos: {sum(len(cartones) for cartones in asignaciones.values())}\n"
                f"💾 Guardado en: {ruta_archivo}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error exportando tablas vendidas: {e}")

    def exportar_tablas_disponibles(self):
        """Exportar tablas disponibles a archivo TXT"""
        if not self.bingo_actual:
            messagebox.showerror("Error", "No hay bingo activo")
            return

        try:
            from utils.helpers import obtener_carpeta_descargas
            downloads_path = obtener_carpeta_descargas()

            nombre_archivo = f"tablas_disponibles_{self.bingo_actual.nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta_archivo = downloads_path / nombre_archivo

            # Obtener cartones disponibles
            cartones_vendidos = self.bingo_actual.obtener_cartones_vendidos()
            cartones_disponibles = [num for num in range(1, self.bingo_actual.cantidad_cartones + 1)
                                  if num not in cartones_vendidos]

            contenido = []
            contenido.append("=" * 60)
            contenido.append(f"REPORTE DE TABLAS DISPONIBLES - {self.bingo_actual.nombre.upper()}")
            contenido.append("=" * 60)
            contenido.append(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            contenido.append(f"Total de cartones disponibles: {len(cartones_disponibles)}")
            contenido.append(f"Precio por cartón: ${self.bingo_actual.precio_carton:,.2f}")
            contenido.append(f"Ganancia potencial: ${len(cartones_disponibles) * self.bingo_actual.precio_carton:,.2f}")
            contenido.append("")
            contenido.append("CARTONES DISPONIBLES:")
            contenido.append("-" * 60)

            if cartones_disponibles:
                # Agrupar en filas de 10 números
                for i in range(0, len(cartones_disponibles), 10):
                    grupo = cartones_disponibles[i:i + 10]
                    linea = " " + ", ".join(f"{num:3}" for num in grupo)
                    contenido.append(linea)
            else:
                contenido.append("NO HAY CARTONES DISPONIBLES")
                contenido.append("TODOS LOS CARTONES ESTÁN VENDIDOS")

            contenido.append("")
            contenido.append("=" * 60)

            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contenido))

            messagebox.showinfo(
                "Exportación Exitosa",
                f"✅ Archivo de tablas disponibles generado:\n\n"
                f"📁 {nombre_archivo}\n\n"
                f"🎫 Cartones disponibles: {len(cartones_disponibles)}\n"
                f"💰 Ganancia potencial: ${len(cartones_disponibles) * self.bingo_actual.precio_carton:,.2f}\n"
                f"💾 Guardado en: {ruta_archivo}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error exportando tablas disponibles: {e}")

    def actualizar_info_bingo(self):
        """Actualizar la información del bingo y estadísticas"""
        if self.bingo_actual:
            texto = f"👥 ASIGNACIONES - Bingo: {self.bingo_actual.nombre}"
            self.lbl_info_bingo.config(text=texto)
            
            # Actualizar estadísticas
            asignaciones = self.obtener_asignaciones_por_persona()
            total_personas = len(asignaciones)
            total_cartones = sum(len(cartones) for cartones in asignaciones.values())
            self.lbl_stats.config(text=f"🎯 {total_personas} personas | 🎫 {total_cartones} cartones vendidos")

    def volver_gestor(self):
        """Volver al gestor de bingos"""
        self.controlador.mostrar_vista("gestor_bingos")

    def mostrar(self, datos=None):
        """Mostrar esta vista"""
        self.frame.pack(fill="both", expand=True)
        if datos and "bingo" in datos:
            self.mostrar_asignaciones(datos["bingo"])

    def ocultar(self):
        """Ocultar esta vista"""
        self.frame.pack_forget()