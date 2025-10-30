import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import json
from models.bingo import Bingo

class VistaGestorBingos:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.bingos = self.cargar_bingos_existentes()
        
        self.frame = tk.Frame(parent, bg='#1e1e1e')
        self.crear_interfaz()
    
    def cargar_bingos_existentes(self):
        """Cargar lista de bingos existentes desde archivos internos"""
        from utils.helpers import crear_directorio_bingos
        directorio_bingos = crear_directorio_bingos()
        bingos = []
        
        if directorio_bingos.exists():
            for archivo in directorio_bingos.glob("*.json"):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        datos = json.load(f)
                    
                    # Crear instancia de Bingo con los datos cargados
                    bingo = Bingo(
                        datos['nombre'],
                        datos['cantidad_cartones'],
                        datos.get('precio_carton', 0)
                    )
                    # Los datos se cargan automáticamente en el constructor de Bingo
                    bingos.append(bingo)
                except Exception as e:
                    print(f"Error cargando bingo {archivo}: {e}")
                    continue
        
        return bingos
    
    def crear_interfaz(self):
        """Crear interfaz del gestor de bingos"""
        # Frame de navegación
        frame_nav = tk.Frame(self.frame, bg='#2d2d2d', height=60)
        frame_nav.pack(fill='x', padx=20, pady=10)
        frame_nav.pack_propagate(False)
        
        # Botón volver
        btn_volver = tk.Button(frame_nav,
                             text="← VOLVER AL MENÚ",
                             command=self.volver_menu,
                             font=('Segoe UI', 10, 'bold'),
                             bg='#666666',
                             fg='white',
                             padx=15,
                             pady=8,
                             relief='flat',
                             cursor='hand2')
        btn_volver.pack(side='left', padx=10, pady=10)
        
        # Título dinámico
        self.titulo = tk.Label(frame_nav,
                             text="GESTOR DE BINGOS",
                             font=('Segoe UI', 16, 'bold'),
                             bg='#2d2d2d',
                             fg='white')
        self.titulo.pack(side='left', padx=20, pady=10)
        
        # Botón crear nuevo bingo
        btn_nuevo = tk.Button(frame_nav,
                            text="🆕 NUEVO BINGO",
                            command=self.mostrar_formulario_creacion,
                            font=('Segoe UI', 10, 'bold'),
                            bg='#4CAF50',
                            fg='white',
                            padx=15,
                            pady=8,
                            relief='flat',
                            cursor='hand2')
        btn_nuevo.pack(side='right', padx=10, pady=10)
        
        # Frame principal
        self.frame_principal = tk.Frame(self.frame, bg='#1e1e1e')
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Mostrar lista de bingos por defecto
        self.mostrar_lista_bingos()
    
    def mostrar_formulario_creacion(self):
        """Mostrar formulario para crear nuevo bingo"""
        # Limpiar frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        
        self.titulo.config(text="CREAR NUEVO BINGO")
        
        # Frame del formulario
        frame_form = tk.Frame(self.frame_principal, bg='#2d2d2d', padx=30, pady=30)
        frame_form.pack(expand=True)
        
        titulo_form = tk.Label(frame_form,
                             text="CREAR NUEVO BINGO",
                             font=('Segoe UI', 20, 'bold'),
                             bg='#2d2d2d',
                             fg='#4CAF50')
        titulo_form.pack(pady=(0, 30))
        
        # Campo nombre del bingo
        frame_nombre = tk.Frame(frame_form, bg='#2d2d2d')
        frame_nombre.pack(fill='x', pady=10)
        
        lbl_nombre = tk.Label(frame_nombre,
                            text="Nombre del Bingo:",
                            font=('Segoe UI', 11, 'bold'),
                            bg='#2d2d2d',
                            fg='#cccccc')
        lbl_nombre.pack(anchor='w')
        
        self.entry_nombre = tk.Entry(frame_nombre,
                                   font=('Segoe UI', 12),
                                   bg='#3d3d3d',
                                   fg='white',
                                   insertbackground='white',
                                   relief='flat',
                                   width=30)
        self.entry_nombre.pack(fill='x', pady=5, ipady=8)
        
        # Campo cantidad de cartones
        frame_cartones = tk.Frame(frame_form, bg='#2d2d2d')
        frame_cartones.pack(fill='x', pady=10)
        
        lbl_cartones = tk.Label(frame_cartones,
                              text="Cantidad de Cartones:",
                              font=('Segoe UI', 11, 'bold'),
                              bg='#2d2d2d',
                              fg='#cccccc')
        lbl_cartones.pack(anchor='w')
        
        self.entry_cartones = tk.Entry(frame_cartones,
                                     font=('Segoe UI', 12),
                                     bg='#3d3d3d',
                                     fg='white',
                                     insertbackground='white',
                                     relief='flat',
                                     width=30)
        self.entry_cartones.pack(fill='x', pady=5, ipady=8)
        self.entry_cartones.insert(0, "200")
        
        # Campo precio por cartón
        frame_precio = tk.Frame(frame_form, bg='#2d2d2d')
        frame_precio.pack(fill='x', pady=10)
        
        lbl_precio = tk.Label(frame_precio,
                            text="Precio por Cartón ($):",
                            font=('Segoe UI', 11, 'bold'),
                            bg='#2d2d2d',
                            fg='#cccccc')
        lbl_precio.pack(anchor='w')
        
        self.entry_precio = tk.Entry(frame_precio,
                                   font=('Segoe UI', 12),
                                   bg='#3d3d3d',
                                   fg='white',
                                   insertbackground='white',
                                   relief='flat',
                                   width=30)
        self.entry_precio.pack(fill='x', pady=5, ipady=8)
        self.entry_precio.insert(0, "100")
        
        # Frame de cálculo de ganancias
        frame_ganancias = tk.Frame(frame_form, bg='#3d3d3d', relief='raised', bd=1)
        frame_ganancias.pack(fill='x', pady=15)
        
        self.lbl_ganancias = tk.Label(frame_ganancias,
                                    text="Ganancias potenciales: $0.00",
                                    font=('Segoe UI', 11, 'bold'),
                                    bg='#3d3d3d',
                                    fg='#4CAF50')
        self.lbl_ganancias.pack(padx=15, pady=10)
        
        # Actualizar ganancias cuando cambien los campos
        self.entry_cartones.bind('<KeyRelease>', self.actualizar_ganancias)
        self.entry_precio.bind('<KeyRelease>', self.actualizar_ganancias)
        
        # Botones con más padding
        frame_botones = tk.Frame(frame_form, bg='#2d2d2d')
        frame_botones.pack(pady=30)
        
        btn_crear = tk.Button(frame_botones,
                            text="🎯 CREAR BINGO",
                            command=self.crear_bingo,
                            font=('Segoe UI', 12, 'bold'),
                            bg='#4CAF50',
                            fg='white',
                            padx=30,
                            pady=15,  # Más padding
                            relief='flat',
                            cursor='hand2')
        btn_crear.pack(side='left', padx=10)
        
        btn_cancelar = tk.Button(frame_botones,
                               text="❌ CANCELAR",
                               command=self.mostrar_lista_bingos,
                               font=('Segoe UI', 12, 'bold'),
                               bg='#f44336',
                               fg='white',
                               padx=30,
                               pady=15,  # Más padding
                               relief='flat',
                               cursor='hand2')
        btn_cancelar.pack(side='left', padx=10)
        
        # Actualizar ganancias iniciales
        self.actualizar_ganancias()
    
    def actualizar_ganancias(self, event=None):
        """Actualizar cálculo de ganancias potenciales"""
        try:
            cartones = int(self.entry_cartones.get() or 0)
            precio = float(self.entry_precio.get() or 0)
            ganancias = cartones * precio
            self.lbl_ganancias.config(text=f"Ganancias potenciales: ${ganancias:,.2f}")
        except:
            self.lbl_ganancias.config(text="Ganancias potenciales: $0.00")
    
    def mostrar_lista_bingos(self):
        """Mostrar lista de bingos existentes"""
        # Limpiar frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        
        self.titulo.config(text="GESTIONAR BINGOS EXISTENTES")
        
        # Recargar bingos
        self.bingos = self.cargar_bingos_existentes()
        
        if not self.bingos:
            # Mostrar mensaje si no hay bingos
            frame_vacio = tk.Frame(self.frame_principal, bg='#2d2d2d', padx=30, pady=50)
            frame_vacio.pack(expand=True)
            
            lbl_vacio = tk.Label(frame_vacio,
                               text="🎯 No hay bingos creados aún\n\nCrea tu primer bingo para comenzar",
                               font=('Segoe UI', 14),
                               bg='#2d2d2d',
                               fg='#cccccc',
                               justify='center')
            lbl_vacio.pack()
            
            btn_crear = tk.Button(frame_vacio,
                                text="🆕 CREAR PRIMER BINGO",
                                command=self.mostrar_formulario_creacion,
                                font=('Segoe UI', 12, 'bold'),
                                bg='#4CAF50',
                                fg='white',
                                padx=20,
                                pady=12,  # Más padding
                                relief='flat',
                                cursor='hand2')
            btn_crear.pack(pady=20)
            
            return
        
        # Frame con scroll para la lista
        frame_contenedor = tk.Frame(self.frame_principal, bg='#1e1e1e')
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
        
        # Mostrar cada bingo en una tarjeta
        for bingo in self.bingos:
            self.crear_tarjeta_bingo(frame_lista, bingo)
    
    def crear_tarjeta_bingo(self, parent, bingo):
        """Crear tarjeta para un bingo en la lista"""
        frame_bingo = tk.Frame(parent, bg='#2d2d2d', relief='raised', bd=1, padx=20, pady=15)
        frame_bingo.pack(fill='x', pady=8, padx=10)
        
        # Información del bingo
        frame_info = tk.Frame(frame_bingo, bg='#2d2d2d')
        frame_info.pack(fill='x')
        
        lbl_nombre = tk.Label(frame_info,
                            text=f"🎯 {bingo.nombre}",
                            font=('Segoe UI', 14, 'bold'),
                            bg='#2d2d2d',
                            fg='#4CAF50')
        lbl_nombre.pack(anchor='w')
        
        cartones_vendidos = len(bingo.obtener_cartones_vendidos())
        ganancias = bingo.obtener_ganancias()
        
        lbl_detalles = tk.Label(frame_info,
                              text=f"Cartones: {cartones_vendidos}/{bingo.cantidad_cartones} | "
                                   f"Precio: ${bingo.precio_carton:,.2f} | "
                                   f"Ganancias: ${ganancias:,.2f}",
                              font=('Segoe UI', 10),
                              bg='#2d2d2d',
                              fg='#cccccc')
        lbl_detalles.pack(anchor='w', pady=(5, 0))
        
        # Botones de acción
        frame_botones = tk.Frame(frame_bingo, bg='#2d2d2d')
        frame_botones.pack(fill='x', pady=(10, 0))
        
        btn_abrir = tk.Button(frame_botones,
                            text="📊 ABRIR BINGO",
                            command=lambda b=bingo: self.abrir_bingo(b),
                            font=('Segoe UI', 9, 'bold'),
                            bg='#2196F3',
                            fg='white',
                            padx=15,
                            pady=8,
                            relief='flat',
                            cursor='hand2')
        btn_abrir.pack(side='left', padx=5)
        
        btn_asignaciones = tk.Button(frame_botones,
                                   text="👥 VER ASIGNACIONES",
                                   command=lambda b=bingo: self.ver_asignaciones(b),
                                   font=('Segoe UI', 9, 'bold'),
                                   bg='#9b59b6',
                                   fg='white',
                                   padx=15,
                                   pady=8,
                                   relief='flat',
                                   cursor='hand2')
        btn_asignaciones.pack(side='left', padx=5)
        
        btn_pdf = tk.Button(frame_botones,
                          text="📄 GENERAR PDF",
                          command=lambda b=bingo: b.exportar_pdf(),
                          font=('Segoe UI', 9, 'bold'),
                          bg='#FF9800',
                          fg='white',
                          padx=15,
                          pady=8,
                          relief='flat',
                          cursor='hand2')
        btn_pdf.pack(side='left', padx=5)
        
        btn_eliminar = tk.Button(frame_botones,
                               text="🗑️ ELIMINAR",
                               command=lambda b=bingo: self.eliminar_bingo(b),
                               font=('Segoe UI', 9, 'bold'),
                               bg='#e74c3c',
                               fg='white',
                               padx=15,
                               pady=8,
                               relief='flat',
                               cursor='hand2')
        btn_eliminar.pack(side='left', padx=5)
    
    def abrir_bingo(self, bingo):
        """Abrir un bingo en la vista de tablas"""
        self.controlador.mostrar_vista("vista_tablas", {"bingo": bingo})
    
    def ver_asignaciones(self, bingo):
        """Ver las asignaciones de un bingo"""
        self.controlador.mostrar_vista("vista_asignaciones", {"bingo": bingo})

    
    def eliminar_bingo(self, bingo):
        """Eliminar un bingo"""
        if messagebox.askyesno("Confirmar Eliminación",
                             f"¿Estás seguro de eliminar el bingo '{bingo.nombre}'?\n\n"
                             f"Esta acción no se puede deshacer y se perderán todos los datos."):
            if bingo.eliminar():
                self.bingos.remove(bingo)
                messagebox.showinfo("Éxito", f"Bingo '{bingo.nombre}' eliminado correctamente")
                self.mostrar_lista_bingos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el bingo")
    
    def crear_bingo(self):
        """Crear un nuevo bingo con los datos del formulario"""
        nombre = self.entry_nombre.get().strip()
        cartones_text = self.entry_cartones.get().strip()
        precio_text = self.entry_precio.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "❌ Por favor ingresa un nombre para el bingo")
            return
        
        try:
            cantidad_cartones = int(cartones_text)
            if cantidad_cartones <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "❌ La cantidad de cartones debe ser un número válido mayor a 0")
            return
        
        try:
            precio_carton = float(precio_text)
            if precio_carton < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "❌ El precio debe ser un número válido mayor o igual a 0")
            return
        
        # Verificar si ya existe un bingo con ese nombre
        for bingo_existente in self.bingos:
            if bingo_existente.nombre.lower() == nombre.lower():
                messagebox.showerror("Error", f"❌ Ya existe un bingo con el nombre '{nombre}'")
                return
        
        # Crear nuevo bingo
        nuevo_bingo = Bingo(nombre, cantidad_cartones, precio_carton)
        self.bingos.append(nuevo_bingo)
        
        messagebox.showinfo("Éxito", 
                          f"✅ Bingo '{nombre}' creado exitosamente!\n\n"
                          f"🎫 Cartones: {cantidad_cartones}\n"
                          f"💰 Precio: ${precio_carton:,.2f}\n"
                          f"💵 Ganancia potencial: ${cantidad_cartones * precio_carton:,.2f}")
        
        # Navegar a la vista de tablas
        self.controlador.mostrar_vista("vista_tablas", {"bingo": nuevo_bingo})
    
    def volver_menu(self):
        """Volver al menú principal"""
        self.controlador.mostrar_vista("menu_principal")
    
    def mostrar(self, datos=None):
        """Mostrar esta vista"""
        self.frame.pack(fill="both", expand=True)
        self.mostrar_lista_bingos()
    
    def ocultar(self):
        """Ocultar esta vista"""
        self.frame.pack_forget()