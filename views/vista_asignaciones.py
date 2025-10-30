import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path

class VistaAsignaciones:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.bingo_actual = None
        
        self.frame = tk.Frame(parent, bg='#1e1e1e')
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz de la pestaña de asignaciones con diseño mejorado"""
        # Frame de navegación superior
        frame_nav = tk.Frame(self.frame, bg='#2d2d2d', height=80)
        frame_nav.pack(fill='x', padx=20, pady=10)
        frame_nav.pack_propagate(False)
        
        # Botón volver al gestor
        btn_volver = tk.Button(frame_nav,
                             text="← VOLVER A BINGOS",
                             command=self.volver_gestor,
                             font=('Segoe UI', 10, 'bold'),
                             bg='#666666',
                             fg='white',
                             padx=20,
                             pady=12,
                             relief='flat',
                             cursor='hand2')
        btn_volver.pack(side='left', padx=10, pady=10)
        
        # Información del bingo actual
        self.lbl_info_bingo = tk.Label(frame_nav,
                                     text="Asignaciones - Bingo: [Nombre]",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#2d2d2d',
                                     fg='#4CAF50')
        self.lbl_info_bingo.pack(side='left', padx=20, pady=10)
        
        # Frame de controles con más padding
        frame_controles = tk.Frame(self.frame, bg='#1e1e1e')
        frame_controles.pack(fill='x', padx=20, pady=15)
        
        # Botones de exportación con más padding
        btn_exportar_vendidos = tk.Button(frame_controles,
                                        text="📄 EXPORTAR TABLAS VENDIDAS (TXT)",
                                        command=self.exportar_tablas_vendidas,
                                        font=('Segoe UI', 10, 'bold'),
                                        bg='#e74c3c',
                                        fg='white',
                                        padx=20,
                                        pady=12,
                                        relief='flat',
                                        cursor='hand2')
        btn_exportar_vendidos.pack(side='left', padx=8)
        
        btn_exportar_disponibles = tk.Button(frame_controles,
                                           text="📄 EXPORTAR TABLAS DISPONIBLES (TXT)",
                                           command=self.exportar_tablas_disponibles,
                                           font=('Segoe UI', 10, 'bold'),
                                           bg='#3498db',
                                           fg='white',
                                           padx=20,
                                           pady=12,
                                           relief='flat',
                                           cursor='hand2')
        btn_exportar_disponibles.pack(side='left', padx=8)
        
        # Frame principal de asignaciones
        self.frame_asignaciones = tk.Frame(self.frame, bg='#1e1e1e')
        self.frame_asignaciones.pack(fill='both', expand=True, padx=20, pady=10)
    def mostrar_asignaciones(self, bingo):
        """Mostrar las asignaciones del bingo actual"""
        self.bingo_actual = bingo
        self.actualizar_info_bingo()
        
        # Limpiar frame de asignaciones
        for widget in self.frame_asignaciones.winfo_children():
            widget.destroy()
        
        # Obtener asignaciones agrupadas por persona
        asignaciones_por_persona = self.obtener_asignaciones_por_persona()
        
        if not asignaciones_por_persona:
            # Mostrar mensaje si no hay asignaciones
            frame_vacio = tk.Frame(self.frame_asignaciones, bg='#2d2d2d', padx=30, pady=50)
            frame_vacio.pack(expand=True)
            
            lbl_vacio = tk.Label(frame_vacio,
                               text="👥 No hay asignaciones registradas\n\nLos cartones asignados aparecerán aquí",
                               font=('Segoe UI', 14),
                               bg='#2d2d2d',
                               fg='#cccccc',
                               justify='center')
            lbl_vacio.pack()
            return
        
        # Frame con scroll para la lista
        frame_contenedor = tk.Frame(self.frame_asignaciones, bg='#1e1e1e')
        frame_contenedor.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(frame_contenedor, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg='#1e1e1e')
        
        frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar scroll con mouse
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        frame_lista.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar cada persona con sus cartones asignados
        for nombre, cartones in sorted(asignaciones_por_persona.items()):
            self.crear_tarjeta_persona(frame_lista, nombre, cartones)
    
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
    
    def crear_tarjeta_persona(self, parent, nombre, cartones):
        """Crear tarjeta para una persona con sus cartones asignados"""
        frame_persona = tk.Frame(parent, bg='#2d2d2d', relief='raised', bd=1, padx=20, pady=15)
        frame_persona.pack(fill='x', pady=8, padx=10)
        
        # Header de la persona
        frame_header = tk.Frame(frame_persona, bg='#2d2d2d')
        frame_header.pack(fill='x')
        
        # Icono y nombre
        lbl_icono = tk.Label(frame_header, text="👤", font=('Segoe UI', 14), bg='#2d2d2d')
        lbl_icono.pack(side='left', padx=(0, 10))
        
        lbl_nombre = tk.Label(frame_header,
                            text=nombre,
                            font=('Segoe UI', 14, 'bold'),
                            bg='#2d2d2d',
                            fg='#4CAF50')
        lbl_nombre.pack(side='left')
        
        # Badge de cantidad
        badge_frame = tk.Frame(frame_header, bg='#e74c3c', relief='raised', bd=1)
        badge_frame.pack(side='right', padx=10)
        
        lbl_badge = tk.Label(badge_frame,
                           text=f"{len(cartones)} cartón{'es' if len(cartones) > 1 else ''}",
                           font=('Segoe UI', 10, 'bold'),
                           bg='#e74c3c',
                           fg='white',
                           padx=8,
                           pady=3)
        lbl_badge.pack()
        
        # Frame para los cartones
        frame_cartones = tk.Frame(frame_persona, bg='#2d2d2d')
        frame_cartones.pack(fill='x', pady=(10, 0))
        
        lbl_cartones_titulo = tk.Label(frame_cartones,
                                     text="Cartones asignados:",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='#2d2d2d',
                                     fg='#cccccc')
        lbl_cartones_titulo.pack(anchor='w', pady=(0, 5))
        
        # Mostrar cartones en grupos de 10
        cartones_ordenados = sorted(cartones)
        for i in range(0, len(cartones_ordenados), 10):
            grupo_cartones = cartones_ordenados[i:i + 10]
            
            grupo_frame = tk.Frame(frame_cartones, bg='#2d2d2d')
            grupo_frame.pack(fill='x', pady=2)
            
            for carton in grupo_cartones:
                btn_carton = tk.Button(grupo_frame,
                                     text=f"#{carton}",
                                     command=lambda c=carton: self.ver_detalle_carton(c),
                                     font=('Segoe UI', 8, 'bold'),
                                     bg='#3498db',
                                     fg='white',
                                     relief='flat',
                                     cursor='hand2',
                                     padx=8,
                                     pady=2)
                btn_carton.pack(side='left', padx=2, pady=2)
    
    def ver_detalle_carton(self, numero):
        """Ver detalle de un cartón específico"""
        if not self.bingo_actual:
            return
        
        estado = self.bingo_actual.obtener_estado_carton(numero)
        if estado.get('vendido', False):
            messagebox.showinfo(
                f"Detalle Cartón #{numero}",
                f"🎫 Cartón #{numero}\n\n"
                f"👤 Asignado a: {estado.get('nombre', '')}\n"
                f"📅 Fecha: {estado.get('fecha_asignacion', 'No disponible')}\n"
                f"💰 Precio: ${self.bingo_actual.precio_carton:,.2f}"
            )
    
    def exportar_tablas_vendidas(self):
        """Exportar tablas vendidas a archivo TXT"""
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
            contenido.append("=" * 60)
            contenido.append(f"REPORTE DE TABLAS VENDIDAS - {self.bingo_actual.nombre.upper()}")
            contenido.append("=" * 60)
            contenido.append(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            contenido.append(f"Total de cartones vendidos: {sum(len(cartones) for cartones in asignaciones.values())}")
            contenido.append(f"Precio por cartón: ${self.bingo_actual.precio_carton:,.2f}")
            contenido.append(f"Ganancias totales: ${self.bingo_actual.obtener_ganancias():,.2f}")
            contenido.append("")
            contenido.append("DETALLE POR PERSONA:")
            contenido.append("-" * 60)
            
            if asignaciones:
                for nombre, cartones in sorted(asignaciones.items()):
                    contenido.append(f"👤 {nombre}:")
                    contenido.append(f"   Cartones: {', '.join(map(str, sorted(cartones)))}")
                    contenido.append(f"   Cantidad: {len(cartones)} cartón{'es' if len(cartones) > 1 else ''}")
                    contenido.append(f"   Total pagado: ${len(cartones) * self.bingo_actual.precio_carton:,.2f}")
                    contenido.append("")
            else:
                contenido.append("No hay tablas vendidas")
                contenido.append("")
            
            contenido.append("=" * 60)
            
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
                    linea = "   " + ", ".join(f"{num:3}" for num in grupo)
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
        """Actualizar la información del bingo en la barra superior"""
        if self.bingo_actual:
            texto = f"Asignaciones - Bingo: {self.bingo_actual.nombre}"
            self.lbl_info_bingo.config(text=texto)
    
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